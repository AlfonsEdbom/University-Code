--
-- Random stuff from PgAdmin4 dump
--

SET statement_timeout = 0;
SET lock_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SET check_function_bodies = false;
SET client_min_messages = warning;



SET default_tablespace = '';

SET default_with_oids = false;


---
---  Drop database if already exists one with same name
--- 
DROP DATABASE IF EXISTS snacks;

--
-- Create Database and Enter it
--

CREATE DATABASE snacks WITH ENCODING = 'UTF8';
\connect snacks

--
-- Random stuff from PgAdmin4 dump AGAIN???????????
--

SET statement_timeout = 0;
SET lock_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SET check_function_bodies = false;
SET client_min_messages = warning;



SET default_tablespace = '';

SET default_with_oids = false;


--
-- Drop tables if exists already for some reason
--

DROP TABLE IF EXISTS snacks_at_home;
DROP TABLE IF EXISTS people;
DROP TABLE IF EXISTS snacks;


---
--- Create Functions and Triggers (might need to move Triggers under INSERTS)
---

--
-- Name: check_cost(); Type: FUNCTION; Schema: public
--

CREATE OR REPLACE FUNCTION check_cost() RETURNS trigger
    LANGUAGE plpgsql
    AS $$
        BEGIN
        IF NEW.cost < 0 THEN
            RAISE EXCEPTION 'The cost of an item cannot be negative';
        END IF;

        RETURN NEW;
        END;$$;
--
-- Name: check_amount(); Type: FUNCTION; Schema: public
--

CREATE OR REPLACE FUNCTION check_amount() RETURNS trigger
    LANGUAGE plpgsql
    AS $$
        BEGIN
        IF NEW.amount <= 0 THEN
            RAISE EXCEPTION 'The amount of an item cannot be 0 or negative';
        
        END IF;
        
        RETURN NEW;
        END;$$;



---
--- Create Tables
---


--
-- Name: people; Type: TABLE; Schema: public; Owner: -; Tablespace:
--




CREATE TABLE people(
    person_id INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    fname TEXT NOT NULL,
    lname TEXT NOT NULL,
    email TEXT NOT NULL UNIQUE,
    UNIQUE (fname, lname)
);

--
-- Name: snacks; Type: TABLE; Schema: public; Owner: -; Tablespace:
--

CREATE TABLE snacks(
    snack_id INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    snack_name TEXT NOT NULL UNIQUE,
    cost NUMERIC(6,2) CHECK(cost >= 0) 
);

--
-- Name: snacks_at_home; Type: TABLE; Schema: public; Owner: -; Tablespace:
--

CREATE TABLE snacks_at_home(
    person INTEGER,
    snack INTEGER,
    amount INTEGER NOT NULL CHECK(amount > 0),
    CONSTRAINT fk_person
        FOREIGN KEY(person)
            REFERENCES people(person_id)
            ON DELETE CASCADE
            ON UPDATE CASCADE,
    CONSTRAINT fk_snack
        FOREIGN KEY(snack)
            REFERENCES snacks(snack_id)
            ON DELETE CASCADE
            ON UPDATE CASCADE);

---
--- Insert data to Tables
---

--
-- Data for Name: people, Type: TABLE DATA, Schema: public
--

INSERT INTO people(fname, lname, email) 
    VALUES 
        ('Alfons', 'Edbom Devall', 'alde0033@student.umu.se'),
        ('Johan  ', 'Lehto', 'jole0088@student.umu.se'),
        ('John', 'Doe', 'john_doe@hotmail.com'),
        ('Jane', 'Doe', 'jane_doe@gmail.com'),
        ('Michael', 'Minock', 'michael.minock@umu.se');

--
-- Data for Name: snacks, Type: TABLE DATA, Schema: public
--

INSERT INTO snacks(snack_name, cost) 
    VALUES
        ('Banana', 5.1),
        ('Chocolate cookies', 3.5),
        ('Rice cookies', 2.2),
        ('Bread', 7.4),
        ('Chocolate', 9.9),
        ('Candy', 9999.11111);

--
-- Data for Name: snacks_at_home, Type: TABLE DATA, Schema: public
--

INSERT INTO snacks_at_home(person, snack, amount)
    VALUES 
        (1, 1, 10),
        (1, 2, 5),
        (1, 5, 10),
        (2, 3, 2),
        (2, 4, 1),
        (2, 6, 4),
        (4, 1, 1),
        (5, 3, 20);

---
--- CONSTRAINTS (PRIMARY KEY, FOREIGN KEY, ....) (TRIGGERS????)
---

CREATE TRIGGER cost_check 
    BEFORE INSERT OR UPDATE OF cost 
    ON snacks
    FOR EACH ROW 
        EXECUTE FUNCTION check_cost();



CREATE TRIGGER snacks_check 
    BEFORE INSERT OR UPDATE OF amount 
    ON snacks_at_home 
    FOR EACH ROW 
        EXECUTE FUNCTION check_amount();

