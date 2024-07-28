import ast
import importlib
import logging
import logging.config
import os
import sys
from pathlib import Path
from typing import LiteralString


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

    def __init__(self, directory: Path, find_sub_class: object, work_dir: Path | None = None):
        """
        Initializes the ClassFinder with the specified directory and optional working directory.

        Args:
            directory (Path): The directory to search for Python files.
            find_sub_class (object): The class to find in the specified directory.
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

    def find_python_files(self) -> list[LiteralString | str | bytes]:
        """
        Recursively finds all Python files in the specified directory.

        Returns:
            list[LiteralString | str | bytes]: A list of paths to Python files.
        """
        python_files = []
        for root, _, files in os.walk(self.directory):
            for file in files:
                if file.endswith(".py"):
                    python_files.append(os.path.join(root, file))  # noqa: PTH118
        return python_files

    def find_classes_in_file(self, file_path) -> list[tuple[str, list[str]]]:
        """
        Finds all classes in the specified Python file and checks their parent classes.

        Args:
            file_path (str): The path to the Python file.

        Returns:
            list[tuple[str, list[str]]]: A list of tuples containing class names and their base classes.
        """
        with open(file_path, encoding="utf-8") as file:  # noqa: PTH123
            tree = ast.parse(file.read(), filename=file_path)

        classes = []
        for node in ast.walk(tree):
            if isinstance(node, ast.ClassDef):
                bases = [base.id for base in node.bases if isinstance(base, ast.Name)]
                classes.append((node.name, bases))

        return classes

    def find_all_classes(self) -> dict[str : list[tuple[str, list[str]]]]:
        """
        Finds all classes in Python files in the specified directory and checks their parent classes.

        Returns:
            dict[str: list[tuple[str, list[str]]]]: A dictionary with file paths as keys and lists of class tuples as values.
        """
        python_files = self.find_python_files()
        all_classes = {}
        for file_path in python_files:
            classes = self.find_classes_in_file(file_path)
            if classes:
                all_classes[file_path] = classes
        return all_classes

    def generate_import_statements(self, classes) -> list[tuple[str, str]]:
        """
        Generates import statements for classes inherited from Base.

        Args:
            classes (dict[str: list[tuple[str, list[str]]]]): A dictionary with file paths as keys and lists of class tuples as values.

        Returns:
            list[tuple[str, str]]: A list of tuples containing module paths and class names.
        """
        import_statements = []
        for file_path, class_list in classes.items():
            for class_name, bases in class_list:
                if self.find_sub_class.__name__ in bases:
                    module_path = os.path.splitext(os.path.relpath(file_path, self.directory))[0].replace(os.sep, ".")  # noqa: PTH122
                    import_statements.append((module_path, class_name))
        return import_statements

    def dynamic_import(self, import_statements) -> list[str]:
        """
        Dynamically imports the specified classes.

        Args:
            import_statements (list[tuple[str, str]]): A list of tuples containing module paths and class names.

        Returns:
            list[str]: A list of import results with success or failure messages.
        """
        answer = []
        for module_path, class_name in import_statements:
            msg = f"  - {module_path}.{class_name}"
            try:
                module = importlib.import_module(module_path)
                _ = getattr(module, class_name)
                answer.append(f"\033[32m{msg.ljust(50, "."):<50}... OK\033[0m")
            except Exception as e:
                answer.append(f"\033[31m{msg.ljust(50, "."):<50}... FAIL: {e.__class__.__name__}\033[0m")
        return answer

    def run(self):
        """
        Runs the class finding and dynamic import process.
        """
        classes = self.find_all_classes()
        for file_path, class_list in classes.items():
            msg = f"\033[37mFile: {file_path}\033[0m"
            self.logger.debug(msg)
            for class_name, bases in class_list:
                msg = f"  Class: {class_name}, Parents classes: {bases}"
                self.logger.debug(msg)

        imports = self.generate_import_statements(classes)
        for module_path, class_name in imports:
            msg = f"from {module_path} import {class_name}"
            self.logger.debug(msg)
        logger_msg = ["\033[37mStarting dynamic import...\033[0m"]
        logger_msg.extend(self.dynamic_import(imports))
        logger_msg.append("\033[37mDynamic import finished.\033[0m")
        self.logger.info("\n".join(logger_msg))

    def setup_logger(self):
        """
        Sets up the logger for the ClassFinder.

        Returns:
            logging.Logger: The configured logger instance.
        """
        logging.config.dictConfig(self.__logging_config)
        logger = logging.getLogger("DynamicImportLogger")
        return logger
