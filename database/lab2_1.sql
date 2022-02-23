--
-- PostgreSQL database dump
--

-- Dumped from database version 14.1
-- Dumped by pg_dump version 14.1

-- Started on 2022-02-23 11:04:45

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

DROP DATABASE lab2;
--
-- TOC entry 3341 (class 1262 OID 16562)
-- Name: lab2; Type: DATABASE; Schema: -; Owner: postgres
--

CREATE DATABASE lab2 WITH TEMPLATE = template0 ENCODING = 'UTF8' LOCALE = 'English_United States.1252';


ALTER DATABASE lab2 OWNER TO postgres;

\connect lab2

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

--
-- TOC entry 216 (class 1255 OID 16924)
-- Name: check_amount(); Type: FUNCTION; Schema: public; Owner: postgres
--

CREATE FUNCTION public.check_amount() RETURNS trigger
    LANGUAGE plpgsql
    AS $$BEGIN
    IF NEW.amount < 0 THEN
        RAISE EXCEPTION 'The amount of an item cannot be negative';
    END IF;
    
    RETURN NEW;
END;$$;


ALTER FUNCTION public.check_amount() OWNER TO postgres;

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- TOC entry 210 (class 1259 OID 16886)
-- Name: snacks; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.snacks (
    snack_id integer NOT NULL,
    snack_name text NOT NULL,
    cost numeric(3,1)
);


ALTER TABLE public.snacks OWNER TO postgres;

--
-- TOC entry 209 (class 1259 OID 16885)
-- Name: Snacks_snack_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public."Snacks_snack_id_seq"
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public."Snacks_snack_id_seq" OWNER TO postgres;

--
-- TOC entry 3342 (class 0 OID 0)
-- Dependencies: 209
-- Name: Snacks_snack_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public."Snacks_snack_id_seq" OWNED BY public.snacks.snack_id;


--
-- TOC entry 211 (class 1259 OID 16895)
-- Name: people; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.people (
    fname text NOT NULL,
    lname text,
    person_id integer NOT NULL
);


ALTER TABLE public.people OWNER TO postgres;

--
-- TOC entry 215 (class 1259 OID 16927)
-- Name: people_person_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.people_person_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.people_person_id_seq OWNER TO postgres;

--
-- TOC entry 3343 (class 0 OID 0)
-- Dependencies: 215
-- Name: people_person_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.people_person_id_seq OWNED BY public.people.person_id;


--
-- TOC entry 214 (class 1259 OID 16905)
-- Name: snacks_at_home; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.snacks_at_home (
    person integer NOT NULL,
    snack integer NOT NULL,
    amount integer DEFAULT 0 NOT NULL
);


ALTER TABLE public.snacks_at_home OWNER TO postgres;

--
-- TOC entry 212 (class 1259 OID 16903)
-- Name: snacks_at_home_person_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.snacks_at_home_person_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.snacks_at_home_person_seq OWNER TO postgres;

--
-- TOC entry 3344 (class 0 OID 0)
-- Dependencies: 212
-- Name: snacks_at_home_person_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.snacks_at_home_person_seq OWNED BY public.snacks_at_home.person;


--
-- TOC entry 213 (class 1259 OID 16904)
-- Name: snacks_at_home_snack_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.snacks_at_home_snack_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.snacks_at_home_snack_seq OWNER TO postgres;

--
-- TOC entry 3345 (class 0 OID 0)
-- Dependencies: 213
-- Name: snacks_at_home_snack_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.snacks_at_home_snack_seq OWNED BY public.snacks_at_home.snack;


--
-- TOC entry 3177 (class 2604 OID 16928)
-- Name: people person_id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.people ALTER COLUMN person_id SET DEFAULT nextval('public.people_person_id_seq'::regclass);


--
-- TOC entry 3176 (class 2604 OID 16889)
-- Name: snacks snack_id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.snacks ALTER COLUMN snack_id SET DEFAULT nextval('public."Snacks_snack_id_seq"'::regclass);


--
-- TOC entry 3178 (class 2604 OID 16908)
-- Name: snacks_at_home person; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.snacks_at_home ALTER COLUMN person SET DEFAULT nextval('public.snacks_at_home_person_seq'::regclass);


--
-- TOC entry 3179 (class 2604 OID 16909)
-- Name: snacks_at_home snack; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.snacks_at_home ALTER COLUMN snack SET DEFAULT nextval('public.snacks_at_home_snack_seq'::regclass);


--
-- TOC entry 3331 (class 0 OID 16895)
-- Dependencies: 211
-- Data for Name: people; Type: TABLE DATA; Schema: public; Owner: postgres
--

INSERT INTO public.people (fname, lname, person_id) VALUES ('Alfons', 'Edbom', 1);
INSERT INTO public.people (fname, lname, person_id) VALUES ('Johan', 'Lehto', 3);
INSERT INTO public.people (fname, lname, person_id) VALUES ('John', 'Doe', 4);


--
-- TOC entry 3330 (class 0 OID 16886)
-- Dependencies: 210
-- Data for Name: snacks; Type: TABLE DATA; Schema: public; Owner: postgres
--



--
-- TOC entry 3334 (class 0 OID 16905)
-- Dependencies: 214
-- Data for Name: snacks_at_home; Type: TABLE DATA; Schema: public; Owner: postgres
--



--
-- TOC entry 3346 (class 0 OID 0)
-- Dependencies: 209
-- Name: Snacks_snack_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public."Snacks_snack_id_seq"', 1, false);


--
-- TOC entry 3347 (class 0 OID 0)
-- Dependencies: 215
-- Name: people_person_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.people_person_id_seq', 4, true);


--
-- TOC entry 3348 (class 0 OID 0)
-- Dependencies: 212
-- Name: snacks_at_home_person_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.snacks_at_home_person_seq', 1, false);


--
-- TOC entry 3349 (class 0 OID 0)
-- Dependencies: 213
-- Name: snacks_at_home_snack_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.snacks_at_home_snack_seq', 1, false);


--
-- TOC entry 3182 (class 2606 OID 16893)
-- Name: snacks Snacks_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.snacks
    ADD CONSTRAINT "Snacks_pkey" PRIMARY KEY (snack_id);


--
-- TOC entry 3184 (class 2606 OID 16935)
-- Name: people people_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.people
    ADD CONSTRAINT people_pkey PRIMARY KEY (person_id);


--
-- TOC entry 3186 (class 2606 OID 16911)
-- Name: snacks_at_home snacks_at_home_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.snacks_at_home
    ADD CONSTRAINT snacks_at_home_pkey PRIMARY KEY (person, snack);


--
-- TOC entry 3189 (class 2620 OID 16925)
-- Name: snacks_at_home snacks_check; Type: TRIGGER; Schema: public; Owner: postgres
--

CREATE TRIGGER snacks_check BEFORE INSERT OR UPDATE OF amount ON public.snacks_at_home FOR EACH ROW EXECUTE FUNCTION public.check_amount();


--
-- TOC entry 3188 (class 2606 OID 16936)
-- Name: snacks_at_home person; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.snacks_at_home
    ADD CONSTRAINT person FOREIGN KEY (person) REFERENCES public.people(person_id) NOT VALID;


--
-- TOC entry 3187 (class 2606 OID 16917)
-- Name: snacks_at_home snack; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.snacks_at_home
    ADD CONSTRAINT snack FOREIGN KEY (snack) REFERENCES public.snacks(snack_id);


-- Completed on 2022-02-23 11:04:46

--
-- PostgreSQL database dump complete
--

