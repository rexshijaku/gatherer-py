import os

from gatherer.db_handler import DBHandler
from gatherer.f_handler import FHandler


def gather(host='localhost', user='root', password='', port=3306,
            output_dir='output_dir',
            tenant_query=None,
            tenant_query_source=None,
            tenant_dbs=None,
            skip_tenant_dbs=None,
            catalog_db=None,
            catalog_query=None,
            catalog_host=None, catalog_user=None,
            catalog_password=None, catalog_port=None,
            output_file_name='output',
            skip_processed_tenants=False,
            file_encoding='latin-1',
            file_headers=None,
            debug=False):
    catalog_required = tenant_dbs is None

    if tenant_dbs is not None:  # when tenants are specified manually no need for query
        tenant_query = None

    if tenant_query is not None:  # or vice versa, when query is set we don't need manual tenant dbs
        tenant_dbs = None

    if tenant_query_source is not None:  # when query source (file) was specified no need for the tenant_query
        tenant_query = None

    dh = DBHandler(host=host, user=user, password=password, port=port,
                   tenant_query=tenant_query, tenant_query_source=tenant_query_source)

    if catalog_required:
        if catalog_host is None:  # if host credentials aren't provided then use tenant connection credentials
            dh.setCatalog(catalog_db, catalog_query,
                          catalog_host=host, catalog_user=user, catalog_password=password,
                          catalog_port=port)
        else:  # otherwise use the provided credentials (catalog specific)
            dh.setCatalog(catalog_db, catalog_query,
                          catalog_host=catalog_host, catalog_user=catalog_user, catalog_password=catalog_password,
                          catalog_port=catalog_port)

        tenant_dbs = dh.get_tenants()  # fill tenant dbs from catalog query

    if skip_tenant_dbs is not None:  # lowercase all for comparison purpose
        skip_tenant_dbs = list(map(str.lower, skip_tenant_dbs))

    for tenant_db in tenant_dbs:

        if tenant_db is None:
            continue

        if skip_tenant_dbs is not None and tenant_db.lower() in skip_tenant_dbs:
            if debug:
                print("tenant is being skipped " + tenant_db)
            continue

        tenant_output_file = output_dir + '/' + tenant_db.lower() + '.csv'
        if skip_processed_tenants and os.path.isfile(tenant_output_file):
            if debug:
                print('the tenant was already queried ' + tenant_output_file)
            continue

        tenant_result = dh.get_tenant_result(tenant_db)
        dh.saveDBResult(tenant_result, tenant_output_file)

    fh = FHandler(encoding=file_encoding)
    files = fh.mergeFiles(all_files_path=output_dir, headers=file_headers)
    fh.save(files, save_path=output_file_name + '.csv')
