create database treasury_alumny;
\c treasury_alumny;

CREATE TABLE role(
   id SERIAL,
   name VARCHAR(30)  NOT NULL,
   PRIMARY KEY(id),
   UNIQUE(name)
);

CREATE TABLE users(
   id SERIAL,
   first_name VARCHAR(100)  NOT NULL,
   last_name VARCHAR(100)  NOT NULL,
   email VARCHAR(50)  NOT NULL,
   password TEXT NOT NULL,
   failed_login_attempts INTEGER NOT NULL,
   PRIMARY KEY(id),
   UNIQUE(email)
);

CREATE TABLE forecast(
   id SERIAL,
   months SMALLINT NOT NULL,
   years INTEGER NOT NULL,
   cash_inflow INTEGER NOT NULL,
   cash_outflow INTEGER NOT NULL,
   PRIMARY KEY(id)
);

CREATE TABLE company_type(
   id SERIAL,
   name VARCHAR(50)  NOT NULL,
   PRIMARY KEY(id),
   UNIQUE(name)
);

CREATE TABLE company(
   id SERIAL,
   name VARCHAR(100)  NOT NULL,
   registration_number VARCHAR(50)  NOT NULL,
   tax_identification_number VARCHAR(50)  NOT NULL,
   email VARCHAR(50)  NOT NULL,
   phone VARCHAR(50)  NOT NULL,
   address VARCHAR(50)  NOT NULL,
   website_url TEXT NOT NULL,
   created_at DATE NOT NULL,
   is_supplier BOOLEAN NOT NULL,
   company_type_id INTEGER NOT NULL,
   PRIMARY KEY(id),
   UNIQUE(name),
   UNIQUE(registration_number),
   UNIQUE(tax_identification_number),
   UNIQUE(email),
   UNIQUE(phone),
   UNIQUE(address),
   UNIQUE(website_url),
   FOREIGN KEY(company_type_id) REFERENCES company_type(id)
);

CREATE TABLE invoice(
   id SERIAL,
   invoice_number VARCHAR(50)  NOT NULL,
   invoice_date DATE NOT NULL,
   expected_payment_date DATE NOT NULL,
   actual_payment_date DATE,
   total_amount REAL NOT NULL,
   paid_amount REAL NOT NULL,
   status SMALLINT NOT NULL,
   company_id INTEGER NOT NULL,
   PRIMARY KEY(id),
   UNIQUE(invoice_number),
   FOREIGN KEY(company_id) REFERENCES company(id)
);

CREATE TABLE financial_transaction(
   id SERIAL,
   cash_inflow REAL NOT NULL,
   cash_outflow DOUBLE PRECISION NOT NULL,
   transaction_date DATE NOT NULL,
   description TEXT NOT NULL,
   user_id INTEGER NOT NULL,
   PRIMARY KEY(id),
   FOREIGN KEY(user_id) REFERENCES users(id)
);

CREATE TABLE client(
   id SERIAL,
   company_id INTEGER NOT NULL,
   PRIMARY KEY(id),
   FOREIGN KEY(company_id) REFERENCES company(id)
);

CREATE TABLE supplier(
   id SERIAL,
   company_id INTEGER NOT NULL,
   PRIMARY KEY(id),
   FOREIGN KEY(company_id) REFERENCES company(id)
);

CREATE TABLE payment(
   id SERIAL,
   payment_number VARCHAR(50)  NOT NULL,
   amount DOUBLE PRECISION NOT NULL,
   payment_date DATE NOT NULL,
   invoice_id INTEGER NOT NULL,
   PRIMARY KEY(id),
   UNIQUE(payment_number),
   FOREIGN KEY(invoice_id) REFERENCES invoice(id)
);

CREATE TABLE user_role(
   id SERIAL,
   role_id INTEGER,
   user_id INTEGER,
   PRIMARY KEY(id),
   FOREIGN KEY(role_id) REFERENCES role(id),
   FOREIGN KEY(user_id) REFERENCES users(id)
);
