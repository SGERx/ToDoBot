import os
from pathlib import Path

import psycopg2
from dotenv import load_dotenv
from loguru import logger
from psycopg2 import sql
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

logger.add("logs/db_script.log", rotation="100 MB", level="INFO")


def load_environment_variables():
    logger.info("Запуск функции {func}", func="load_environment_variables")
    env_path = Path(__file__).resolve().parent.parent / '.env'
    logger.info(f"Путь к файлу .env: {env_path}")
    logger.info(f"Содержимое .env: {open(env_path).read()}")
    load_dotenv(dotenv_path=env_path)
    logger.info("Завершение функции {func}", func="load_environment_variables")


def get_connection_params_from_env():
    logger.info("Запуск функции {func}", func="get_connection_params_from_env")
    return {
        'dbname': os.getenv('DB_NAME'),
        'user': os.getenv('DB_USER'),
        'password': os.getenv('DB_PASSWORD'),
        'host': os.getenv('DB_HOST'),
        'port': os.getenv('DB_PORT')
    }


def execute_db_creation(connection_parameters, database_name):
    logger.info("Запуск функции {func}", func="execute_db_creation")
    try:
        connection_parameters.pop('dbname', None)
        connection = psycopg2.connect(**connection_parameters)
        connection.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)

        cursor = connection.cursor()
        cursor.execute("ROLLBACK;")

        cursor.execute(sql.SQL("CREATE DATABASE {}").format(
            sql.Identifier(database_name)))

        connection.commit()
        logger.info(f"Создание базы данных '{database_name}' завершено")
    except psycopg2.Error as e:
        logger.info(f"Ошибка при создании базы данных: {e}")

    finally:
        if connection:
            connection.close()
    logger.info("Завершение функции {func}", func="load_environment_variables")


def execute_tasks_table_creation(connection_parameters):
    logger.info("Запуск функции {func}", func="execute_tasks_table_creation")
    logger.info(f"Параметры для создания таблицы - {connection_parameters}")
    connection = psycopg2.connect(**connection_parameters)
    cursor = connection.cursor()

    try:
        create_tasks_query = '''CREATE TABLE tasks (
        id SERIAL PRIMARY KEY,
        user_id INTEGER REFERENCES user(id),
        title VARCHAR(255) NOT NULL,
        description TEXT NOT NULL,
        task_date DATE,
        task_time TIME,
        status VARCHAR(50) NOT NULL
        );
        '''
        cursor.execute(create_tasks_query)
        logger.info("Таблица tasks создана")
    except Exception as e:
        connection.rollback()
        logger.info(f"Ошибка создания таблицы tasks - исключение {e}")
    finally:
        connection.commit()
        connection.close()
        logger.info("Применение изменений, внесенных в базу данных ")
    logger.info("Завершение функции {func}", func="execute_tasks_table_creation")


if __name__ == "__main__":
    logger.info("Запуск файла {file} через __main__", file="init_postgres.py")
    load_environment_variables()
    connection_parameters = get_connection_params_from_env()
    creation_params = get_connection_params_from_env()
    logger.info(f"Параметры соединения - {connection_parameters}")
    database_name = connection_parameters['dbname']
    logger.info(f"Имя создаваемой базы данных - {database_name}")
    execute_db_creation(connection_parameters, database_name)
    execute_tasks_table_creation(creation_params)
    logger.info("Завершение файла {file} через __main__", file="init_postgres.py")
