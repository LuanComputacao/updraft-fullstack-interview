#!/bin/bash

set -e

function create_user() {
        local user=$1
        local password=$2
        echo "Creating user '$user'"
        psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" <<-EOSQL
            CREATE USER "$user" with encrypted password '$password';
EOSQL
}

function create_database() {
        local database=$1
        echo "Creating database '$database'"
        psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" <<-EOSQL
            CREATE DATABASE "$database";
EOSQL
}


function grant_access() {
    local database=$1
    local user=$2
        echo "Grant access user '$user'"
        psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" <<-EOSQL
        GRANT CREATE, CONNECT ON DATABASE "$database" TO "$user";
        ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT SELECT, UPDATE, INSERT, DELETE, REFERENCES ON TABLES TO "$user";
EOSQL
}

function grant_schema_access() {
    local database=$1
    local user=$2
    echo "Granting schema access to user '$user'"
    psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" --dbname="$database" <<-EOSQL
        GRANT ALL PRIVILEGES ON SCHEMA public TO "$user";
        GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO "$user";
        GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA public TO "$user";
EOSQL
}

if [ -n "$POSTGRES_NON_ROOT_USER" ]; then
    create_user $POSTGRES_NON_ROOT_USER $POSTGRES_NON_ROOT_USER_PASSWORD
fi


if [ -n "$POSTGRES_MULTIPLE_DATABASES" ]; then
        for db in $(echo $POSTGRES_MULTIPLE_DATABASES | tr ',' ' '); do
                create_database $db
        if [ -n "$POSTGRES_NON_ROOT_USER" ]; then
            grant_access $db $POSTGRES_NON_ROOT_USER
            grant_schema_access $db $POSTGRES_NON_ROOT_USER
        fi
        done
else
    if [ -n "$POSTGRES_NON_ROOT_USER" ]; then
        grant_access $POSTGRES_DB $POSTGRES_NON_ROOT_USER
        grant_schema_access $db $POSTGRES_NON_ROOT_USER
    fi
fi