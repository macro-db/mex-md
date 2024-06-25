<!DOCTYPE html>
<html>
<body>

<h1>Monthly and Quarterly Macroeconomic Database</h1>

<p>This repository hosts a collection of macroeconomic datasets designed to support empirical research and analysis in economics. The database is updated monthly and quarterly to reflect the latest economic indicators from the Bank of Mexico and Instituto Nacional de Estadística y Geografía (INEGI).</p>

<h2>Motivation</h2>

<p>The motivation behind this repository is to provide researchers with a comprehensive and regularly updated dataset suitable for "big data" empirical analysis in economics. The dataset aims to mimic existing literature's coverage while offering several key advantages:</p>

<ul>
    <li><strong>Monthly Updates</strong>: Data is sourced from Banxico and INEGI and updated monthly, ensuring researchers have access to the most recent information.</li>
    <li><strong>Public Accessibility</strong>: The dataset is publicly accessible, facilitating transparency, comparison, and replication of research findings.</li>
    <li><strong>Data Management</strong>: By centralizing data updates and revisions, researchers are relieved from the burden of managing dataset changes.</li>
</ul>

<p>The repository includes two main datasets:</p>
<ul>
    <li><strong>Monthly Dataset</strong>: Contains macroeconomic indicators updated monthly.</li>
    <li><strong>Quarterly Dataset</strong>: Contains macroeconomic indicators updated on a quarterly basis.</li>
</ul>

<h2>Repository Structure</h2>

<pre>
|-- data/
    |-- MD_YYYY_MM_DD.csv       # Monthly updated dataset
    |-- QD_YYYY_MM_DD.csv       # Quarterly updated dataset
|-- README.md                   
</pre>

<p>The <code>data/</code> folder contains the archived datasets in CSV format. The files are named using the format <code>MD_YYYY_MM_DD</code> for the monthly database and <code>QD_YYYY_MM_DD</code> for the quarterly database, where <code>YYYY</code> represents the year, <code>MM</code> represents the month, and <code>DD</code> represents the day of the dataset. This allows users to replicate past results with specific data versions.</p>

<h2>Usage</h2>

<p>Researchers are encouraged to explore and utilize the datasets for various empirical studies in economics. Proper citation and acknowledgment of the data sources (Bank of Mexico and INEGI) are recommended.</p>

<h2>Citation</h2>

<p>If you use this dataset in your research or publication, please cite it as follows:</p>

<p><em>Example citation:</em><br>
Author(s), "Monthly and Quarterly Macroeconomic Database", GitHub repository, (Year), <a href="https://github.com/ymacro-db/mex-db">https://github.com/ymacro-db/mex-db</a>.</p>

</body>
</html>
