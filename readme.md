# Gatherer
Collects data from multiple MySQL Databases in a multi-tenant architecture. Gatherer helps to gather the scattered data across different databases which share the same schema. It outputs the whole collected data into a single CSV file.

##### Pip
You can install this package from pip by running the following command :
```html
pip install gatherer
```

#### Pros

- Cuts out the need of performing a manual job by executing your query on each database and then merging the results.
- No wait for huge response which may fail or exceed different limits.
- Specific databases can be excluded.
- Large and complex queries can be read from a file, so, there is no need of placing your query inside the code.
- Catalog can be loaded from three different sources (manual list, the same instance as tenants or the remote instance).
- Eliminates the need of advanced knowledge in cross-database queries.
- The process can be terminated at any time, and it can be restarted later (which means files are stored locally after every successful execution on a tenant).

#### Parameters

Name | Description | Type | Default
--- | --- | --- | --- 
host | The MySQL Instance IP/Identifier of Tenant Database/s (or all-with Catalog). | string | localhost
user | The MySQL Instance User of Tenant Databases (or all-with-Catalog). | string | root
password | The MySQL Instance Password of Tenant Databases (or all-with-Catalog). | string | Empty
port | The MySQL Instance Port of Tenant Databases (or all-with-Catalog). | integer | 3306
output_dir |  Each tenant file will be stored here before the final merge. Consider it as a temporary database. | string | output_dir
tenant_query | The SELECT query to be performed. | string | None
tenant_query_source | The SELECT query to be performed from file. | string | None
tenant_dbs | Databases given manually. If this is set then Catalog parameters will not be taken into consideration. | array | None
skip_tenant_dbs | Tenant Databases to be skipped. | string | None
catalog_db | The Catalog Database. The Catalog Query will be executed here. | string | None
catalog_query | The Query to SELECT Tenants Database names. | string | None
catalog_host | The MySQL Instance IP/Identifier of Catalog.  | string | None
catalog_user | Catalog host User. | string | None
catalog_password | Catalog host Password | string | None
output_file_name | The name of the file which contains the final result. | string | output
skip_processed_tenants | Tenant Databases to be skipped. | string | None
file_encoding | The File Encoding to be used in final CSV. | string | latin-1
file_headers | The Headers in final CSV file. | string | latin-1
debug | Debug the process on console. | boolean | False



### How it works
Collector runs a given query in each tenant database which is present in its {list}, this list is either given manually (filled with Database names as array in your code) or fetched automatically by a given Catalog query (read from Catalog and outputed into an array).
Each of these runs yields a result which is outputted into a CSV file in {output_dir}. At the end of this, all tenant files are merged into a single one.

### Simple usage

```python

import gatherer

gatherer.gather(host='localhost',
                  user='root',
                  password='',
                  port=3306,
                  tenant_query='SELECT my_column_1,my_column_2,my_column_3 FROM my_table;',
                  skip_tenant_dbs=['My_Tenant1_DB', 'My_Tenant2_DB'],
                  catalog_db='CATALOG_DB',
                  catalog_query='SELECT my_tenant_database_name FROM my_tenants;',
                  output_dir='temp_output'
                  )

```

### Contributions 
Feel free to contribute on development, testing or eventual bug reporting.

### Support
For general questions about the Resurrector, tweet at @rexshijaku or write me an email on rexhepshijaku@gmail.com.

### Author
##### Rexhep Shijaku
 - Email : rexhepshijaku@gmail.com
 - Twitter : https://twitter.com/rexshijaku

### License
MIT License

Copyright (c) 2022 | Rexhep Shijaku

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
