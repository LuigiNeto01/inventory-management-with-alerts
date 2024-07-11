# Inventory Management Application

This is an inventory management application built with Python using `tkinter` for the graphical interface and `mysql.connector` for database interaction. The application allows you to monitor and manage an inventory of products, providing real-time alerts for any changes.

## Features

- **Inventory Display**: View current inventory data with product names and quantities.
- **Real-Time Alerts**: Receive pop-up notifications for any changes in inventory, including additions, removals, and quantity changes.
- **Configuration**: Set the duration for pop-up alerts via a configuration tab.

## Installation

1. **Clone the repository**:
    ```bash
    git clone https://github.com/your-username/inventory-management-app.git
    cd inventory-management-app
    ```

2. **Install required packages**:
    Ensure you have `mysql-connector-python` installed. If not, install it using pip:
    ```bash
    pip install mysql-connector-python
    ```

3. **Set up MySQL database**:
    Create a MySQL database and table:
    ```sql
    CREATE DATABASE estoque;
    USE estoque;
    CREATE TABLE estoque_prod (
        id INT AUTO_INCREMENT PRIMARY KEY,
        nome VARCHAR(255) NOT NULL,
        quantidade INT NOT NULL
    );
    ```

4. **Configure the database connection**:
    Update the `db_connect` method in `EstoqueApp` class with your MySQL credentials:
    ```python
    conexao = mysql.connector.connect(
        host="localhost",
        user="your-username",
        password="your-password",
        database="estoque"
    )
    ```

## Usage

1. **Run the application**:
    ```bash
    python inventory_app.py
    ```

2. **Navigate through the application**:
    - **Management Tab**: View and monitor your inventory data.
    - **Configuration Tab**: Set the duration for pop-up alerts.

## Configuration

- The application uses a `config.json` file to store configuration settings. If the file doesn't exist, it will be created with default settings.
- You can adjust the duration of pop-up alerts in the "Configuration" tab and save the changes.

## Author

- **Your Name** - [your-username](https://github.com/your-username)

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
