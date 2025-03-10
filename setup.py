import os
from setuptools import setup


def read(fname) -> str:
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


setup(
    name="import_batch_ftcg",
    version="1.0.0",
    author="Maël Le Gall",
    author_email="ans-terminologies@esante.gouv.fr",
    description=("Création des fichiers d'import en batch contenant"
                 "les nouvelles traductions du FTCG (French Translation"
                 " Collaboration Group) de la SNOMED Int."),
    license="MIT",
    url="https://github.com/ansforge/interop-outil-nrc-import-batch-ftcg",
    packages=['import_batch_ftcg', 'test'],
    install_requires=[
        "pandas",
    ],
    long_description=read('README'),
)
