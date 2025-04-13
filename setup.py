from setuptools import setup, find_packages

setup(
    name="text_processor",
    version="0.1.0",
    packages=find_packages(),
    description="Инструмент для обработки текстовых файлов по конфигурации",
    author="CpyBAgy - Ivan Bashkatov",
    python_requires=">=3.6",
    entry_points={
        "console_scripts": [
            "text_processor=script:main",
        ],
    },
    test_suite="tests",
    tests_require=["pytest", "pytest-cov"],
    extras_require={"dev": ["pytest", "pytest-cov", "black", "flake8"]},
)
