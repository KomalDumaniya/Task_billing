# Task_billing

## Overview
Developed a custom Odoo module for task billing, integrating project.task and account.move models for billing processes.

## Features
- Create Bill from Task: Generate vendor bills directly from project tasks.
- View Bills: View all posted bills related to tasks.
- Cancel Bills: Cancel bills associated with tasks.
- Automatic Bill Confirmation: Automatically confirm bills upon creation.

## Installation

1. Clone the repository:
    bash
    git clone https://github.com/KomalDumaniya/Task_billing
    
2. Install the required dependencies:
    bash
    pip install -r requirements.txt
    
3. Run the Odoo server:
    bash
    ./odoo-bin

## Configuration

1. **Activate Developer Mode**: Go to your Odoo instance and activate developer mode from the settings.
2. **Install the Module**: Go to Apps, search for `Task Billing`, and install the module.
3. **Set Up Project Task**: Configure your project tasks to enable billing functionalities.

## Models and Methods

### Key Models:
- `project.task`: Extends the project task model to include billing functionalities.
- `account.move`: Handles the creation and management of vendor bills.

### Key Methods:
- `action_create_bill`: Method to create a bill from a task.
- `action_view_bills`: Method to view posted bills related to a task.
- `action_cancel_bill`: Method to cancel a bill.
