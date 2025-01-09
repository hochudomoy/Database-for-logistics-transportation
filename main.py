import tkinter as tk
from tkinter import messagebox, END
from PIL import ImageTk, Image
from tkinter import ttk
import psycopg2
from psycopg2 import sql
from datetime import datetime
import random

def create_database():
    conn = psycopg2.connect(f'postgresql://{Config.LOGIN}:{Config.PASSWORD}@localhost/postgres')
    conn.set_isolation_level(psycopg2.extensions.ISOLATION_LEVEL_AUTOCOMMIT)
    cursor = conn.cursor()
    try:
        cursor.execute('CREATE DATABASE transport WITH OWNER human')
        conn = psycopg2.connect(f'postgresql://{Config.LOGIN}:{Config.PASSWORD}@localhost/transport')
        cursor = conn.cursor()
        cursor.execute(sql.SQL('''CREATE OR REPLACE PROCEDURE create_tables()0
                          LANGUAGE plpgsql AS $$
                          BEGIN
                          CREATE TABLE customer(organization_name TEXT PRIMARY KEY, phone TEXT, name TEXT, surname TEXT, mark NUMERIC(3,2) DEFAULT 5.0);
                          CREATE TABLE car(number VARCHAR(9) PRIMARY KEY, model TEXT, capacity NUMERIC(4,2), price NUMERIC(6,2), volume NUMERIC(3), year INTEGER, loading VARCHAR(7), refregerator VARCHAR(3));
                          CREATE TABLE driver(name TEXT, surname TEXT, patronymic TEXT, license NUMERIC(10,0) PRIMARY KEY, salary NUMERIC(15,2) DEFAULT 0.0, phone TEXT, address TEXT, mark NUMERIC(3,2) DEFAULT 5.0);
                          CREATE TABLE orders(id NUMERIC(4,0) PRIMARY KEY, car_number VARCHAR(9) REFERENCES car(number) ON DELETE SET NULL, license_number NUMERIC(10,0) REFERENCES driver(license) ON DELETE SET NULL, distance NUMERIC(6,2),name_organization TEXT REFERENCES customer(organization_name) ON DELETE SET NULL, order_date DATE, mark_driver NUMERIC(1,0), mark_customer NUMERIC(1,0), city_loading TEXT, city_unloading TEXT, implementation VARCHAR(3));
                          END;
                          $$;'''))
        conn.commit()
        cursor.execute('CALL create_tables()')
        conn.commit()
        cursor.execute(sql.SQL('''CREATE OR REPLACE PROCEDURE create_indxes()
                                  LANGUAGE plpgsql AS $$
                                  BEGIN
                                  CREATE INDEX idx_driver_surname ON driver(surname);
                                  CREATE INDEX idx_cities ON orders(city_loading,city_unloading);
                                  END;
                                  $$;'''))
        conn.commit()
        cursor.execute('CALL create_indxes()')
        conn.commit()
        cursor.execute(sql.SQL('''CREATE OR REPLACE PROCEDURE create_user(login TEXT, password TEXT)
                          LANGUAGE plpgsql AS $$
                          BEGIN
                          EXECUTE FORMAT('CREATE USER %I WITH PASSWORD %L',login,password);
                          GRANT INSERT, SELECT ON driver,orders,customer,car TO PUBLIC;
                          END;
                          $$;'''))
        conn.commit()
        cursor.execute(sql.SQL('''CREATE OR REPLACE PROCEDURE drop_user(login TEXT)
                                  LANGUAGE plpgsql AS $$
                                  BEGIN
                                  EXECUTE FORMAT('DROP USER %I;',login);
                                  END;
                                  $$;'''))
        conn.commit()
        cursor.execute(sql.SQL('''CREATE OR REPLACE PROCEDURE delete_tables(table_name TEXT)
                                  LANGUAGE plpgsql AS $$
                                  BEGIN
                                  EXECUTE FORMAT ('DELETE FROM %s', table_name);
                                  END;
                                  $$;'''))
        conn.commit()
        cursor.execute(sql.SQL('''CREATE OR REPLACE PROCEDURE delete_driver(p_phone TEXT)
                                  LANGUAGE plpgsql AS $$
                                  BEGIN
                                  DELETE FROM driver WHERE driver.phone=p_phone;
                                  END;
                                  $$;'''))
        conn.commit()
        cursor.execute(sql.SQL('''CREATE OR REPLACE PROCEDURE delete_car(p_number TEXT)
                                  LANGUAGE plpgsql AS $$
                                  BEGIN
                                  DELETE FROM car WHERE car.number=p_number;
                                  END;
                                  $$;'''))
        conn.commit()
        cursor.execute(sql.SQL('''CREATE OR REPLACE PROCEDURE insert_customer(org_name TEXT, phone_number TEXT, c_name TEXT, c_surname TEXT)
                                  LANGUAGE plpgsql AS $$
                                  BEGIN
                                  INSERT INTO customer(organization_name,phone,name,surname) VALUES(org_name,phone_number,c_name, c_surname);
                                  END;
                                  $$;'''))
        conn.commit()
        cursor.execute(sql.SQL('''CREATE OR REPLACE PROCEDURE insert_driver(d_name TEXT, d_surname TEXT, d_patronymic TEXT, d_license NUMERIC(10,0), d_phone TEXT, d_address TEXT)
                                  LANGUAGE plpgsql AS $$
                                  BEGIN
                                  INSERT INTO driver(name,surname,patronymic,license,phone,address) VALUES(d_name,d_surname,d_patronymic,d_license,d_phone,d_address);
                                  END;
                                  $$;'''))
        conn.commit()
        cursor.execute(sql.SQL('''CREATE OR REPLACE PROCEDURE insert_car(c_number VARCHAR(9), c_model TEXT, c_capacity NUMERIC(4,2), c_price NUMERIC(6,2), c_volume NUMERIC(5,2), c_year INTEGER, c_loading VARCHAR(7), c_refregerator VARCHAR(3))
                                  LANGUAGE plpgsql AS $$
                                  BEGIN
                                  INSERT INTO car(number,model,capacity,price,volume,year,loading,refregerator) VALUES(c_number,c_model,c_capacity,c_price,c_volume,c_year,c_loading,c_refregerator);
                                  END;
                                  $$;'''))
        conn.commit()
        cursor.execute(sql.SQL('''CREATE OR REPLACE PROCEDURE insert_orders(o_id NUMERIC(4,0), o_car_number VARCHAR(9), o_license_number NUMERIC(10,0), o_distance NUMERIC(6,2),o_name_organization TEXT, o_order_date DATE, o_mark_driver NUMERIC(3,2), o_mark_customer NUMERIC(3,2), o_city_loading TEXT, o_city_unloading TEXT, o_implementation VARCHAR(3))
                                  LANGUAGE plpgsql AS $$
                                  BEGIN
                                  INSERT INTO orders(id,car_number,license_number,distance,name_organization,order_date,mark_driver,mark_customer,city_loading,city_unloading,implementation) VALUES(o_id,o_car_number,o_license_number,o_distance,o_name_organization,o_order_date,o_mark_driver,o_mark_customer,o_city_loading,o_city_unloading,o_implementation);
                                  END;
                                  $$;'''))
        conn.commit()
        cursor.execute(sql.SQL('''CREATE OR REPLACE PROCEDURE update_phone_driver(d_license NUMERIC(10,0), d_phone TEXT)
                                  LANGUAGE plpgsql AS $$
                                  BEGIN
                                  UPDATE driver SET phone=d_phone WHERE license=d_license;
                                  END;
                                  $$;'''))
        conn.commit()
        cursor.execute(sql.SQL('''CREATE OR REPLACE PROCEDURE update_address_driver(d_license NUMERIC(10,0), d_address TEXT)
                                  LANGUAGE plpgsql AS $$
                                  BEGIN
                                  UPDATE driver SET address=d_address WHERE license=d_license;
                                  END;
                                  $$;'''))
        conn.commit()
        cursor.execute(sql.SQL('''CREATE OR REPLACE PROCEDURE update_contact_company(company TEXT, c_name TEXT,c_surname TEXT)
                                  LANGUAGE plpgsql AS $$
                                  BEGIN
                                  UPDATE customer SET name=c_name, surname=c_surname WHERE organization_name=company;
                                  END;
                                  $$;'''))
        conn.commit()
        cursor.execute(sql.SQL('''CREATE OR REPLACE PROCEDURE update_status_orders(o_id NUMERIC(4,0),d_mark NUMERIC(1,0),c_mark NUMERIC(1,0))
                                  LANGUAGE plpgsql AS $$
                                  BEGIN
                                  UPDATE orders SET implementation='ДА', mark_driver=d_mark,mark_customer=c_mark WHERE id=o_id;
                                  END;
                                  $$;'''))
        conn.commit()
        cursor.execute(sql.SQL('''CREATE OR REPLACE FUNCTION get_driver( grad NUMERIC(3,2))
                                  RETURNS TABLE(name TEXT, surname TEXT, patronymic TEXT, mark NUMERIC(3,2)) AS $$
                                  BEGIN
                                  RETURN QUERY (SELECT driver.name, driver.surname, driver.patronymic, driver.mark FROM driver WHERE driver.mark <= grad ORDER BY driver.mark DESC);
                                  END;$$ LANGUAGE plpgsql;'''))
        conn.commit()

        cursor.execute(sql.SQL('''CREATE OR REPLACE FUNCTION get_customer(c_mark NUMERIC(3,2))
                                    RETURNS TABLE(organization_name TEXT, phone TEXT, name TEXT, surname TEXT, mark NUMERIC(3,2)) AS $$
                                    BEGIN 
                                    RETURN QUERY (SELECT customer.organization_name, customer.phone, customer.name, customer.surname, customer.mark FROM customer WHERE customer.mark >= c_mark ORDER BY customer.mark DESC);
                                    END;$$ LANGUAGE plpgsql;'''))
        conn.commit()

        cursor.execute(sql.SQL('''CREATE OR REPLACE FUNCTION get_customer_name(c_name TEXT)
                                    RETURNS TABLE(organization_name TEXT, phone TEXT,name TEXT, surname TEXT) AS $$
                                    BEGIN 
                                    RETURN QUERY (SELECT customer.organization_name, customer.phone, customer.name, customer.surname FROM customer WHERE customer.organization_name = c_name);
                                    END;$$ LANGUAGE plpgsql;'''))
        conn.commit()

        cursor.execute(sql.SQL('''CREATE OR REPLACE FUNCTION get_driver_orders(d_surname TEXT)
                                            RETURNS TABLE(id NUMERIC(4,0), surname TEXT, car_number VARCHAR(9), distance NUMERIC(6,2), order_date DATE) AS $$
                                            BEGIN 
                                            RETURN QUERY (SELECT orders.id, driver.surname, orders.car_number, orders.distance, orders.order_date FROM orders INNER JOIN driver ON orders.license_number = driver.license AND driver.surname = d_surname AND orders.implementation = 'ДА' ORDER BY orders.id);
                                            END;$$ LANGUAGE plpgsql;'''))
        conn.commit()

        cursor.execute(sql.SQL('''CREATE OR REPLACE FUNCTION get_car_orders(car_numbers TEXT)
                                            RETURNS TABLE(id NUMERIC(4,0), car_number VARCHAR(9), model TEXT, distance NUMERIC(6,2), order_date DATE) AS $$
                                            BEGIN 
                                            RETURN QUERY (SELECT orders.id, car.number, car.model, orders.distance, orders.order_date FROM orders JOIN car ON orders.car_number = car.number WHERE car.number = car_numbers ORDER BY orders.id);
                                            END;$$ LANGUAGE plpgsql;'''))
        conn.commit()

        cursor.execute(sql.SQL('''CREATE OR REPLACE FUNCTION get_order_status(status TEXT)
                                            RETURNS TABLE(id NUMERIC(4,0), car_number VARCHAR(9), name TEXT, surname TEXT, name_organization TEXT, order_date DATE, implementation VARCHAR(3) ) AS $$
                                            BEGIN 
                                            RETURN QUERY (SELECT orders.id, orders.car_number,  driver.name, driver.surname, orders.name_organization,  orders.order_date, orders.implementation  FROM orders JOIN driver ON orders.license_number = driver.license WHERE orders.implementation = status ORDER BY orders.id);
                                            END;$$ LANGUAGE plpgsql;'''))
        conn.commit()

        cursor.execute(sql.SQL('''CREATE OR REPLACE FUNCTION get_order_cities(load_city TEXT, unload_city TEXT)
                                            RETURNS TABLE(id NUMERIC(4,0), surname TEXT, name_organization TEXT, city_loading TEXT, city_unloading TEXT,  implementation VARCHAR(3) ) AS $$
                                            BEGIN 
                                            RETURN QUERY (SELECT orders.id, driver.surname, orders.name_organization, orders.city_loading, orders.city_unloading, orders.implementation  FROM orders JOIN driver ON driver.license = orders.license_number WHERE orders.city_loading = load_city AND orders.city_unloading = unload_city ORDER BY orders.implementation DESC);
                                            END;$$ LANGUAGE plpgsql;'''))
        conn.commit()

        cursor.execute(sql.SQL('''CREATE OR REPLACE FUNCTION get_specific_car(cap NUMERIC(4,2), vol NUMERIC(5,2), ye INTEGER, type VARCHAR(7), refreg VARCHAR(3))
                                            RETURNS TABLE(number VARCHAR(9), model TEXT, capacity NUMERIC(4,2), volume NUMERIC(5,2), year INTEGER) AS $$
                                            BEGIN 
                                            RETURN QUERY (SELECT car.number, car.model, car.capacity, car.volume, car.year FROM car WHERE car.capacity > cap AND car.volume > vol AND car.year > ye AND car.loading = type AND car.refregerator = refreg ORDER BY car.capacity, car.volume, car.year);
                                            END;$$ LANGUAGE plpgsql;'''))
        conn.commit()

        #ПОЛУЧЕНИЕ ВСЕЙ ТАБЛИЦЫ

        cursor.execute(sql.SQL('''CREATE OR REPLACE FUNCTION get_all_customers()
                                    RETURNS TABLE(organization_name TEXT, phone TEXT, name TEXT, surname TEXT, mark NUMERIC(3,2)) AS $$
                                    BEGIN 
                                    RETURN QUERY (SELECT customer.organization_name, customer.phone, customer.name, customer.surname, customer.mark FROM customer ORDER BY customer.organization_name);
                                    END;$$ LANGUAGE plpgsql;'''))
        conn.commit()

        cursor.execute(sql.SQL('''CREATE OR REPLACE FUNCTION get_all_cars()
                                    RETURNS TABLE(number VARCHAR(9), model TEXT, capacity NUMERIC(4,2), price NUMERIC(6,2), volume NUMERIC(5,2), year INTEGER, loading VARCHAR(7), refregerator VARCHAR(3)) AS $$
                                    BEGIN 
                                    RETURN QUERY (SELECT car.number, car.model, car.capacity, car.price, car.volume, car.year, car.loading, car.refregerator FROM car ORDER BY car.capacity, car.volume, car.year);
                                    END;$$ LANGUAGE plpgsql;'''))
        conn.commit()

        cursor.execute(sql.SQL('''CREATE OR REPLACE FUNCTION get_all_drivers()
                                    RETURNS TABLE(name TEXT, surname TEXT, patronymic TEXT, license NUMERIC(10,0), salary NUMERIC(8,2), phone TEXT, address TEXT, mark NUMERIC(3,2)) AS $$
                                    BEGIN 
                                    RETURN QUERY (SELECT driver.name, driver.surname, driver.patronymic, driver.license, driver.salary, driver.phone, driver.address, driver.mark FROM driver ORDER BY driver.mark DESC);
                                    END;$$ LANGUAGE plpgsql;'''))
        conn.commit()

        cursor.execute(sql.SQL('''CREATE OR REPLACE FUNCTION get_all_orders()
                                    RETURNS TABLE(id NUMERIC(4,0), car_number VARCHAR(9), license_number NUMERIC(10,0), distance NUMERIC(6,2), name_organization TEXT, order_date DATE, mark_driver NUMERIC(3,2), mark_customer NUMERIC(3,2), city_loading TEXT, city_unloading TEXT, implementation VARCHAR(3)) AS $$
                                    BEGIN 
                                    RETURN QUERY (SELECT orders.id, orders.car_number, orders.license_number, orders.distance, orders.name_organization, orders.order_date, orders.mark_driver, orders.mark_customer, orders.city_loading, orders.city_unloading, orders.implementation FROM orders ORDER BY orders.id);
                                    END;$$ LANGUAGE plpgsql;'''))
        conn.commit()
        cursor.execute(sql.SQL('''CREATE OR REPLACE FUNCTION find_license()
                                    RETURNS TABLE(license NUMERIC (10,0)) AS $$
                                    BEGIN 
                                    RETURN QUERY (SELECT driver.license FROM driver);
                                    END;$$ LANGUAGE plpgsql;'''))
        conn.commit()
        cursor.execute(sql.SQL('''CREATE OR REPLACE FUNCTION find_customer()
                                        RETURNS TABLE(organization_name TEXT) AS $$
                                        BEGIN 
                                        RETURN QUERY (SELECT customer.organization_name FROM customer);
                                        END;$$ LANGUAGE plpgsql;'''))
        conn.commit()
        cursor.execute(sql.SQL('''CREATE OR REPLACE FUNCTION find_car()
                                        RETURNS TABLE(number VARCHAR(8)) AS $$
                                        BEGIN 
                                        RETURN QUERY (SELECT car.number FROM car);
                                        END;$$ LANGUAGE plpgsql;'''))
        conn.commit()
        cursor.execute(sql.SQL('''CREATE OR REPLACE FUNCTION find_unimplemented_order()
                                        RETURNS TABLE(id NUMERIC(4,0)) AS $$
                                        BEGIN 
                                        RETURN QUERY (SELECT orders.id FROM orders where orders.implementation='НЕТ');
                                        END;$$ LANGUAGE plpgsql;'''))
        conn.commit()

        cursor.execute(sql.SQL('''CREATE OR REPLACE FUNCTION find_driver_number()
                                        RETURNS TABLE(phone TEXT, surname TEXT) AS $$
                                        BEGIN 
                                        RETURN QUERY (SELECT driver.phone,driver.surname FROM driver);
                                        END;$$ LANGUAGE plpgsql;'''))
        conn.commit()

        cursor.execute(sql.SQL('''CREATE OR REPLACE FUNCTION change_marks_driver()  
                                                RETURNS TRIGGER AS $$
                                                DECLARE
                                                    avg_mark_driver NUMERIC;
                                                BEGIN 
                                                    IF NEW.implementation = 'ДА' THEN
                                                        SELECT AVG(orders.mark_driver) INTO avg_mark_driver
                                                        FROM orders
                                                        WHERE orders.license_number = NEW.license_number AND orders.implementation = NEW.implementation;

                                                        UPDATE driver
                                                        SET mark = avg_mark_driver
                                                        WHERE driver.license = NEW.license_number;
                                                    END IF;
                                                    RETURN NEW;
                                                END;$$ LANGUAGE plpgsql;
                                                
                                                
                                                
                                                CREATE OR REPLACE FUNCTION change_marks_customer()  
                                                        RETURNS TRIGGER AS $$
                                                        DECLARE
                                                            avg_mark_customer NUMERIC;
                                                        BEGIN 
                                                            IF NEW.implementation = 'ДА' THEN
                                                                SELECT AVG(orders.mark_customer) INTO avg_mark_customer
                                                                FROM orders
                                                                WHERE orders.name_organization = NEW.name_organization AND orders.implementation = NEW.implementation;

                                                                UPDATE customer
                                                                SET mark = avg_mark_customer
                                                                WHERE customer.organization_name = NEW.name_organization;
                                                            END IF;
                                                            RETURN NEW;
                                                END;$$ LANGUAGE plpgsql;'''))

        conn.commit()

        cursor.execute(sql.SQL('''CREATE OR REPLACE PROCEDURE create_trigger_d()
                                                LANGUAGE plpgsql AS $$
                                                BEGIN
                                                CREATE TRIGGER change_marks_driver
                                                AFTER INSERT OR UPDATE ON orders
                                                FOR EACH ROW
                                                EXECUTE FUNCTION change_marks_driver();
                                                END;$$;'''))

        conn.commit()

        cursor.execute('CALL create_trigger_d()')
        conn.commit()

        cursor.execute(sql.SQL('''CREATE OR REPLACE PROCEDURE create_trigger_c()
                                        LANGUAGE plpgsql AS $$
                                        BEGIN
                                        CREATE TRIGGER change_marks_customer
                                        AFTER INSERT OR UPDATE ON orders
                                        FOR EACH ROW
                                        EXECUTE FUNCTION change_marks_customer();
                                        END;$$;'''))

        conn.commit()

        cursor.execute('CALL create_trigger_c()')
        conn.commit()

        cursor.execute(sql.SQL('''CREATE OR REPLACE FUNCTION earned_money()  
                                                RETURNS TRIGGER AS $$
                                                DECLARE
                                                    money NUMERIC;
                                                BEGIN 
                                                    IF NEW.implementation = 'ДА' THEN
                                                        SELECT SUM(orders.distance * car.price) INTO money
                                                        FROM orders
                                                        JOIN car ON orders.car_number = car.number
                                                        WHERE orders.license_number = NEW.license_number AND orders.implementation = NEW.implementation; 
                                                        UPDATE driver
                                                        SET salary = money
                                                        WHERE driver.license = NEW.license_number;
                                                    END IF;
                                                    RETURN NEW;
                                                END;$$ LANGUAGE plpgsql;'''))

        conn.commit()
        cursor.execute(sql.SQL('''CREATE OR REPLACE PROCEDURE create_trigger_money()
                                        LANGUAGE plpgsql AS $$
                                        BEGIN
                                        CREATE TRIGGER earned_money
                                        AFTER INSERT OR UPDATE ON orders
                                        FOR EACH ROW
                                        EXECUTE FUNCTION earned_money();
                                        END;$$;'''))
        conn.commit()

        cursor.execute('CALL create_trigger_money()')
        conn.commit()
        cursor.close()
        conn.close()

    except:
        cursor.close()
        conn.close()

def drop_database():
    conn = psycopg2.connect(f'postgresql://{Config.LOGIN}:{Config.PASSWORD}@localhost/postgres')
    conn.set_isolation_level(psycopg2.extensions.ISOLATION_LEVEL_AUTOCOMMIT)
    cursor = conn.cursor()
    try:cursor.execute('DROP DATABASE transport;')
    except:messagebox.showerror('Oшибка', 'Ошибка! Невозможно удалить базу данных!')
    cursor.close()
    conn.close()
class Config:
    LOGIN = "human"
    PASSWORD = "secure"


class LoginFrame(tk.Frame):
    def __init__(self, master, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        LoginFrame.config(self, background='#c5d0e6')
        self.login_label = tk.Label(self, text='ЛОГИН', font='algerian', background='#c5d0e6')
        self.login = tk.Entry(self)
        self.password_label = tk.Label(self, text='ПАРОЛЬ', font='algerian', background='#c5d0e6')
        self.password = tk.Entry(self)

        self.login.insert(0, Config.LOGIN)
        self.login_btn = tk.Button(self, text='ВОЙТИ', font='algerian', fg='white')

        self.login_btn.config(bg='green', activebackground="#35654d")
        self.login_btn.config(command=self._login_command)

        self.login_label.pack()
        self.login.pack()
        self.password_label.pack()
        self.password.pack()
        self.login_btn.pack(fill='x', padx=300, pady=5)
        image = Image.open("car.jpg")
        self.img = ImageTk.PhotoImage(image)
        self.img_label = tk.Label(self, image=self.img)
        self.img_label.pack()

    def _login_command(self):
        if (self.login.get() == 'human' and self.password.get() == 'secure'):
            Config.LOGIN = self.login.get()
            Config.PASSWORD = self.password.get()
            messagebox.showinfo('УСПЕХ', 'Вы успешно вошли')
            self.forget()
            MainFrame(self.master).pack()
            create_database()
        else:
            try:
                conn = psycopg2.connect(f'postgresql://human:secure@localhost/transport')
                cursor = conn.cursor()
                try:
                    cursor.execute(sql.SQL('''CALL create_user(%s,%s)'''), (self.login.get(), self.password.get()), )
                    conn.commit()
                    Config.LOGIN = self.login.get()
                    Config.PASSWORD = self.password.get()
                    self.forget()
                    MainFrame(self.master).pack()
                except:
                    try:
                        Config.LOGIN = self.login.get()
                        Config.PASSWORD = self.password.get()
                        conn = psycopg2.connect(f'postgresql://{Config.LOGIN}:{Config.PASSWORD}@localhost/transport')
                        self.forget()
                        MainFrame(self.master).pack()
                    except:
                        messagebox.showerror('Oшибка', 'Неверный логин или пароль')
            except:
                messagebox.showerror('Oшибка', 'База данных не существует. Войдите от имени администратора')


class MainFrame(tk.Frame):
    def __init__(self, master, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        MainFrame.config(self, background='#627182')
        self.action_label = tk.Label(self, text='Что вы хотите сделать?', background='#627182',
                                     font=('algerian', 16, 'bold'), foreground='#EAF0CE')
        self.action_label.pack(fill='x', padx=0, pady=20)
        self.add_btn = tk.Button(self, text='Добавить данные', background='#A5D0D9', font=('algerian', 14))
        self.remove_btn = tk.Button(self, text='Удалить данные', background='#A5C0D9', font=('algerian', 14))
        self.add_btn.pack(fill='x', padx=0, pady=10)
        if (Config.LOGIN == 'human' and Config.PASSWORD == 'secure'): self.remove_btn.pack(fill='x', padx=0, pady=15)
        self.add_btn.config(command=self._add_command)
        self.remove_btn.config(command=self._remove_command)
        self.find_btn = tk.Button(self, text="Найти", background='#A5AFD9', font=('algerian', 14))
        self.find_btn.pack(fill='x', padx=0, pady=10)
        self.find_btn.config(command=self._find_command)
        self.update_btn = tk.Button(self, text="Изменить данные", background='#99A6D9',
                                    font=('algerian', 14))
        if (Config.LOGIN == 'human' and Config.PASSWORD == 'secure'): self.update_btn.pack(fill='x', padx=0, pady=15)
        self.update_btn.config(command=self._update_command)
        self.content_btn = tk.Button(self, text="Посмотреть содержание таблиц", background='#99A6D9',
                                     font=('algerian', 14))
        self.content_btn.pack(fill='x', padx=0, pady=10)
        self.content_btn.config(command=self._content_command)
        self.remove_user_btn = tk.Button(self, text="Удалить и выйти", background='#A5AFD9', font=('algerian', 14))
        if (Config.LOGIN != 'human' or Config.PASSWORD != 'secure'): self.remove_user_btn.pack(fill='x', padx=0,
                                                                                               pady=15)
        self.remove_user_btn.config(command=self._remove_user_command)
        self.cat_btn=tk.Button(self, text="Посмотреть на котика", background='#99A6D9',
                                     font=('algerian', 14))
        self.cat_btn.pack(anchor="se", padx=[400,10], pady=[300,10])
        self.cat_btn.config(command=self._cat_command)

    def _add_command(self):
        self.forget()
        AddFrame(self.master).pack()

    def _remove_command(self):
        self.forget()
        RemoveFrame(self.master).pack()

    def _find_command(self):
        self.forget()
        FindFrame(self.master).pack()

    def _update_command(self):
        self.forget()
        UpdateFrame(self.master).pack()

    def _content_command(self):
        self.forget()
        ContentFrame(self.master).pack()
    def _cat_command(self):
        self.forget()
        CatFrame(self.master).pack()

    def _remove_user_command(self):
        if (messagebox.askyesno("Предупреждение", 'Вы уверены, что хотите удалить пользователя?')):
            conn = psycopg2.connect(f'postgresql://human:secure@localhost/transport')
            cursor = conn.cursor()
            cursor.execute(sql.SQL('''CALL drop_user(%s)'''), (Config.LOGIN,))
            conn.commit()
            self.forget()
            LoginFrame(self.master).pack()


class AddFrame(tk.Frame):
    def __init__(self, master, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        AddFrame.config(self, background='#627182')
        self.action_label = tk.Label(self, text='Что вы хотите сделать?', background='#627182',
                                     font=('algerian', 16, "bold"), foreground='#EAF0CE')
        self.driver_btn = tk.Button(self, text='Добавить нового водителя', background='#96DAFA', font=('algerian', 14))
        self.car_btn = tk.Button(self, text='Добавить новую машину', background='#ADCDE0', font=('algerian', 14))
        self.customer_btn = tk.Button(self, text='Добавить нового заказчика', background='#86B8EF',
                                      font=('algerian', 14))
        self.order_btn = tk.Button(self, text='Добавить новый заказ', background='#8CBAFA', font=('algerian', 14))
        self.back_btn = tk.Button(self, text='Назад', background='#7B7AF0', font=('algerian', 14))
        self.action_label.pack(fill='x', padx=200, pady=15)
        self.car_btn.pack(fill='x', padx=200, pady=15)
        self.driver_btn.pack(fill='x', padx=200, pady=15)
        self.customer_btn.pack(fill='x', padx=200, pady=15)
        self.order_btn.pack(fill='x', padx=200, pady=15)
        self.back_btn.pack(fill='x', padx=200, pady=15)
        self.driver_btn.config(command=self._add_driver_command)
        self.car_btn.config(command=self._add_car_command)
        self.customer_btn.config(command=self._add_customer_command)
        self.order_btn.config(command=self._add_order_command)
        self.back_btn.config(command=self._back_command)


    def _back_command(self):
        self.forget()
        MainFrame(self.master).pack()

    def _add_driver_command(self):
        self.forget()
        AddDriver(self.master).pack()

    def _add_car_command(self):
        self.forget()
        AddCar(self.master).pack()

    def _add_customer_command(self):
        self.forget()
        AddCustomer(self.master).pack()

    def _add_order_command(self):
        self.forget()
        AddOrder(self.master).pack()


class AddDriver(tk.Frame):
    def __init__(self, master, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        AddDriver.config(self, background='#627182')
        self.name_label = tk.Label(self, text='Введите имя', background='#627182', font=('algerian', 16, 'bold'),
                                   foreground='#EAF0CE')
        self.surname_label = tk.Label(self, text='Введите фамилию', background='#627182', font=('algerian', 16, 'bold'),
                                      foreground='#EAF0CE')
        self.patronymic_label = tk.Label(self, text='Введите отчество', background='#627182',
                                         font=('algerian', 16, 'bold'), foreground='#EAF0CE')
        self.license_label = tk.Label(self, text='Введите номер водительского удостоверения', background='#627182',
                                      font=('algerian', 16, 'bold'), foreground='#EAF0CE')
        self.phone_label = tk.Label(self, text='Введите номер телефона', background='#627182',
                                    font=('algerian', 16, 'bold'), foreground='#EAF0CE')
        self.address_label = tk.Label(self, text='Введите адрес', background='#627182', font=('algerian', 16, 'bold'),
                                      foreground='#EAF0CE')
        self.name = tk.Entry(self, font=('arial', 12))
        self.surname = tk.Entry(self, font=('arial', 12))
        self.patronymic = tk.Entry(self, font=('arial', 12))
        self.license = tk.Entry(self, font=('arial', 12))
        self.phone = tk.Entry(self, font=('arial', 12))
        self.address = tk.Entry(self, font=('arial', 12))
        self.name_label.pack()
        self.name.pack(fill='x', padx=250, pady=5)
        self.surname_label.pack()
        self.surname.pack(fill='x', padx=250, pady=5)
        self.patronymic_label.pack()
        self.patronymic.pack(fill='x', padx=250, pady=5)
        self.license_label.pack()
        self.license.pack(fill='x', padx=250, pady=5)
        self.phone_label.pack()
        self.phone.pack(fill='x', padx=250, pady=5)
        self.address_label.pack()
        self.address.pack(fill='both', padx=250, pady=5)
        self.add_btn = tk.Button(self, text='Добавить')
        self.add_btn.pack(fill='x', padx=300, pady=5)
        self.add_btn.config(command=self._add_command, background='#A2E8F0', font=('algerian', 14))
        self.back_btn = tk.Button(self, text='Назад', background='#ADBBE0', font=('algerian', 14))
        self.back_btn.pack(fill='x', padx=300, pady=5)
        self.back_btn.config(command=self._back_command)

    def _back_command(self):
        self.forget()
        AddFrame(self.master).pack()

    def _add_command(self):
        if (self.license.get().isdigit() and len(self.license.get()) == 10):
            if self.name.get() != '':
                if self.surname.get() != '':
                    conn = psycopg2.connect(f'postgresql://{Config.LOGIN}:{Config.PASSWORD}@localhost/transport')
                    cursor = conn.cursor()
                    try:
                        cursor.execute(sql.SQL('CALL insert_driver(%s,%s,%s,%s,%s,%s);'), (
                            self.name.get(), self.surname.get(), self.patronymic.get(), float(self.license.get()),
                            self.phone.get(),
                            self.address.get()))
                        conn.commit()
                        messagebox.showinfo('УСПЕХ', 'Вы успешно добавили водителя')
                        self.forget()
                        AddFrame(self.master).pack()
                    except:
                        messagebox.showerror('Oшибка',
                                             'Ошибка! Убедитесь, что водитель с таким номером удостоверения не существует!')
                else:
                    messagebox.showerror('Oшибка', 'Введите фамилию водителя')
            else:
                messagebox.showerror('Oшибка', 'Введите имя водителя')
        else:
            messagebox.showerror('Oшибка', 'Неверно введён номер водительского удостоверения')


class AddCar(tk.Frame):
    def __init__(self, master, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        AddCar.config(self, background='#627182')
        self.number_label = tk.Label(self, text='Введите госномер в формате \n номер + номер региона А000АА00',
                                     background='#627182', font=('algerian', 16, 'bold'), foreground='#EAF0CE')
        self.model_label = tk.Label(self, text='Введите название модели', background='#627182', font=('algerian', 16, 'bold'),
                                    foreground='#EAF0CE')
        self.capacity_label = tk.Label(self, text='Введите грузоподъёмность в тоннах', background='#627182',
                                       font=('algerian', 16, 'bold'), foreground='#EAF0CE')
        self.price_label = tk.Label(self, text='Введите цену за километр', background='#627182',
                                    font=('algerian', 16, 'bold'), foreground='#EAF0CE')
        self.volume_label = tk.Label(self, text='Введите объём в кубических метрах', background='#627182',
                                     font=('algerian', 16, 'bold'),
                                     foreground='#EAF0CE')
        self.year_label = tk.Label(self, text='Введите год выпуска машины', background='#627182',
                                   font=('algerian', 16, 'bold'), foreground='#EAF0CE')
        self.loading_label = tk.Label(self, text='Выберите тип погрузки', background='#627182',
                                      font=('algerian', 16, 'bold'), foreground='#EAF0CE')
        self.number = tk.Entry(self, font=('algerian', 12))
        self.model = tk.Entry(self, font=('algerian', 12))
        self.capacity = tk.Entry(self, font=('algerian', 12))
        self.volume = tk.Entry(self, font=('algerian', 12))
        self.price = tk.Entry(self, font=('algerian', 12))
        self.year = tk.Entry(self, font=('algerian', 12))
        self.loading = ttk.Combobox(self, state="readonly", values=["Боковая", "Верхняя", "Задняя"])
        self.var = tk.StringVar()
        self.var.set("НЕТ")
        self.fridge = tk.Checkbutton(self, text="Наличие рефрежератора", variable=self.var, onvalue="ДА",
                                     offvalue="НЕТ", bg='#627182', font=('algerian', 16, 'bold'), foreground='#EAF0CE',
                                     selectcolor='black')
        self.number_label.pack()
        self.number.pack(fill='x', padx=250, pady=5)
        self.model_label.pack()
        self.model.pack(fill='x', padx=250, pady=5)
        self.capacity_label.pack()
        self.capacity.pack(fill='x', padx=250, pady=5)
        self.price_label.pack()
        self.price.pack(fill='x', padx=250, pady=5)
        self.volume_label.pack()
        self.volume.pack(fill='x', padx=250, pady=5)
        self.year_label.pack()
        self.year.pack(fill='x', padx=250, pady=5)
        self.loading_label.pack()
        self.loading.pack(fill='x', padx=250, pady=5)

        self.fridge.pack()
        self.add_btn = tk.Button(self, text='Добавить', background='#A2E8F0', font=('algerian', 14))
        self.add_btn.pack(fill='x', padx=300, pady=5)
        self.add_btn.config(command=self._add_command)
        self.back_btn = tk.Button(self, text='Назад', background='#ADBBE0', font=('algerian', 14))
        self.back_btn.pack(fill='x', padx=300, pady=5)
        self.back_btn.config(command=self._back_command)

    def _back_command(self):
        self.forget()
        AddFrame(self.master).pack()

    def _add_command(self):
        if len(self.number.get()) == 8 or len(self.number.get()) == 9:
            try:
                if float(self.capacity.get()) < 100:
                    try:
                        if float(self.price.get()) < 10000:
                            if self.volume.get().isdigit() and int(self.volume.get()) < 1000:
                                if self.year.get().isdigit() and len(self.year.get()) == 4 and 1800<=int(
                                        self.year.get()) <=2024:
                                    if self.loading.get() != '':
                                        if self.model.get() != '':
                                            conn = psycopg2.connect(
                                                f'postgresql://{Config.LOGIN}:{Config.PASSWORD}@localhost/transport')
                                            cursor = conn.cursor()
                                            try:
                                                cursor.execute(sql.SQL('CALL insert_car(%s,%s,%s,%s,%s,%s,%s,%s);'),
                                                               (self.number.get(), self.model.get(),
                                                                float(self.capacity.get()),
                                                                float(self.price.get()),
                                                                float(self.volume.get()), int(self.year.get()),
                                                                self.loading.get(),
                                                                self.var.get(),))
                                                conn.commit()
                                                messagebox.showinfo('УСПЕХ', 'Вы успешно добавили машину')
                                                self.forget()
                                                AddFrame(self.master).pack()
                                            except:
                                                messagebox.showerror('Oшибка',
                                                                     'Ошибка! Убедитесь, что машины с таким номером не существует!')
                                        else:
                                            messagebox.showerror('Oшибка', 'Ошибка!Не указана модель машины!')
                                    else:
                                        messagebox.showerror('Oшибка', 'Ошибка!Не выбран тип погрузки!')
                                else:
                                    messagebox.showerror('Oшибка', 'Ошибка!Неправильно введен год машины!')
                            else:
                                messagebox.showerror('Oшибка', 'Ошибка!Неправильно введен объём машины!')
                        else:
                            messagebox.showerror('Oшибка', 'Ошибка!Неправильно введена цена за километр!')
                    except:
                        messagebox.showerror('Oшибка', 'Ошибка!Неправильно введена цена за километр!')
                else:
                    messagebox.showerror('Oшибка', 'Ошибка!Неправильно введена грузоподъёмность!')
            except:
                messagebox.showerror('Oшибка', 'Ошибка!Неправильно введена грузоподъёмность!')
        else:
            messagebox.showerror('Oшибка', 'Ошибка!Неправильно введен номер машины!')


class AddCustomer(tk.Frame):
    def __init__(self, master, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        AddCustomer.config(self, background='#627182')
        self.company_label = tk.Label(self, text='Введите название компании', background='#627182',
                                      font=('algerian', 16, 'bold'), foreground='#EAF0CE')
        self.phone_label = tk.Label(self, text='Введите номер телефона', background='#627182',
                                    font=('algerian', 16, 'bold'), foreground='#EAF0CE')
        self.name_label = tk.Label(self, text='Введите имя контактного лица', background='#627182',
                                   font=('algerian', 16, 'bold'), foreground='#EAF0CE')
        self.surname_label = tk.Label(self, text='Введите фамилию контактного лица', background='#627182',
                                      font=('algerian', 16, 'bold'), foreground='#EAF0CE')
        self.company = tk.Entry(self, font=('arial', 12))
        self.phone = tk.Entry(self, font=('arial', 12))
        self.name = tk.Entry(self, font=('arial', 12))
        self.surname = tk.Entry(self, font=('arial', 12))
        self.company_label.pack()
        self.company.pack(fill='x', padx=250, pady=5)
        self.phone_label.pack()
        self.phone.pack(fill='x', padx=250, pady=5)
        self.name_label.pack()
        self.name.pack(fill='x', padx=250, pady=5)
        self.surname_label.pack()
        self.surname.pack(fill='x', padx=250, pady=5)

        self.add_btn = tk.Button(self, text='Добавить', background='#A2E8F0', font=('algerian', 14))
        self.add_btn.pack(fill='x', padx=300, pady=5)
        self.add_btn.config(command=self._add_command)
        self.back_btn = tk.Button(self, text='Назад', background='#ADBBE0', font=('algerian', 14))
        self.back_btn.pack(fill='x', padx=300, pady=5)
        self.back_btn.config(command=self._back_command)

    def _back_command(self):
        self.forget()
        AddFrame(self.master).pack()

    def _add_command(self):
        if self.company.get() != '':
            conn = psycopg2.connect(f'postgresql://{Config.LOGIN}:{Config.PASSWORD}@localhost/transport')
            cursor = conn.cursor()
            try:
                cursor.execute(sql.SQL('CALL insert_customer(%s,%s,%s,%s);'),
                               (self.company.get(), self.phone.get(), self.name.get(), self.surname.get(),))
                conn.commit()
                messagebox.showinfo('УСПЕХ', 'Вы успешно добавили заказчика')
                self.forget()
                AddFrame(self.master).pack()
            except:
                messagebox.showerror('Oшибка', 'Ошибка! Убедитесь, что компания с таким названием не существует!')
        else:
            messagebox.showerror('Oшибка', 'Ошибка!Неправильно введено название компании!')


class AddOrder(tk.Frame):
    def __init__(self, master, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        AddOrder.config(self, background='#627182')
        self.id_label = tk.Label(self, text='Введите ID заказа', background='#627182', font=('algerian', 14, 'bold'),
                                 foreground='#EAF0CE')
        self.number_label = tk.Label(self, text='Введите госномер автомобиля', background='#627182',
                                     font=('algerian', 12, 'bold'), foreground='#EAF0CE')
        self.license_label = tk.Label(self, text='Введите номер водительского удостоверения водителя',
                                      background='#627182', font=('algerian', 12, 'bold'), foreground='#EAF0CE')
        self.distance_label = tk.Label(self, text='Введите расстояние в километрах', background='#627182',
                                       font=('algerian', 12, 'bold'), foreground='#EAF0CE')
        self.company_label = tk.Label(self, text='Введите название компании', background='#627182',
                                      font=('algerian', 12, 'bold'), foreground='#EAF0CE')
        self.date_label = tk.Label(self, text='Введите дату выполнения заказа в формате YYYY-MM-DD',
                                   background='#627182',
                                   font=('algerian', 12, 'bold'), foreground='#EAF0CE')
        self.city1_label = tk.Label(self, text='Введите город погрузки', background='#627182',
                                    font=('algerian', 12, 'bold'), foreground='#EAF0CE')
        self.city2_label = tk.Label(self, text='Введите город выгрузки', background='#627182',
                                    font=('algerian', 12, 'bold'), foreground='#EAF0CE')
        self.mark_d_label = tk.Label(self, text='Введите оценку водителя (если заказ не выполнен, введите 5)',
                                     background='#627182',
                                     font=('algerian', 12, 'bold'), foreground='#EAF0CE')
        self.mark_c_label = tk.Label(self, text='Введите оценку заказчика (если заказ не выполнен, введите 5)',
                                     background='#627182',
                                     font=('algerian', 12, 'bold'), foreground='#EAF0CE')
        self.execution_label = tk.Label(self, text='Заказ выполнен?', background='#627182',
                                        font=('algerian', 12, 'bold'), foreground='#EAF0CE')
        self.id = tk.Entry(self, font=('arial', 9))
        conn = psycopg2.connect(f'postgresql://{Config.LOGIN}:{Config.PASSWORD}@localhost/transport')
        cursor = conn.cursor()
        cursor.callproc('find_car')
        self.data = cursor.fetchall()
        self.number = ttk.Combobox(self, state="readonly", values=self.data)
        cursor.callproc('find_license')
        self.data1 = cursor.fetchall()
        self.license = ttk.Combobox(self, state="readonly", values=self.data1)
        self.distance = tk.Entry(self, font=('arial', 9))
        cursor.callproc('find_customer')
        self.data2 = cursor.fetchall()
        self.company = ttk.Combobox(self, state="readonly", values=self.data2)
        self.date = tk.Entry(self, font=('arial', 9))
        self.city1 = tk.Entry(self, font=('arial', 9))
        self.city2 = tk.Entry(self, font=('arial', 9))
        self.mark_d = tk.Entry(self, font=('arial', 9))
        self.mark_c = tk.Entry(self, font=('arial', 9))
        self.id_label.pack()
        self.id.pack(fill='x', padx=250, pady=0)
        self.number_label.pack()
        self.number.pack(fill='x', padx=250, pady=0)
        self.license_label.pack()
        self.license.pack(fill='x', padx=250, pady=0)
        self.distance_label.pack()
        self.distance.pack(fill='x', padx=250, pady=0)
        self.company_label.pack()
        self.company.pack(fill='x', padx=250, pady=0)
        self.date_label.pack()
        self.date.pack(fill='x', padx=250, pady=0)
        self.city1_label.pack()
        self.city1.pack(fill='x', padx=250, pady=0)
        self.city2_label.pack()
        self.city2.pack(fill='x', padx=250, pady=0)
        self.mark_d_label.pack()
        self.mark_d.pack(fill='x', padx=250, pady=0)
        self.mark_c_label.pack()
        self.mark_c.pack(fill='x', padx=250, pady=0)
        self.execution_label.pack()
        self.execution = tk.StringVar(value='НЕТ')
        self.yes = tk.Radiobutton(self, text='ДА', value="ДА", variable=self.execution, background='#627182',
                                  font=('algerian', 8, 'bold'), foreground='#FAC742')
        self.no = tk.Radiobutton(self, text='НЕТ', value="НЕТ", variable=self.execution, background='#627182',
                                 font=('algerian', 8, 'bold'), foreground='#FAC742')
        self.yes.pack(fill='x', padx=250, pady=0)
        self.no.pack(fill='x', padx=250, pady=0)
        self.add_btn = tk.Button(self, text='Добавить', background='#A2E8F0', font=('algerian', 14))
        self.add_btn.pack(fill='x', padx=300, pady=5)
        self.add_btn.config(command=self._add_command)
        self.back_btn = tk.Button(self, text='Назад', background='#ADBBE0', font=('algerian', 14))
        self.back_btn.pack(fill='x', padx=300, pady=5)
        self.back_btn.config(command=self._back_command)

    def _back_command(self):
        self.forget()
        AddFrame(self.master).pack()

    def _add_command(self):
        if self.id.get().isdigit and len(self.id.get()) <= 4:
            if self.license.get() != '' and self.number.get() != '' and self.company.get() != '':
               try:
                    if float(self.distance.get()) < 10000:
                        if self.mark_c.get().isdigit() and float(self.mark_c.get()) <= 5:
                            if self.mark_d.get().isdigit() and float(self.mark_d.get()) <= 5:
                                if (self.execution.get() == 'НЕТ' and float(self.mark_c.get()) == 5 and float(
                                        self.mark_d.get()) == 5) or self.execution.get() == 'ДА':
                                    try:
                                        datetime.strptime(self.date.get(), "%Y-%m-%d")
                                        if (datetime.strptime(self.date.get(), "%Y-%m-%d")<=datetime.now() and self.execution.get()=='ДА') or self.execution.get()=='НЕТ':
                                            conn = psycopg2.connect(f'postgresql://{Config.LOGIN}:{Config.PASSWORD}@localhost/transport')
                                            cursor = conn.cursor()
                                            try:
                                                cursor.execute(
                                                    sql.SQL('CALL insert_orders(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s);'),
                                                    (float(self.id.get()), self.number.get(), float(self.license.get()),
                                                        float(self.distance.get()),
                                                        self.company.get(), self.date.get(), float(self.mark_d.get()),
                                                        float(self.mark_c.get()), self.city1.get(), self.city2.get(),
                                                        self.execution.get()))
                                                conn.commit()
                                                messagebox.showinfo('УСПЕХ', 'Вы успешно добавили заказ')
                                                self.forget()
                                                AddFrame(self.master).pack()
                                            except:messagebox.showerror('Oшибка','Ошибка! Убедитесь, что заказа с таким номером не существует!')
                                        else:messagebox.showerror('Oшибка', 'Ошибка!Дата ещё не наступила!')
                                    except:
                                        messagebox.showerror('Oшибка', 'Ошибка!Неверный формат даты!')

                                else:
                                    messagebox.showerror('Oшибка',
                                                         'Ошибка!Если заказ не выполнен должны стоять оценки по умолчанию равные 5')
                            else:
                                messagebox.showerror('Oшибка', 'Ошибка!Неправильно введена оценка заказчика!')
                        else:
                            messagebox.showerror('Oшибка', 'Ошибка!Неправильно введена оценка водителя!')
                    else:
                        messagebox.showerror('Oшибка', 'Ошибка!Неправильно введено расстояние!')
               except:
                    messagebox.showerror('Oшибка', 'Ошибка!Неправильно введено расстояние!')
            else:
                messagebox.showerror('Oшибка', 'Ошибка!Заполните пустые поля!')
        else:
            messagebox.showerror('Oшибка', 'Ошибка!Неправильно введен id заказа!')


class RemoveFrame(tk.Frame):
    def __init__(self, master, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        RemoveFrame.config(self, background='#627182')
        self.action_label = tk.Label(self, text='Что вы хотите сделать?', background='#627182',
                                     font=('algerian', 16, "bold"), foreground='#EAF0CE')
        self.driver_btn = tk.Button(self, text='Удалить водителя', background='#9DC1FA', font=('algerian', 14))
        self.car_btn = tk.Button(self, text='Удалить машину', background='#96DAFA', font=('algerian', 14))
        self.database_btn = tk.Button(self, text='Удалить базу данных', background='#9BA1FA', font=('algerian', 14))
        self.table_btn = tk.Button(self, text='Очистить таблицу', background='#B2AAFA', font=('algerian', 14))
        self.back_btn = tk.Button(self, text='Назад', background='#9BB0FA', font=('algerian', 14))
        self.action_label.pack(fill='x', padx=300, pady=15)
        self.car_btn.pack(fill='x', padx=300, pady=15)
        self.driver_btn.pack(fill='x', padx=300, pady=15)
        self.database_btn.pack(fill='x', padx=300, pady=15)
        self.table_btn.pack(fill='x', padx=300, pady=15)
        self.back_btn.pack(fill='x', padx=300, pady=15)
        self.back_btn.config(command=self._back_command)
        self.database_btn.config(command=self._database_command)
        self.table_btn.config(command=self._table_command)
        self.driver_btn.config(command=self._driver_command)
        self.car_btn.config(command=self._car_command)

    def _back_command(self):
        self.forget()
        MainFrame(self.master).pack()

    def _database_command(self):
        if (messagebox.askyesno("Предупреждение", 'Вы уверены, что хотите удалить базу данных?')):
            drop_database()
            self.forget()
            LoginFrame(self.master).pack()

    def _table_command(self):
        self.forget()
        RemoveTableFrame(self.master).pack()

    def _driver_command(self):
        self.forget()
        RemoveDriverFrame(self.master).pack()

    def _car_command(self):
        self.forget()
        RemoveCarFrame(self.master).pack()


class RemoveTableFrame(tk.Frame):
    def __init__(self, master, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        RemoveTableFrame.config(self, background='#627182')
        self.driver_btn = tk.Button(self, text='Очистить таблицу Водители', background='#9DC1FA', font=('algerian', 14))
        self.car_btn = tk.Button(self, text='Очистить таблицу Машины', background='#96DAFA', font=('algerian', 14))
        self.customer_btn = tk.Button(self, text='Очистить таблицу Заказчики', background='#9BA1FA',
                                      font=('algerian', 14))
        self.order_btn = tk.Button(self, text='Очистить таблицу Заказы', background='#B2AAFA', font=('algerian', 14))
        self.car_btn.pack(fill='x', padx=200, pady=15)
        self.driver_btn.pack(fill='x', padx=200, pady=15)
        self.customer_btn.pack(fill='x', padx=200, pady=15)
        self.order_btn.pack(fill='x', padx=200, pady=15)
        self.driver_btn.config(command=self._driver_command)
        self.car_btn.config(command=self._car_command)
        self.customer_btn.config(command=self._customer_command)
        self.order_btn.config(command=self._order_command)
        self.back_btn = tk.Button(self, text='Назад', background='#9BB0FA', font=('algerian', 14))
        self.back_btn.pack(fill='x', padx=200, pady=15)
        self.back_btn.config(command=self._back_command)

    def _driver_command(self):
        if (messagebox.askyesno("Предупреждение", 'Вы уверены, что хотите очистить таблицу водители?')):
            conn = psycopg2.connect(f'postgresql://{Config.LOGIN}:{Config.PASSWORD}@localhost/transport')
            cursor = conn.cursor()
            try:
                cursor.execute('''CALL delete_tables('driver');''')
                conn.commit()
                messagebox.showinfo('УСПЕХ', 'Таблица водители очищена')
            except:
                messagebox.showerror('Oшибка', 'Попробуйте ещё раз')

    def _car_command(self):
        if (messagebox.askyesno("Предупреждение", 'Вы уверены, что хотите очистить таблицу машины?')):
            conn = psycopg2.connect(f'postgresql://{Config.LOGIN}:{Config.PASSWORD}@localhost/transport')
            cursor = conn.cursor()
            try:
                cursor.execute('''CALL delete_tables('car');''')
                conn.commit()
                messagebox.showinfo('УСПЕХ', 'Таблица машины очищена')
            except:
                messagebox.showerror('Oшибка', 'Попробуйте ещё раз')

    def _customer_command(self):
        if (messagebox.askyesno("Предупреждение", 'Вы уверены, что хотите очистить таблицу заказчики?')):
            conn = psycopg2.connect(f'postgresql://{Config.LOGIN}:{Config.PASSWORD}@localhost/transport')
            cursor = conn.cursor()
            try:
                cursor.execute('''CALL delete_tables('customer');''')
                conn.commit()
                messagebox.showinfo('УСПЕХ', 'Таблица заказчики очищена')
            except:
                messagebox.showerror('Oшибка', 'Попробуйте ещё раз')

    def _order_command(self):
        if (messagebox.askyesno("Предупреждение", 'Вы уверены, что хотите очистить таблицу заказы?')):
            conn = psycopg2.connect(f'postgresql://{Config.LOGIN}:{Config.PASSWORD}@localhost/transport')
            cursor = conn.cursor()
            try:
                cursor.execute('''CALL delete_tables('orders');''')
                conn.commit()
                messagebox.showinfo('УСПЕХ', 'Таблица заказы очищена')
            except:
                messagebox.showerror('Oшибка', 'Попробуйте ещё раз')

    def _back_command(self):
        self.forget()
        RemoveFrame(self.master).pack()


class RemoveDriverFrame(tk.Frame):
    def __init__(self, master, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        RemoveDriverFrame.config(self, background='#627182')
        self.driver_label = tk.Label(self, text='Выберите номер телефона и фамилию водителя, которого хотите удалить',
                                     background='#627182', font=('algerian', 16, "bold"), foreground='#EAF0CE')
        conn = psycopg2.connect(f'postgresql://{Config.LOGIN}:{Config.PASSWORD}@localhost/transport')
        cursor = conn.cursor()
        cursor.callproc('find_driver_number')
        self.data = cursor.fetchall()
        self.phone = ttk.Combobox(self, state="readonly", values=self.data)
        self.driver_label.pack()
        self.phone.pack(fill='x', padx=300, pady=15)
        self.driver_btn = tk.Button(self, text='Удалить', background='#9DC1FA', font=('algerian', 14))
        self.driver_btn.pack(fill='x', padx=300, pady=15)
        self.driver_btn.config(command=self._driver_command)

        self.back_btn = tk.Button(self, text='Назад', background='#9BB0FA', font=('algerian', 14))
        self.back_btn.pack(fill='x', padx=300, pady=15)
        self.back_btn.config(command=self._back_command)


    def _driver_command(self):
        if (messagebox.askyesno("Предупреждение", 'Вы уверены, что хотите удалить водителя?')):
            conn = psycopg2.connect(f'postgresql://{Config.LOGIN}:{Config.PASSWORD}@localhost/transport')
            cursor = conn.cursor()
            if self.phone.get() != '':
                phone=(self.phone.get().split()[0])
                cursor.execute(sql.SQL('CALL delete_driver(%s);'), (phone,))
                conn.commit()
                messagebox.showinfo('УСПЕХ', 'Водитель удалён')
                self.forget()
                RemoveFrame(self.master).pack()
            else:
                messagebox.showerror('Oшибка', 'Введите фамилию водителя')

    def _back_command(self):
        self.forget()
        RemoveFrame(self.master).pack()


class RemoveCarFrame(tk.Frame):
    def __init__(self, master, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        RemoveCarFrame.config(self, background='#627182')
        self.car_label = tk.Label(self, text='Введите номер машины, которую хотите удалить', background='#627182',
                                  font=('algerian', 16, "bold"), foreground='#EAF0CE')
        conn = psycopg2.connect(f'postgresql://{Config.LOGIN}:{Config.PASSWORD}@localhost/transport')
        cursor = conn.cursor()
        cursor.callproc('find_car')
        self.data = cursor.fetchall()
        self.number = ttk.Combobox(self, state="readonly", values=self.data)
        self.car_label.pack()
        self.number.pack(fill='x', padx=300, pady=15)
        self.car_btn = tk.Button(self, text='Удалить', background='#9DC1FA', font=('algerian', 14))
        self.car_btn.pack(fill='x', padx=300, pady=15)
        self.car_btn.config(command=self._car_command)

        self.back_btn = tk.Button(self, text='Назад', background='#9BB0FA', font=('algerian', 14))
        self.back_btn.pack(fill='x', padx=300, pady=15)
        self.back_btn.config(command=self._back_command)


    def _car_command(self):
        if (messagebox.askyesno("Предупреждение", 'Вы уверены, что хотите удалить машину?')):
            conn = psycopg2.connect(f'postgresql://{Config.LOGIN}:{Config.PASSWORD}@localhost/transport')
            cursor = conn.cursor()
            if len(self.number.get()) == 8 or len(self.number.get() == 9):
                cursor.execute(sql.SQL('CALL delete_car(%s);'), (self.number.get(),))
                conn.commit()
                messagebox.showinfo('УСПЕХ', 'Машина удалена')
                self.forget()
                RemoveFrame(self.master).pack()
            else:
                messagebox.showerror('Oшибка', 'Неверный формат номера')

    def _back_command(self):
        self.forget()
        RemoveFrame(self.master).pack()


class FindFrame(tk.Frame):
    def __init__(self, master, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        FindFrame.config(self, background='#627182')
        self.driver_button = tk.Button(self, text='Найти водителя по оценке', background='#B9D6FA',
                                       font=('algerian', 14))
        self.customer1_button = tk.Button(self, text='Найти заказчика по оценке', background='#BBEBFA',
                                          font=('algerian', 14))
        self.customer2_button = tk.Button(self, text='Найти заказчика по названию компании', background='#B9F9FA',
                                          font=('algerian', 14))
        self.car_button = tk.Button(self, text='Найти машину по характеристикам', background='#B6E3FA',
                                    font=('algerian', 14))
        self.order1_button = tk.Button(self, text='Найти заказы выполненные определённым водителем',
                                       background='#B4CCFA', font=('algerian', 14))
        self.order2_button = tk.Button(self, text='Найти заказы выполненные на определённой машине',
                                       background='#B6BFFA', font=('algerian', 14))
        self.order3_button = tk.Button(self, text='Найти заказы выполненные/невыполненные', background='#C3B6FA',
                                       font=('algerian', 14))
        self.order4_button = tk.Button(self, text='Найти заказы по городу выгрузки и городу погрузки',
                                       background='#B4B6FA', font=('algerian', 14))
        self.driver_button.pack(fill='x', padx=10, pady=10)
        self.customer1_button.pack(fill='x', padx=10, pady=10)
        self.customer2_button.pack(fill='x', padx=10, pady=10)
        self.car_button.pack(fill='x', padx=10, pady=10)
        self.order1_button.pack(fill='x', padx=10, pady=10)
        self.order2_button.pack(fill='x', padx=10, pady=10)
        self.order3_button.pack(fill='x', padx=10, pady=10)
        self.order4_button.pack(fill='x', padx=10, pady=10)
        self.back_btn = tk.Button(self, text='Назад', background='#9DC1FA', font=('algerian', 14))
        self.back_btn.pack(fill='x', padx=10, pady=15)
        self.back_btn.config(command=self._back_command)
        self.driver_button.config(command=self._driver_command)
        self.car_button.config(command=self._car_command)
        self.customer1_button.config(command=self._customer1_command)
        self.customer2_button.config(command=self._customer2_command)
        self.order1_button.config(command=self._order1_command)
        self.order2_button.config(command=self._order2_command)
        self.order3_button.config(command=self._order3_command)
        self.order4_button.config(command=self._order4_command)

    def _back_command(self):
        self.forget()
        MainFrame(self.master).pack()

    def _driver_command(self):
        self.forget()
        FindDriverFrame(self.master).pack()

    def _car_command(self):
        self.forget()
        FindCarFrame(self.master).pack()

    def _customer1_command(self):
        self.forget()
        FindCustomer1Frame(self.master).pack()

    def _customer2_command(self):
        self.forget()
        FindCustomer2Frame(self.master).pack()

    def _order1_command(self):
        self.forget()
        FindOrder1Frame(self.master).pack()

    def _order2_command(self):
        self.forget()
        FindOrder2Frame(self.master).pack()

    def _order3_command(self):
        self.forget()
        FindOrder3Frame(self.master).pack()

    def _order4_command(self):
        self.forget()
        FindOrder4Frame(self.master).pack()


class FindDriverFrame(tk.Frame):
    def __init__(self, master, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        FindDriverFrame.config(self, background='#627182')
        self.rate_label = tk.Label(self, text='Оценка водителя не выше, чем:', background='#627182',
                                   font=('algerian', 16, "bold"), foreground='#EAF0CE')
        self.rate = tk.Entry(self, font=('algerian', 12))
        self.rate_label.pack()
        self.rate.pack(fill='x', padx=200, pady=15)
        self.find_button = tk.Button(self, text='Найти', background='#B2AAFA', font=('algerian', 14))
        self.find_button.pack(fill='x', padx=200, pady=15)
        self.find_button.config(command=self._get_driver)  #AAAAA
        self.back_btn = tk.Button(self, text='Назад', background='#9BB0FA', font=('algerian', 14))
        self.back_btn.pack(fill='x', padx=200, pady=15)
        self.back_btn.config(command=self._back_command)
        self.columns = ('имя', 'фамилия', 'отчество', 'оценка')
        self.tree = ttk.Treeview(columns=self.columns, show="headings")

    def _back_command(self):
        self.tree.destroy()
        self.forget()
        FindFrame(self.master).pack()

    def _get_driver(self):
        self.tree.destroy()
        self.tree = ttk.Treeview(columns=self.columns, show="headings")
        conn = psycopg2.connect(f'postgresql://{Config.LOGIN}:{Config.PASSWORD}@localhost/transport')
        cursor = conn.cursor()
        try:
            cursor.callproc('get_driver', (float(self.rate.get()),))
            if 0<=float(self.rate.get())<=5:
                self.data = cursor.fetchall()
                self.tree.heading('имя', text='ИМЯ')
                self.tree.heading('фамилия', text='ФАМИЛИЯ')
                self.tree.heading('отчество', text='ОТЧЕСТВО')
                self.tree.heading('оценка', text='ОЦЕНКА')
                for i in self.data:
                    self.tree.insert("", END, values=i)
                self.tree.pack(fill='y', expand=1)
                conn.commit()
            else:messagebox.showerror('Oшибка', 'Ошибка! Оценка должна быть в интервале от 0 до 5!')
        except:
            messagebox.showerror('Oшибка', 'Ошибка! Убедтесь, что вводите число!')


class FindCarFrame(tk.Frame):
    def __init__(self, master, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        FindCarFrame.config(self, background='#627182')
        self.capacity_label = tk.Label(self, text='Грузоподъёмность машины от:', background='#627182',
                                       font=('algerian', 16, "bold"), foreground='#EAF0CE')
        self.capacity = tk.Entry(self, font=('algerian', 12))
        self.capacity_label.pack()
        self.capacity.pack(fill='x', padx=200, pady=15)
        self.volume_label = tk.Label(self, text='Объём от:', background='#627182', font=('algerian', 16, "bold"),
                                     foreground='#EAF0CE')
        self.volume = tk.Entry(self, font=('algerian', 12))
        self.volume_label.pack()
        self.volume.pack(fill='x', padx=200, pady=15)
        self.year_label = tk.Label(self, text='Год выпуска не меньше:', background='#627182',
                                   font=('algerian', 16, "bold"), foreground='#EAF0CE')
        self.year = tk.Entry(self, font=('algerian', 12))
        self.year_label.pack()
        self.year.pack(fill='x', padx=200, pady=15)
        self.loading_label = tk.Label(self, text='Тип погрузки:', background='#627182', font=('algerian', 16, "bold"),
                                      foreground='#EAF0CE')
        self.loading = ttk.Combobox(self, state="readonly", values=["Боковая", "Верхняя", "Задняя"])
        self.loading_label.pack()
        self.loading.pack(fill='x', padx=200, pady=15)
        self.var = tk.StringVar()
        self.var.set("НЕТ")
        self.fridge = tk.Checkbutton(self, text="Наличие рефрежератора", variable=self.var, onvalue="ДА",
                                     offvalue="НЕТ", bg='#627182', font=('algerian', 16, 'bold'), foreground='#EAF0CE',
                                     selectcolor='black')
        self.fridge.pack(fill='x', padx=200, pady=15)
        self.find_button = tk.Button(self, text='Найти', background='#B2AAFA', font=('algerian', 14))
        self.find_button.pack(fill='x', padx=200, pady=15)
        self.back_btn = tk.Button(self, text='Назад', background='#9BB0FA', font=('algerian', 14))
        self.back_btn.pack(fill='x', padx=200, pady=15)
        self.back_btn.config(command=self._back_command)
        #(number VARCHAR(9), model TEXT, capacity NUMERIC(4,2), volume NUMERIC(5,2), year INTEGER
        self.find_button.config(command=self._get_specific_car)
        self.columns = ('номер', 'модель', 'груз', 'объём', 'год')
        self.tree = ttk.Treeview(columns=self.columns, show="headings")

    def _back_command(self):
        self.tree.destroy()
        self.forget()
        FindFrame(self.master).pack()

    def _get_specific_car(self):
        self.tree.destroy()
        self.tree = ttk.Treeview(columns=self.columns, show="headings")
        conn = psycopg2.connect(f'postgresql://{Config.LOGIN}:{Config.PASSWORD}@localhost/transport')
        cursor = conn.cursor()
        try:
            cursor.callproc('get_specific_car', (
                float(self.capacity.get()), int(self.volume.get()), int(self.year.get()), self.loading.get(),
                self.var.get(),))
            if 0<=float(self.capacity.get())<=100:
                if 0<=int(self.volume.get())<=1000:
                    if len(self.year.get())==4 and int(self.year.get())<=2024:
                        if self.loading.get()!='':
                                self.data = cursor.fetchall()
                                self.tree.heading('номер', text='НОМЕР')
                                self.tree.heading('модель', text='МОДЕЛЬ')
                                self.tree.heading('груз', text='ГРУЗОПОДЪЁМНОСТЬ')
                                self.tree.heading('объём', text='ОБЪЁМ')
                                self.tree.heading('год', text='ГОД')
                                for i in self.data:
                                    self.tree.insert("", END, values=i)
                                self.tree.pack(fill='y', expand=1)
                                conn.commit()
                        else:messagebox.showerror('Oшибка', 'Ошибка!  Введите тип погрузки!')
                    else:messagebox.showerror('Oшибка', 'Ошибка! Неверено введён год выпуска машины!')
                else:messagebox.showerror('Oшибка', 'Ошибка! Неверено введён объём машины!')
            else:messagebox.showerror('Oшибка', 'Ошибка! Неверено введена грузоподъёмность машины!')
        except:
            messagebox.showerror('Oшибка', 'Ошибка! Убедтесь, что правильно ввели данные!')


class FindCustomer1Frame(tk.Frame):
    def __init__(self, master, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        FindCustomer1Frame.config(self, background='#627182')
        self.rate_label = tk.Label(self, text='Оценка заказчика от:', background='#627182',
                                   font=('algerian', 16, "bold"), foreground='#EAF0CE')
        self.rate = tk.Entry(self, font=('algerian', 12))
        self.rate_label.pack()
        self.rate.pack(fill='x', padx=200, pady=15)
        self.find_button = tk.Button(self, text='Найти', background='#B2AAFA', font=('algerian', 14))
        self.find_button.pack(fill='x', padx=200, pady=15)
        self.back_btn = tk.Button(self, text='Назад', background='#9BB0FA', font=('algerian', 14))
        self.back_btn.pack(fill='x', padx=200, pady=15)
        self.back_btn.config(command=self._back_command)
        self.find_button.config(command=self._get_customer)
        self.columns = ('название организации', 'телефон', 'имя', 'фамилия', 'оценка')
        self.tree = ttk.Treeview(columns=self.columns, show="headings")

    def _back_command(self):
        self.tree.destroy()
        self.forget()
        FindFrame(self.master).pack()

    def _get_customer(self):

        self.tree.destroy()
        self.tree = ttk.Treeview(columns=self.columns, show="headings")
        conn = psycopg2.connect(f'postgresql://{Config.LOGIN}:{Config.PASSWORD}@localhost/transport')
        cursor = conn.cursor()
        try:
            cursor.callproc('get_customer', (float(self.rate.get()),))
            if 0<=float(self.rate.get())<=5:
                self.data = cursor.fetchall()
                self.tree.heading('название организации', text='НАЗВАНИЕ ОРГАНИЗАЦИИ')
                self.tree.heading('телефон', text='КОНТАКТНЫЙ ТЕЛЕФОН')
                self.tree.heading('имя', text='ИМЯ КОНТАКТНОГО ЛИЦА')
                self.tree.heading('фамилия', text='ФАМИЛИЯ КОНТАКТНОГО ЛИЦА')
                self.tree.heading('оценка', text='ОЦЕНКА')
                for i in self.data:
                    self.tree.insert("", END, values=i)
                self.tree.pack(fill='y', expand=1)
                conn.commit()
            else:messagebox.showerror('Oшибка', 'Ошибка! Оценка должна быть в промежутке от 0 до 5!')
        except:
            messagebox.showerror('Oшибка', 'Ошибка! Убедтесь, что вводите число!')


class FindCustomer2Frame(tk.Frame):
    def __init__(self, master, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        FindCustomer2Frame.config(self, background='#627182')
        self.name_label = tk.Label(self, text='Название компании:', background='#627182', font=('algerian', 16, "bold"),
                                   foreground='#EAF0CE')
        self.name = tk.Entry(self, font=('arial', 12))
        self.name_label.pack()
        self.name.pack(fill='x', padx=200, pady=15)
        self.find_button = tk.Button(self, text='Найти', background='#B2AAFA', font=('algerian', 14))
        self.find_button.pack(fill='x', padx=200, pady=15)
        self.back_btn = tk.Button(self, text='Назад', background='#9BB0FA', font=('algerian', 14))
        self.back_btn.pack(fill='x', padx=200, pady=15)
        self.back_btn.config(command=self._back_command)
        self.find_button.config(command=self._get_customer_name)
        self.columns = ('название организации', 'телефон', 'имя', 'фамилия')
        self.tree = ttk.Treeview(columns=self.columns, show="headings")

    def _back_command(self):
        self.tree.destroy()
        self.forget()
        FindFrame(self.master).pack()

    def _get_customer_name(self):
        if  self.name.get()!='':
            self.tree.destroy()
            self.tree = ttk.Treeview(columns=self.columns, show="headings")
            conn = psycopg2.connect(f'postgresql://{Config.LOGIN}:{Config.PASSWORD}@localhost/transport')
            cursor = conn.cursor()
            cursor.callproc('get_customer_name', (str(self.name.get()),))
            self.data = cursor.fetchall()
            self.tree.heading('название организации', text='НАЗВАНИЕ ОРГАНИЗАЦИИ')
            self.tree.heading('телефон', text='КОНТАКТНЫЙ ТЕЛЕФОН')
            self.tree.heading('имя', text='ИМЯ КОНТАКТНОГО ЛИЦА')
            self.tree.heading('фамилия', text='ФАМИЛИЯ КОНТАКТНОГО ЛИЦА')
            for i in self.data:
                self.tree.insert("", END, values=i)
            self.tree.pack(fill='y', expand=1)
            conn.commit()
        else:messagebox.showerror('Oшибка', 'Введите название компании')


class FindOrder1Frame(tk.Frame):
    def __init__(self, master, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        FindOrder1Frame.config(self, background='#627182')
        self.surname_label = tk.Label(self, text='Фамилия водителя:', background='#627182',
                                      font=('algerian', 16, "bold"), foreground='#EAF0CE')
        self.surname = tk.Entry(self, font=('arial', 12))
        self.surname_label.pack()
        self.surname.pack(fill='x', padx=200, pady=15)
        self.find_button = tk.Button(self, text='Найти', background='#B2AAFA', font=('algerian', 14))
        self.find_button.pack(fill='x', padx=200, pady=15)
        self.back_btn = tk.Button(self, text='Назад', background='#9BB0FA', font=('algerian', 14))
        self.back_btn.pack(fill='x', padx=200, pady=15)
        self.back_btn.config(command=self._back_command)

        #id NUMERIC(4,0), surname TEXT, car_number VARCHAR(9), distance NUMERIC(6,2), order_date DATE
        self.find_button.config(command=self._get_driver_orders)
        self.columns = ('ID', 'фамилия', 'номер', 'расстояние', 'дата')
        self.tree = ttk.Treeview(columns=self.columns, show="headings")

    def _back_command(self):
        self.tree.destroy()
        self.forget()
        FindFrame(self.master).pack()

    def _get_driver_orders(self):
        if self.surname.get()!='':
            self.tree.destroy()
            self.tree = ttk.Treeview(columns=self.columns, show="headings")
            conn = psycopg2.connect(f'postgresql://{Config.LOGIN}:{Config.PASSWORD}@localhost/transport')
            cursor = conn.cursor()
            cursor.callproc('get_driver_orders', ((self.surname.get()),))
            self.data = cursor.fetchall()
            self.tree.heading('ID', text='ID')
            self.tree.heading('фамилия', text='ФАМИЛИЯ')
            self.tree.heading('номер', text='НОМЕР')
            self.tree.heading('расстояние', text='РАССТОЯНИЕ')
            self.tree.heading('дата', text='ДАТА')
            for i in self.data:
                self.tree.insert("", END, values=i)
            self.tree.pack(fill='y', expand=1)
            conn.commit()
        else:messagebox.showerror('Oшибка', 'Введите фамилию водителя')


class FindOrder2Frame(tk.Frame):
    def __init__(self, master, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        FindOrder2Frame.config(self, background='#627182')
        self.name_label = tk.Label(self, text='Номер машины:', background='#627182', font=('algerian', 16, "bold"),
                                   foreground='#EAF0CE')
        self.name = tk.Entry(self, font=('arial', 12))
        self.name_label.pack()
        self.name.pack(fill='x', padx=200, pady=15)
        self.find_button = tk.Button(self, text='Найти', background='#B2AAFA', font=('algerian', 14))
        self.find_button.pack(fill='x', padx=200, pady=15)
        self.back_btn = tk.Button(self, text='Назад', background='#9BB0FA', font=('algerian', 14))
        self.back_btn.pack(fill='x', padx=200, pady=15)
        self.back_btn.config(command=self._back_command)
        self.find_button.config(command=self._get_car_orders)
        self.columns = ('ID', 'номер', 'модель', 'расстояние', 'дата')
        self.tree = ttk.Treeview(columns=self.columns, show="headings")

    def _back_command(self):
        self.tree.destroy()
        self.forget()
        FindFrame(self.master).pack()

    def _get_car_orders(self):
        if self.name.get()!='' and (len(self.name.get) == 8 or len(self.name.get) == 9):
            self.tree.destroy()
            self.tree = ttk.Treeview(columns=self.columns, show="headings")
            conn = psycopg2.connect(f'postgresql://{Config.LOGIN}:{Config.PASSWORD}@localhost/transport')
            cursor = conn.cursor()
            cursor.callproc('get_car_orders', ((self.name.get()),))
            self.data = cursor.fetchall()
            self.tree.heading('ID', text='ID')
            self.tree.heading('номер', text='НОМЕР')
            self.tree.heading('модель', text='МОДЕЛь')
            self.tree.heading('расстояние', text='РАССТОЯНИЕ')
            self.tree.heading('дата', text='ДАТА')
            for i in self.data:
                self.tree.insert("", END, values=i)
            self.tree.pack(fill='y', expand=1)
            conn.commit()
        else:messagebox.showerror('Oшибка', 'Неверно введён номер машины!')


class FindOrder3Frame(tk.Frame):
    def __init__(self, master, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        FindOrder3Frame.config(self, background='#627182')
        self.execution_label = tk.Label(self, text='Заказ выполнен?:', background='#627182',
                                        font=('algerian', 16, "bold"), foreground='#EAF0CE')
        self.execution_label.pack()
        self.execution = tk.StringVar(value='НЕТ')
        self.yes = tk.Radiobutton(self, text='ДА', value="ДА", variable=self.execution, background='#627182',
                                  font=('algerian', 16, "bold"), foreground='#FAC742')
        self.no = tk.Radiobutton(self, text='НЕТ', value="НЕТ", variable=self.execution, background='#627182',
                                 font=('algerian', 16, "bold"), foreground='#FAC742')
        self.yes.pack(fill='x', padx=200, pady=15)
        self.no.pack(fill='x', padx=200, pady=15)
        self.find_button = tk.Button(self, text='Найти', background='#B2AAFA', font=('algerian', 14))
        self.find_button.pack(fill='x', padx=200, pady=15)
        self.back_btn = tk.Button(self, text='Назад', background='#9BB0FA', font=('algerian', 14))
        self.back_btn.pack(fill='x', padx=200, pady=15)
        self.back_btn.config(command=self._back_command)
        self.find_button.config(command=self._get_order_status)
        self.columns = ('id', 'номер_машины', 'имя', 'фамилия', 'название_организации', 'дата', 'выполнение')
        self.tree = ttk.Treeview(columns=self.columns, show="headings")

    def _back_command(self):
        self.tree.destroy()
        self.forget()
        FindFrame(self.master).pack()

    def _get_order_status(self):
        self.tree.destroy()
        self.tree = ttk.Treeview(columns=self.columns, show="headings")
        conn = psycopg2.connect(f'postgresql://{Config.LOGIN}:{Config.PASSWORD}@localhost/transport')
        cursor = conn.cursor()
        cursor.callproc('get_order_status', (self.execution.get(),))
        self.data = cursor.fetchall()
        self.tree.heading('id', text='ID')
        self.tree.heading('номер_машины', text='НОМЕР МАШИНЫ')
        self.tree.heading('имя', text='ИМЯ ВОДИТЕЛЯ')
        self.tree.heading('фамилия', text='ФАМИЛИЯ ВОДИТЕЛЯ')
        self.tree.heading('название_организации', text='НАЗВАНИЕ ОРГАНИЗАЦИИ')
        self.tree.heading('дата', text='ДАТА')
        self.tree.heading('выполнение', text='ВЫПОЛНЕНО')
        for i in self.data:
            self.tree.insert("", END, values=i)
        self.tree.pack(fill='y', expand=1)
        conn.commit()


class FindOrder4Frame(tk.Frame):
    def __init__(self, master, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        FindOrder4Frame.config(self, background='#627182')
        self.city1_label = tk.Label(self, text='Город погрузки:', background='#627182', font=('algerian', 16, "bold"),
                                    foreground='#EAF0CE')
        self.city1 = tk.Entry(self, font=('arial', 12))
        self.city1_label.pack()
        self.city1.pack(fill='x', padx=200, pady=15)
        self.city2_label = tk.Label(self, text='Город выгрузки:', background='#627182', font=('algerian', 16, "bold"),
                                    foreground='#EAF0CE')
        self.city2 = tk.Entry(self, font=('arial', 12))
        self.city2_label.pack()
        self.city2.pack(fill='x', padx=200, pady=15)
        self.find_button = tk.Button(self, text='Найти', background='#B2AAFA', font=('algerian', 14))
        self.find_button.pack(fill='x', padx=200, pady=15)
        self.back_btn = tk.Button(self, text='Назад', background='#9BB0FA', font=('algerian', 14))
        self.back_btn.pack(fill='x', padx=200, pady=15)
        self.back_btn.config(command=self._back_command)
        self.find_button.config(command=self._get_order_cities)
        self.columns = ('id', 'название_организации', 'фамилия', 'город_погрузки', 'город_выгрузки', 'выполнение')
        self.tree = ttk.Treeview(columns=self.columns, show="headings")

    def _back_command(self):
        self.tree.destroy()
        self.forget()
        FindFrame(self.master).pack()

    def _get_order_cities(self):
        self.tree.destroy()
        self.tree = ttk.Treeview(columns=self.columns, show="headings")
        conn = psycopg2.connect(f'postgresql://{Config.LOGIN}:{Config.PASSWORD}@localhost/transport')
        cursor = conn.cursor()
        cursor.callproc('get_order_cities', (self.city1.get(), self.city2.get(),))
        self.data = cursor.fetchall()
        self.tree.heading('id', text='ID')
        self.tree.heading('название_организации', text='НАЗВАНИЕ ОРГАНИЗАЦИИ')
        self.tree.heading('фамилия', text='ФАМИЛИЯ КОНТАКТНОГО ЛИЦА')
        self.tree.heading('город_погрузки', text='ГОРОД ПОРУЗКИ')
        self.tree.heading('город_выгрузки', text='ГОРОД ВЫГРУЗКИ')
        self.tree.heading('выполнение', text='ВЫПОЛНЕНО')
        for i in self.data:
            self.tree.insert("", END, values=i)
        self.tree.pack(fill='y', expand=1)
        conn.commit()


class ContentFrame(tk.Frame):
    text = None

    def __init__(self, master, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        ContentFrame.config(self, background='#627182')
        self.Driver_table_btn = tk.Button(self, text='Посмотреть содержание таблицы Водители', background='#9DC1FA',
                                          font=('algerian', 14))
        self.Driver_table_btn.pack(fill='x', padx=10, pady=15)
        self.Driver_table_btn.config(command=self._DriverTable_command)
        self.Car_table_btn = tk.Button(self, text='Посмотреть содержание таблицы Машины', background='#96DAFA',
                                       font=('algerian', 14))
        self.Car_table_btn.pack(fill='x', padx=10, pady=15)
        self.Car_table_btn.config(command=self._CarTable_command)
        self.Customer_table_btn = tk.Button(self, text='Посмотреть содержание таблицы Заказчики', background='#9BA1FA',
                                            font=('algerian', 14))
        self.Customer_table_btn.pack(fill='x', padx=10, pady=15)
        self.Customer_table_btn.config(command=self._CustomerTable_command)
        self.Order_table_btn = tk.Button(self, text='Посмотреть содержание таблицы Заказы', background='#B2AAFA',
                                         font=('algerian', 14))
        self.Order_table_btn.pack(fill='x', padx=10, pady=15)
        self.Order_table_btn.config(command=self._OrderTable_command)
        self.back_btn = tk.Button(self, text='Назад', background='#9BB0FA', font=('algerian', 14))
        self.back_btn.pack(fill='x', padx=10, pady=15)
        self.back_btn.config(command=self._back_command)
        self.text = ''

    def _back_command(self):
        self.forget()
        MainFrame(self.master).pack()

    def _DriverTable_command(self):
        ContentFrame.text = 'driver'
        self.forget()
        Content(self.master).pack()

    def _CarTable_command(self):
        ContentFrame.text = 'car'
        self.forget()
        Content(self.master).pack()

    def _CustomerTable_command(self):
        ContentFrame.text = 'customer'
        self.forget()
        Content(self.master).pack()

    def _OrderTable_command(self, ):
        ContentFrame.text = 'orders'
        self.forget()
        Content(self.master).pack()


class Content(tk.Frame):
    def __init__(self, master, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        Content.config(self, background='#627182')
        self.back_btn = tk.Button(self, text='Назад', background='#9BB0FA', font=('algerian', 14))
        self.back_btn.pack(fill='x', padx=10, pady=15)
        self.back_btn.config(command=self._back_command)
        if ContentFrame.text == 'driver':
            self.columns = ('имя', 'фамилия', 'отчество', 'номер', 'зарплата', 'номер телефона', 'адрес', 'оценка')
            self.tree = ttk.Treeview(columns=self.columns, show="headings")
            self._driver_command()
        if ContentFrame.text == 'car':
            self.columns = ('номер', 'модель', 'груз', 'цена', 'объём', 'год', 'погрузка', 'рефрежератор')
            self.tree = ttk.Treeview(columns=self.columns, show="headings")
            self._car_command()
        if ContentFrame.text == 'customer':
            self.columns = ('название', 'телефон', 'имя', 'фамилия', 'оценка заказчика')
            self.tree = ttk.Treeview(columns=self.columns, show="headings")
            self._customer_command()
        if ContentFrame.text == 'orders':
            self.columns = (
                'id', 'номер', 'удостоверение', 'расстояние', 'организация', 'дата', 'оценка_водителя',
                'оценка_заказчика',
                'город1', 'город2', 'выполнение')
            self.tree = ttk.Treeview(columns=self.columns, show="headings")
            self._orders_command()

    def _back_command(self):
        self.tree.destroy()
        self.forget()
        ContentFrame(self.master).pack()

    def _driver_command(self):
        self.tree.destroy()
        self.tree = ttk.Treeview(columns=self.columns, show="headings")
        conn = psycopg2.connect(f'postgresql://{Config.LOGIN}:{Config.PASSWORD}@localhost/transport')
        cursor = conn.cursor()
        cursor.callproc('get_all_drivers')
        self.data = cursor.fetchall()
        self.tree.heading('имя', text='ИМЯ')
        self.tree.heading('фамилия', text='ФАМИЛИЯ')
        self.tree.heading('отчество', text='ОТЧЕСТВО')
        self.tree.heading('номер', text='НОМЕР ВОДИТЕЛЬСКОГО УДОСТОВЕРЕНИЯ')
        self.tree.heading('зарплата', text='ЗАРАБОТАННАЯ СУММА')
        self.tree.heading('номер телефона', text='НОМЕР ТЕЛЕФОНА')
        self.tree.heading('адрес', text='АДРЕС')
        self.tree.heading('оценка', text='ОЦЕНКА')
        for i in self.data:
            self.tree.insert("", END, values=i)
        self.tree.pack(fill='y', expand=1)
        conn.commit()

    def _car_command(self):
        self.tree.destroy()
        self.tree = ttk.Treeview(columns=self.columns, show="headings")
        conn = psycopg2.connect(f'postgresql://{Config.LOGIN}:{Config.PASSWORD}@localhost/transport')
        cursor = conn.cursor()
        cursor.callproc('get_all_cars')
        self.data = cursor.fetchall()
        self.tree.heading('номер', text='НОМЕР')
        self.tree.heading('модель', text='МОДЕЛЬ')
        self.tree.heading('груз', text='ГРУЗОПОДЪЁМНОСТЬ')
        self.tree.heading('цена', text='ЦЕНА')
        self.tree.heading('объём', text='ОБЪЁМ')
        self.tree.heading('год', text='ГОД ВЫПУСКА')
        self.tree.heading('погрузка', text='ТИП ПОГРУЗКИ')
        self.tree.heading('рефрежератор', text='НАЛИЧИЕ РЕФРЕЖЕРАТОРА')
        for i in self.data:
            self.tree.insert("", END, values=i)
        self.tree.pack(fill='y', expand=1)
        conn.commit()

    def _customer_command(self):
        self.tree.destroy()
        self.tree = ttk.Treeview(columns=self.columns, show="headings")
        conn = psycopg2.connect(f'postgresql://{Config.LOGIN}:{Config.PASSWORD}@localhost/transport')
        cursor = conn.cursor()
        cursor.callproc('get_all_customers')
        self.data = cursor.fetchall()
        self.tree.heading('название', text='НАЗВАНИЕ КОМПАНИИ')
        self.tree.heading('телефон', text='КОНТАКТНЫЙ ТЕЛЕФОН')
        self.tree.heading('имя', text='ИМЯ КОНТАКТНОГО ЛИЦА')
        self.tree.heading('фамилия', text='ФАМИЛИЯ КОНТАКТНОГО ЛИЦА')
        self.tree.heading('оценка заказчика', text='ОЦЕНКА ЗАКАЗЧИКА')
        for i in self.data:
            self.tree.insert("", END, values=i)
        self.tree.pack(fill='y', expand=1)
        conn.commit()

    def _orders_command(self):
        self.tree.destroy()
        self.tree = ttk.Treeview(columns=self.columns, show="headings")
        conn = psycopg2.connect(f'postgresql://{Config.LOGIN}:{Config.PASSWORD}@localhost/transport')
        cursor = conn.cursor()
        cursor.callproc('get_all_orders')
        self.data = cursor.fetchall()
        self.tree.heading('id', text='ID')
        self.tree.heading('номер', text='НОМЕР МАШИНЫ')
        self.tree.heading('удостоверение', text='НОМЕР УДОСТОВЕРЕНИЯ ВОДИТЕЛЯ')
        self.tree.heading('расстояние', text='РАССТОЯНИЕ')
        self.tree.heading('организация', text='НАЗВАНИЕ ОРГАНИЗАЦИИ')
        self.tree.heading('дата', text='ДАТА ЗАКАЗА')
        self.tree.heading('оценка_водителя', text='ОЦЕНКА ВОДИТЕЛЯ')
        self.tree.heading('оценка_заказчика', text='ОЦЕНКА ЗАКАЗЧИКА')
        self.tree.heading('город1', text='ГОРОД ПОГРУЗКИ')
        self.tree.heading('город2', text='ГОРОД ВЫГРУЗКИ')
        self.tree.heading('выполнение', text='ВЫПОЛНЕН')
        for i in self.data:
            self.tree.insert("", END, values=i)
        self.tree.pack(fill='y', expand=1)
        conn.commit()


class UpdateFrame(tk.Frame):
    def __init__(self, master, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        UpdateFrame.config(self, background='#627182')
        self.action_label = tk.Label(self, text='Что вы хотите сделать?', background='#627182',
                                     font=('algerian', 16, "bold"), foreground='#EAF0CE')
        self.phone_driver_btn = tk.Button(self, text='Изменить номер телефона водителя', background='#ADCDE0',
                                          font=('algerian', 14))
        self.address_driver_btn = tk.Button(self, text='Изменить адрес водителя', background='#96DAFA',
                                            font=('algerian', 14))
        self.customer_btn = tk.Button(self, text='Изменить контактное лицо заказчика', background='#86B8EF',
                                      font=('algerian', 14))
        self.order_btn = tk.Button(self, text='Изменить статус заказа на выполненный', background='#8CBAFA',
                                   font=('algerian', 14))
        self.back_btn = tk.Button(self, text='Назад', background='#7B7AF0', font=('algerian', 14))
        self.action_label.pack(fill='x', padx=200, pady=15)
        self.phone_driver_btn.pack(fill='x', padx=200, pady=15)
        self.address_driver_btn.pack(fill='x', padx=200, pady=15)
        self.customer_btn.pack(fill='x', padx=200, pady=15)
        self.order_btn.pack(fill='x', padx=200, pady=15)
        self.back_btn.pack(fill='x', padx=200, pady=15)
        self.phone_driver_btn.config(command=self._phone_driver_command)
        self.address_driver_btn.config(command=self._address_driver_command)
        self.customer_btn.config(command=self._contact_customer_command)
        self.order_btn.config(command=self._status_order_command)
        self.back_btn.config(command=self._back_command)

    def _back_command(self):
        self.forget()
        MainFrame(self.master).pack()

    def _phone_driver_command(self):
        self.forget()
        UpdatePhoneDriver(self.master).pack()

    def _address_driver_command(self):
        self.forget()
        UpdateAddressDriver(self.master).pack()

    def _contact_customer_command(self):
        self.forget()
        UpdateCustomer(self.master).pack()

    def _status_order_command(self):
        self.forget()
        UpdateOrder(self.master).pack()


class UpdatePhoneDriver(tk.Frame):
    def __init__(self, master, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        UpdatePhoneDriver.config(self, background='#627182')
        self.license_label = tk.Label(self, text='Номер водительского удостоверения водителя:', background='#627182',
                                      font=('algerian', 16, "bold"),
                                      foreground='#EAF0CE')
        conn = psycopg2.connect(f'postgresql://{Config.LOGIN}:{Config.PASSWORD}@localhost/transport')
        cursor = conn.cursor()
        cursor.callproc('find_license')
        self.data = cursor.fetchall()
        self.license = ttk.Combobox(self, state="readonly", values=self.data)
        self.license_label.pack()
        self.license.pack(fill='x', padx=200, pady=15)
        self.phone_label = tk.Label(self, text='Новый номер телефона водителя:', background='#627182',
                                    font=('algerian', 16, "bold"),
                                    foreground='#EAF0CE')
        self.phone = tk.Entry(self, font=('arial', 12))
        self.phone_label.pack()
        self.phone.pack(fill='x', padx=200, pady=15)
        self.update_button = tk.Button(self, text='Изменить', background='#B2AAFA', font=('algerian', 14))
        self.update_button.pack(fill='x', padx=200, pady=15)
        self.update_button.config(command=self._update_command)
        self.back_btn = tk.Button(self, text='Назад', background='#9BB0FA', font=('algerian', 14))
        self.back_btn.pack(fill='x', padx=200, pady=15)
        self.back_btn.config(command=self._back_command)

    def _back_command(self):
        self.forget()
        UpdateFrame(self.master).pack()

    def _update_command(self):
        if self.license.get() != '':
            conn = psycopg2.connect(f'postgresql://{Config.LOGIN}:{Config.PASSWORD}@localhost/transport')
            cursor = conn.cursor()
            cursor.execute(sql.SQL('CALL update_phone_driver(%s,%s);'), (float(self.license.get()), self.phone.get(),))
            conn.commit()
            messagebox.showinfo('УСПЕХ', 'Вы успешно изменили телефон водителя')
        else:
            messagebox.showerror('Oшибка', 'Введите номер водительского удостоверения водителя')


class UpdateAddressDriver(tk.Frame):
    def __init__(self, master, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        UpdateAddressDriver.config(self, background='#627182')
        self.license_label = tk.Label(self, text='Номер водительского удостоверения водителя:', background='#627182',
                                      font=('algerian', 16, "bold"),
                                      foreground='#EAF0CE')
        conn = psycopg2.connect(f'postgresql://{Config.LOGIN}:{Config.PASSWORD}@localhost/transport')
        cursor = conn.cursor()
        cursor.callproc('find_license')
        self.data = cursor.fetchall()
        self.license = ttk.Combobox(self, state="readonly", values=self.data)
        self.license_label.pack()
        self.license.pack(fill='x', padx=200, pady=15)
        self.address_label = tk.Label(self, text='Новый адрес водителя:', background='#627182',
                                      font=('algerian', 16, "bold"),
                                      foreground='#EAF0CE')
        self.address = tk.Entry(self, font=('arial', 12))
        self.address_label.pack()
        self.address.pack(fill='x', padx=200, pady=15)
        self.update_button = tk.Button(self, text='Изменить', background='#B2AAFA', font=('algerian', 14))
        self.update_button.pack(fill='x', padx=200, pady=15)
        self.update_button.config(command=self._update_command)
        self.back_btn = tk.Button(self, text='Назад', background='#9BB0FA', font=('algerian', 14))
        self.back_btn.pack(fill='x', padx=200, pady=15)
        self.back_btn.config(command=self._back_command)

    def _back_command(self):
        self.forget()
        UpdateFrame(self.master).pack()

    def _update_command(self):
        if self.license.get() != '':
            conn = psycopg2.connect(f'postgresql://{Config.LOGIN}:{Config.PASSWORD}@localhost/transport')
            cursor = conn.cursor()
            cursor.execute(sql.SQL('CALL update_address_driver(%s,%s);'),
                           (float(self.license.get()), self.address.get(),))
            conn.commit()
            messagebox.showinfo('УСПЕХ', 'Вы успешно изменили адрес водителя')
        else:
            messagebox.showerror('Oшибка', 'Введите водительское удостоверение водителя')


class UpdateCustomer(tk.Frame):
    def __init__(self, master, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        UpdateCustomer.config(self, background='#627182')
        self.organization_label = tk.Label(self, text='Название организации:', background='#627182',
                                           font=('algerian', 16, "bold"),
                                           foreground='#EAF0CE')
        conn = psycopg2.connect(f'postgresql://{Config.LOGIN}:{Config.PASSWORD}@localhost/transport')
        cursor = conn.cursor()
        cursor.callproc('find_customer')
        self.data = cursor.fetchall()
        self.organization = ttk.Combobox(self, state="readonly", values=self.data)
        self.organization_label.pack()
        self.organization.pack(fill='x', padx=200, pady=15)
        self.name_label = tk.Label(self, text='Имя нового контактного лица:', background='#627182',
                                   font=('algerian', 16, "bold"),
                                   foreground='#EAF0CE')
        self.name = tk.Entry(self, font=('arial', 12))
        self.name_label.pack()
        self.name.pack(fill='x', padx=200, pady=15)
        self.surname_label = tk.Label(self, text='Фамилия нового контактного лица:', background='#627182',
                                      font=('algerian', 16, "bold"),
                                      foreground='#EAF0CE')
        self.surname = tk.Entry(self, font=('arial', 12))
        self.surname_label.pack()
        self.surname.pack(fill='x', padx=200, pady=15)
        self.update_button = tk.Button(self, text='Изменить', background='#B2AAFA', font=('algerian', 14))
        self.update_button.pack(fill='x', padx=200, pady=15)
        self.update_button.config(command=self._update_command)
        self.back_btn = tk.Button(self, text='Назад', background='#9BB0FA', font=('algerian', 14))
        self.back_btn.pack(fill='x', padx=200, pady=15)
        self.back_btn.config(command=self._back_command)

    def _back_command(self):
        self.forget()
        UpdateFrame(self.master).pack()

    def _update_command(self):
        if self.organization.get()!='':
            conn = psycopg2.connect(f'postgresql://{Config.LOGIN}:{Config.PASSWORD}@localhost/transport')
            cursor = conn.cursor()
            cursor.execute(sql.SQL('CALL update_contact_company(%s,%s,%s);'),
                       (self.organization.get(), self.name.get(), self.surname.get(),))
            conn.commit()
            messagebox.showinfo('УСПЕХ', 'Вы успешно изменили контактное лицо')
        else:messagebox.showerror('Oшибка', 'Введите название организации!')

class UpdateOrder(tk.Frame):
    def __init__(self, master, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        UpdateOrder.config(self, background='#627182')
        self.id_label = tk.Label(self, text='ID заказа:', background='#627182',
                                 font=('algerian', 16, "bold"),
                                 foreground='#EAF0CE')
        conn = psycopg2.connect(f'postgresql://{Config.LOGIN}:{Config.PASSWORD}@localhost/transport')
        cursor = conn.cursor()
        cursor.callproc('find_unimplemented_order')
        self.data = cursor.fetchall()
        self.id = ttk.Combobox(self, state="readonly", values=self.data)
        self.id_label.pack()
        self.id.pack(fill='x', padx=200, pady=15)
        self.driver_label = tk.Label(self, text='Оценка водителя:', background='#627182',
                                     font=('algerian', 16, "bold"),
                                     foreground='#EAF0CE')
        self.driver = tk.Entry(self, font=('arial', 12))
        self.driver_label.pack()
        self.driver.pack(fill='x', padx=200, pady=15)
        self.customer_label = tk.Label(self, text='Оценка заказчика:', background='#627182',
                                       font=('algerian', 16, "bold"),
                                       foreground='#EAF0CE')
        self.customer = tk.Entry(self, font=('arial', 12))
        self.customer_label.pack()
        self.customer.pack(fill='x', padx=200, pady=15)
        self.update_button = tk.Button(self, text='Изменить', background='#B2AAFA', font=('algerian', 14))
        self.update_button.pack(fill='x', padx=200, pady=15)
        self.update_button.config(command=self._update_command)
        self.back_btn = tk.Button(self, text='Назад', background='#9BB0FA', font=('algerian', 14))
        self.back_btn.pack(fill='x', padx=200, pady=15)
        self.back_btn.config(command=self._back_command)

    def _back_command(self):
        self.forget()
        UpdateFrame(self.master).pack()

    def _update_command(self):
        if self.id.get().isdigit() and len(self.id.get()) <= 4:
            if self.driver.get().isdigit() and 0 <= float(self.driver.get()) <= 5:
                if self.customer.get().isdigit() and 0 <= float(self.customer.get()) <= 5:
                    try:
                        conn = psycopg2.connect(f'postgresql://{Config.LOGIN}:{Config.PASSWORD}@localhost/transport')
                        cursor = conn.cursor()
                        cursor.execute(sql.SQL('CALL update_status_orders(%s,%s,%s);'),
                                   (float(self.id.get()), float(self.driver.get()), float(self.customer.get(), )))
                        conn.commit()
                        messagebox.showinfo('УСПЕХ', 'Вы успешно изменили статус заказа')
                    except:messagebox.showerror('Oшибка', 'Не удалось изменить статус заказа')
                else:
                    messagebox.showerror('Oшибка', 'Неверный формат оценки заказчика')
            else:
                messagebox.showerror('Oшибка', 'Неверный формат оценки водителя')
        else:
            messagebox.showerror('Oшибка', 'Неверный ID')
class CatFrame(tk.Frame):
    def __init__(self, master, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        CatFrame.config(self, background='#627182')
        rand = random.choice([1,2,3])
        if  (rand==1):image = Image.open("cat.jpg")
        elif (rand==2):image = Image.open("cat1.jpg")
        else: image = Image.open("cat2.jpg")
        self.img = ImageTk.PhotoImage(image)
        self.img_button = tk.Button(self, image=self.img)
        self.img_button.pack(fill='both', padx=100,pady=100)
        self.img_button.config(command=self._back_command)
    def _back_command(self):
        self.forget()
        MainFrame(self.master).pack()

window = tk.Tk()
window.geometry('1250x750')
window.title('Грузоперевозки')
window.config(background='#627182')
LoginFrame(window).pack()

window.mainloop()
