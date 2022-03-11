.. flusstools documentation parent file.


TKE Analyst
===========

This Python3 code aids in analyzing raw measurements with an Acoustic Doppler Velocimeter (ADV) producing ``*.vno`` and ``*.vna`` files. It detects and removes spikes according to `Nikora and Goring (1998) <https://doi.org/10.1061/(ASCE)0733-9429(1998)124:6(630)>`_ and  `Goring and Nikora (2002) <https://doi.org/10.1061/(ASCE)0733-9429(2002)128:1(117)>`_.

The code was originally developed in Matlab(R) at the `Nepf Environmental Fluid Mechanics Laboratory <https://nepf.mit.edu/>`_ (`Massachusetts Institute of Technology <https://web.mit.edu/>`_).

.. important::

    ``*.vno`` and ``*.vna`` files need to comply with the following name convetion:
    ``XX_YY_ZZ_something.vna`` where ``XX``, ``YY``, and ``ZZ`` are streamwise (x), perpendicular (y), and vertical (z) coordinates in CENTIMETERS, respectively. Anything else added after ``ZZ_`` is ignore by the code (it just copies it for the sake of dataset naming).

.. note::

    This documentation is also as available as `style-adapted PDF <https://tke-analyst.readthedocs.io/_/downloads/en/latest/pdf/>`_.

Requirements \& Installation
============================

*Time requirement: 5-10 min.*

Get Python
----------

To get the code running, the following software is needed and their installation instructions are provided below:

- Python `>=3.6`
- NumPy `>=1.20`
- Openpyxl `3.0.3`
- Pandas `>=1.4.1`
- Matplotlib `>=3.5.0`

Start with downloading and installing the latest version of `Anaconda Python <https://www.anaconda.com/products/individual>`_.  Alternatively, downloading and installing a pure `Python <https://www.python.org/downloads/>`_ interpreter will also work. Detailed information about installing Python is available in the `Anaconda Docs <https://docs.continuum.io/anaconda/install/windows/>`_ and at `hydro-informatics.com/python-basics <https://hydro-informatics.com/python-basics/pyinstall.html>`_.

To install the NumPy, Openpyxl, Pandas, and Matplotlib libraries after installing Anaconda, open Anaconda Prompt (e.g., click on the Windows icon, tap ``anaconda prompt``, and hit enter``). In Anaconda Prompt, enter the following command sequence to install the libraries in the **base** environment. The installation may take a while depending on your internet speed.

.. code-block::

    conda install -c anaconda numpy
    conda install -c anaconda openpyxl
    conda install -c anaconda numpy
    conda install -c conda-forge pandas
    conda install -c conda-forge matplotlib

If you are struggling with the dark window and blinking cursor of Anaconda Prompt, worry not. You can also use Anaconda Navigator and install the four libraries (in the above order) in Anaconda Navigator.

.. note::

    Alternatively, create a new conda environment to install the three libraries for this application. However, creating a new environment may eat up a lot of disk space and installing the Python-omnipresent libraries NumPy, Openpyxl, Pandas, and Maplotlib in the **base** environment does not hurt.


Run the Code
------------

First-time Usage
~~~~~~~~~~~~~~~~

The code can be either started from Terminal (Anaconda Prompt) or within an Integrated Development Environment (**IDE**). With Anaconda installed, consider using Spyder (Anaconda Navigator > `Spyder IDE <https://www.spyder-ide.org/>`_).

`Download tke-calculator.zip <https://github.com/sschwindt/tke-calculator/archive/refs/heads/main.zip>`_  and unpack it to the directory where you want to run the code.

.. tip::

    Alternative to downloading the zip file, you may want to ``git clone`` the repository, which enables regular updating of the code (e.g., if there is an update of plot functions available). For using git, make sure that `git bash <https://git-scm.com/downloads>`_ is installed on your computer. Then, open git bash, `cd <https://docs.microsoft.com/en-us/windows-server/administration/windows-commands/cd>`_ into the directory where you want to download the code and type:

    ``git clone https://github.com/sschwindt/tke-calculator.git``

    To update any time, ``cd`` into the directory where ``tke-calculator`` lives and type:

    ``git pull --rebase``


Regular Usage
~~~~~~~~~~~~~

With Python installed and the code living on your computer:

- Copy your data to the ``data`` sub-folder of ``tke-analyst`` (next to the folder ``test-example`` that contains three exemplary ``*.vna`` files). Make sure the files are named with ``XX_YY_ZZ_something.vna`` where ``XX``, ``YY``, and ``ZZ`` are streamwise (x), perpendicular (y), and vertical (z) coordinates in CENTIMETERS, respectively
- Complete the required information on the experimental setup in ``tke-calculator/input.xlsx`` (see below figure). **IMPORTANT: Never modify column A or any list in the sourcetables sheet (unless you also modify ``load_input_defs`` in line 25ff of ``profile_analyst.py``).** The code uses the text provided in these areas of *input.xlsx* to identify setups. If useful, consider substituting the *Wood* wording in your mind and with a note in column C with your characteristic turbulence objects, but do not modify column A.
- Open Anaconda Prompt (or any other Python-able Terminal) and:
    + ``cd`` into the code directory (e.g., ``cd "C:research\project\tke-analyst"`` if you unpacked ``tke-analyst`` to a folder living in the directory *C:research\project\*)
    + run the code: ``python profile_analyst.py``
    + wait until the code finished with ``-- DONE -- ALL TASKS FINISHED --``
- After a successful run, the code will have produced the following files in ``...\tke-analyst\data\TEST`` (where ``TEST`` may correspond to ``test-example``):
    + ``.xlsx`` files of full-time series data, with spikes and despiked.
    + ``.xlsx`` files of statistic summaries (i.e., average, standard deviation *std*, TKE) of velocity parameters with x, y, and z positions, with spikes and despiked.
    + Two plots (``norm-tke-x.png`` and ``norm-tke-x-despiked.png``) showing normalized TKE plotted against normalized x, with spikes and despiked, respectively.

.. figure:: https://github.com/sschwindt/tke-calculator/raw/main/docs/img/input-xlsx.jpg
   :alt: input turbulent tke experiment setup parameters

   *The interface of the input.xlsx workbook for entering experiment parameters and specifying a despiking method.*


Usage Example
=============

For example, download and unpack the code to your hard-disk in a folder called ``C:\my-project\tke-analyst\``. To analyze the ``*.vna`` files in ``test-example``, they were copied into a test folder that lives in the ``data`` folder.

The definitions in the above-shown ``input.xlsx`` define x-normalization as a function of a wood log length


.. toctree::
    :hidden:

    Get Started <self>

.. toctree::
    :hidden:

    Developer Docs <codedocs>

.. toctree::
    :hidden:

    License <license>



