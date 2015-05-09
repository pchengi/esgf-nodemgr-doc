import user_api

components = ["publisher", "attribute_service"]

projects = ["ACME", "CMIP5"]

for n in components:

    user_api.init_directory(n)

for n in projects:
    
    user_api.init_project(n)

