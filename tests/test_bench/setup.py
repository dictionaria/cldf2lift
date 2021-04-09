from setuptools import setup


setup(
    name='cldfbench_test_bench',
    py_modules=['cldfbench_test_bench'],
    include_package_data=True,
    zip_safe=False,
    entry_points={
        'cldfbench.dataset': [
            'test_bench=cldfbench_test_bench:Dataset',
        ]
    },
    install_requires=[
        'cldfbench',
    ],
    extras_require={
        'test': [
            'pytest-cldf',
        ],
    },
)
