--
-- PostgreSQL database dump
--

\restrict EBeQLnOqiYSZbjkSKcnRHbVmRVDsxeCTiEsh1gNpWKIDv1nxaA79umcbhXmjPzd

-- Dumped from database version 18.3
-- Dumped by pg_dump version 18.3

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET transaction_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: otp_verifications; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.otp_verifications (
    id integer NOT NULL,
    contact character varying(100) NOT NULL,
    otp character varying(10) NOT NULL,
    purpose character varying(50) NOT NULL,
    verified integer,
    created_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP,
    expires_at timestamp without time zone NOT NULL
);


--
-- Name: otp_verifications_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.otp_verifications_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: otp_verifications_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.otp_verifications_id_seq OWNED BY public.otp_verifications.id;


--
-- Name: parents; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.parents (
    id integer NOT NULL,
    phone_no character varying(15) NOT NULL,
    college_id character varying(50) NOT NULL,
    student_name character varying(100),
    created_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP
);


--
-- Name: parents_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.parents_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: parents_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.parents_id_seq OWNED BY public.parents.id;


--
-- Name: student_registry; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.student_registry (
    id integer NOT NULL,
    college_id character varying(50) NOT NULL,
    is_registered boolean
);


--
-- Name: student_registry_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.student_registry_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: student_registry_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.student_registry_id_seq OWNED BY public.student_registry.id;


--
-- Name: students; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.students (
    id integer NOT NULL,
    college_id character varying(50) NOT NULL,
    full_name character varying(100) NOT NULL,
    email character varying(100) NOT NULL,
    phone_no character varying(15) NOT NULL,
    password_hash character varying(255) NOT NULL,
    room_number character varying(20),
    status character varying(20),
    created_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP,
    updated_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP
);


--
-- Name: students_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.students_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: students_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.students_id_seq OWNED BY public.students.id;


--
-- Name: wardens; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.wardens (
    id integer NOT NULL,
    email character varying(100) NOT NULL,
    warden_id character varying(50) NOT NULL,
    password_hash character varying(255) NOT NULL,
    role character varying(20),
    created_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP,
    updated_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP
);


--
-- Name: wardens_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.wardens_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: wardens_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.wardens_id_seq OWNED BY public.wardens.id;


--
-- Name: otp_verifications id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.otp_verifications ALTER COLUMN id SET DEFAULT nextval('public.otp_verifications_id_seq'::regclass);


--
-- Name: parents id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.parents ALTER COLUMN id SET DEFAULT nextval('public.parents_id_seq'::regclass);


--
-- Name: student_registry id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.student_registry ALTER COLUMN id SET DEFAULT nextval('public.student_registry_id_seq'::regclass);


--
-- Name: students id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.students ALTER COLUMN id SET DEFAULT nextval('public.students_id_seq'::regclass);


--
-- Name: wardens id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.wardens ALTER COLUMN id SET DEFAULT nextval('public.wardens_id_seq'::regclass);


--
-- Data for Name: otp_verifications; Type: TABLE DATA; Schema: public; Owner: -
--



--
-- Data for Name: parents; Type: TABLE DATA; Schema: public; Owner: -
--



--
-- Data for Name: student_registry; Type: TABLE DATA; Schema: public; Owner: -
--

INSERT INTO public.student_registry VALUES (1, 'STU001', true);
INSERT INTO public.student_registry VALUES (2, 'STU002', true);
INSERT INTO public.student_registry VALUES (3, 'STU003', true);
INSERT INTO public.student_registry VALUES (4, 'STU004', false);


--
-- Data for Name: students; Type: TABLE DATA; Schema: public; Owner: -
--



--
-- Data for Name: wardens; Type: TABLE DATA; Schema: public; Owner: -
--



--
-- Name: otp_verifications_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.otp_verifications_id_seq', 1, false);


--
-- Name: parents_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.parents_id_seq', 1, false);


--
-- Name: student_registry_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.student_registry_id_seq', 4, true);


--
-- Name: students_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.students_id_seq', 1, false);


--
-- Name: wardens_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.wardens_id_seq', 1, false);


--
-- Name: otp_verifications otp_verifications_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.otp_verifications
    ADD CONSTRAINT otp_verifications_pkey PRIMARY KEY (id);


--
-- Name: parents parents_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.parents
    ADD CONSTRAINT parents_pkey PRIMARY KEY (id);


--
-- Name: student_registry student_registry_college_id_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.student_registry
    ADD CONSTRAINT student_registry_college_id_key UNIQUE (college_id);


--
-- Name: student_registry student_registry_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.student_registry
    ADD CONSTRAINT student_registry_pkey PRIMARY KEY (id);


--
-- Name: students students_email_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.students
    ADD CONSTRAINT students_email_key UNIQUE (email);


--
-- Name: students students_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.students
    ADD CONSTRAINT students_pkey PRIMARY KEY (id);


--
-- Name: wardens wardens_email_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.wardens
    ADD CONSTRAINT wardens_email_key UNIQUE (email);


--
-- Name: wardens wardens_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.wardens
    ADD CONSTRAINT wardens_pkey PRIMARY KEY (id);


--
-- Name: wardens wardens_warden_id_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.wardens
    ADD CONSTRAINT wardens_warden_id_key UNIQUE (warden_id);


--
-- Name: ix_otp_verifications_contact; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX ix_otp_verifications_contact ON public.otp_verifications USING btree (contact);


--
-- Name: ix_otp_verifications_id; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX ix_otp_verifications_id ON public.otp_verifications USING btree (id);


--
-- Name: ix_parents_id; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX ix_parents_id ON public.parents USING btree (id);


--
-- Name: ix_parents_phone_no; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX ix_parents_phone_no ON public.parents USING btree (phone_no);


--
-- Name: ix_students_college_id; Type: INDEX; Schema: public; Owner: -
--

CREATE UNIQUE INDEX ix_students_college_id ON public.students USING btree (college_id);


--
-- Name: ix_students_id; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX ix_students_id ON public.students USING btree (id);


--
-- Name: ix_wardens_id; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX ix_wardens_id ON public.wardens USING btree (id);


--
-- Name: parents parents_college_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.parents
    ADD CONSTRAINT parents_college_id_fkey FOREIGN KEY (college_id) REFERENCES public.students(college_id);


--
-- PostgreSQL database dump complete
--

\unrestrict EBeQLnOqiYSZbjkSKcnRHbVmRVDsxeCTiEsh1gNpWKIDv1nxaA79umcbhXmjPzd

