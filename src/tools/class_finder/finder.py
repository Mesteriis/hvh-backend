import importlib
import logging
import logging.config
import os
import sys
from pathlib import Path


class ClassFinder:
    """
    A class to find and dynamically import Python classes from a specified directory.

    Attributes:
        directory (Path): The directory to search for Python files.
        logger (logging.Logger): The logger instance for logging messages.
    """

    __logging_config = {
        "version": 1,
        "formatters": {
            "default": {
                "format": "%(levelname)s %(asctime)s %(name)s:\n%(message)s",
            },
        },
        "handlers": {
            "console": {
                "class": "logging.StreamHandler",
                "formatter": "default",
                "level": "INFO",
            },
        },
        "root": {
            "handlers": ["console"],
            "level": "INFO",
        },
    }

    def __init__(self, directory: Path, find_sub_class: type, work_dir: Path | None = None):
        """
        Initializes the ClassFinder with the specified directory and optional working directory.

        Args:
            directory (Path): The directory to search for Python files.
            find_sub_class (type): The class to find in the specified directory.
            work_dir (Path, optional): The working directory to add to sys.path. Defaults to None.


        Raises:
            FileNotFoundError: If the specified directory does not exist.
        """
        if work_dir is not None:
            sys.path.append(str(work_dir))
        if not directory.exists():
            raise FileNotFoundError(f"Directory not found: {directory}")
        self.find_sub_class = find_sub_class
        self.directory = directory
        self.logger = self.setup_logger()

    def find_python_files(self) -> list[str]:
        """
        Recursively finds all Python files in the specified directory.

        Returns:
            list[str]: A list of paths to Python files.
        """
        python_files = []
        for root, _, files in os.walk(self.directory):
            for file in files:
                if file.endswith(".py"):
                    python_files.append(os.path.join(root, file))  # noqa: PTH118
        return python_files

    def find_classes_in_file(self, file_path: str) -> list[str]:
        """
        Finds all classes in the specified Python file by importing and checking inheritance.

        Args:
            file_path (str): The path to the Python file.

        Returns:
            list[str]: A list of class names that inherit from the specified base class.
        """
        module_path = str(Path(file_path).relative_to(self.directory).with_suffix("")).replace(os.sep, ".")
        if "models" not in module_path:
            return []
        try:
            module = importlib.import_module(module_path)
        except (ModuleNotFoundError, ImportError):
            self.logger.warning(f"Module not found: {module_path}")
            return []

        classes = []
        for attr_name in dir(module):
            attr = getattr(module, attr_name)
            if isinstance(attr, type) and issubclass(attr, self.find_sub_class) and attr is not self.find_sub_class:
                classes.append(attr_name)

        return classes

    def find_all_classes(self) -> dict[str, list[str]]:
        """
        Finds all classes in Python files in the specified directory and checks their inheritance.

        Returns:
            dict[str, list[str]]: A dictionary with file paths as keys and lists of class names as values.
        """
        python_files = self.find_python_files()
        all_classes = {}
        for file_path in python_files:
            classes = self.find_classes_in_file(file_path)
            if classes:
                all_classes[file_path] = classes
        return all_classes

    def generate_import_statements(self, classes: dict[str, list[str]]) -> list[tuple[str, str]]:
        """
        Generates import statements for classes inherited from the specified base class.

        Args:
            classes (dict[str, list[str]]): A dictionary with file paths as keys and lists of class names as values.

        Returns:
            list[tuple[str, str]]: A list of tuples containing module paths and class names.
        """
        import_statements = []
        for file_path, class_list in classes.items():
            module_path = str(Path(file_path).relative_to(self.directory).with_suffix("")).replace(os.sep, ".")
            for class_name in class_list:
                import_statements.append((module_path, class_name))
        return import_statements

    @staticmethod
    def dynamic_import(import_statements: list[tuple[str, str]]) -> list[str]:
        """
        Dynamically imports the specified classes.

        Args:
            import_statements (list[tuple[str, str]]): A list of tuples containing module paths and class names.

        Returns:
            list[str]: A list of import results with success or failure messages.
        """
        report = []
        for module_path, class_name in import_statements:
            msg = f"  - {module_path}.{class_name}"
            try:
                module = importlib.import_module(module_path)
                _ = getattr(module, class_name)
                report.append(f"\033[32m{msg.ljust(50, ".")}... OK\033[0m")
            except Exception as e:
                report.append(
                    f"\033[31m{msg.ljust(50, ".")}... FAIL \n    {e.__class__.__name__}:\033[0m \033[37m{e}\033[0m"
                )
        return report

    def run(self):
        """
        Runs the class finding and dynamic import process.
        """
        classes = self.find_all_classes()
        for file_path, class_list in classes.items():
            msg = f"\033[37mFile: {file_path}\033[0m"
            self.logger.debug(msg)
            for class_name in class_list:
                msg = f"  Class: {class_name}, Inherits from: {self.find_sub_class.__name__}"
                self.logger.debug(msg)

        imports = self.generate_import_statements(classes)
        for module_path, class_name in imports:
            msg = f"from {module_path} import {class_name}"
            self.logger.debug(msg)
        logger_msg = ["\033[37mStarting dynamic import...\033[0m"]
        logger_msg.extend(self.dynamic_import(imports))
        logger_msg.append("\033[37mDynamic import finished.\033[0m")
        self.logger.info("\n".join(logger_msg))

    def setup_logger(self) -> logging.Logger:
        """
        Sets up the logger for the ClassFinder.

        Returns:
            logging.Logger: The configured logger instance.
        """
        logging.config.dictConfig(self.__logging_config)
        logger = logging.getLogger("DynamicImportLogger")
        return logger
