--
-- PostgreSQL database dump
--

-- Dumped from database version 13.2 (Debian 13.2-1.pgdg100+1)
-- Dumped by pg_dump version 13.2

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

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: address_helper; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.address_helper (
    id integer NOT NULL,
    country_code character varying(50) NOT NULL,
    country_name character varying(200) NOT NULL,
    state character varying(400) NOT NULL,
    state_code character varying(100) NOT NULL,
    city character varying(400) NOT NULL,
    "order" bigint NOT NULL
);


ALTER TABLE public.address_helper OWNER TO postgres;

--
-- Name: address_type_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.address_type_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.address_type_id_seq OWNER TO postgres;

--
-- Name: address_type_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.address_type_id_seq OWNED BY public.address_helper.id;


--
-- Name: aggregation_type; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.aggregation_type (
    id integer NOT NULL,
    name character varying(250) NOT NULL,
    "order" bigint NOT NULL
);


ALTER TABLE public.aggregation_type OWNER TO postgres;

--
-- Name: aggregation_type_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.aggregation_type_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.aggregation_type_id_seq OWNER TO postgres;

--
-- Name: aggregation_type_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.aggregation_type_id_seq OWNED BY public.aggregation_type.id;


--
-- Name: data_type; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.data_type (
    id integer NOT NULL,
    name character varying(250) NOT NULL,
    label_name character varying(200) NOT NULL,
    "order" bigint NOT NULL
);


ALTER TABLE public.data_type OWNER TO postgres;

--
-- Name: app_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.app_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.app_id_seq OWNER TO postgres;

--
-- Name: app_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.app_id_seq OWNED BY public.data_type.id;


--
-- Name: attachments; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.attachments (
    id integer NOT NULL,
    created_at timestamp with time zone NOT NULL,
    updated_at timestamp with time zone NOT NULL,
    file character varying(500),
    bucket character varying(200) NOT NULL,
    file_attachments_path character varying(250) NOT NULL,
    file_url character varying(1000),
    file_size bigint NOT NULL,
    date date NOT NULL,
    field_id integer,
    form_id integer
);


ALTER TABLE public.attachments OWNER TO postgres;

--
-- Name: attachments_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.attachments_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.attachments_id_seq OWNER TO postgres;

--
-- Name: attachments_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.attachments_id_seq OWNED BY public.attachments.id;


--
-- Name: auth_group; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.auth_group (
    id integer NOT NULL,
    name character varying(150) NOT NULL
);


ALTER TABLE public.auth_group OWNER TO postgres;

--
-- Name: auth_group_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.auth_group_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.auth_group_id_seq OWNER TO postgres;

--
-- Name: auth_group_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.auth_group_id_seq OWNED BY public.auth_group.id;


--
-- Name: auth_group_permissions; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.auth_group_permissions (
    id integer NOT NULL,
    group_id integer NOT NULL,
    permission_id integer NOT NULL
);


ALTER TABLE public.auth_group_permissions OWNER TO postgres;

--
-- Name: auth_group_permissions_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.auth_group_permissions_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.auth_group_permissions_id_seq OWNER TO postgres;

--
-- Name: auth_group_permissions_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.auth_group_permissions_id_seq OWNED BY public.auth_group_permissions.id;


--
-- Name: auth_permission; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.auth_permission (
    id integer NOT NULL,
    name character varying(255) NOT NULL,
    content_type_id integer NOT NULL,
    codename character varying(100) NOT NULL
);


ALTER TABLE public.auth_permission OWNER TO postgres;

--
-- Name: auth_permission_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.auth_permission_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.auth_permission_id_seq OWNER TO postgres;

--
-- Name: auth_permission_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.auth_permission_id_seq OWNED BY public.auth_permission.id;


--
-- Name: charge_frequency_type; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.charge_frequency_type (
    id integer NOT NULL,
    name character varying(250) NOT NULL,
    "order" bigint NOT NULL
);


ALTER TABLE public.charge_frequency_type OWNER TO postgres;

--
-- Name: charge_frequency_type_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.charge_frequency_type_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.charge_frequency_type_id_seq OWNER TO postgres;

--
-- Name: charge_frequency_type_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.charge_frequency_type_id_seq OWNED BY public.charge_frequency_type.id;


--
-- Name: charge_type; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.charge_type (
    id integer NOT NULL,
    name character varying(250) NOT NULL,
    "order" bigint NOT NULL
);


ALTER TABLE public.charge_type OWNER TO postgres;

--
-- Name: charge_type_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.charge_type_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.charge_type_id_seq OWNER TO postgres;

--
-- Name: charge_type_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.charge_type_id_seq OWNED BY public.charge_type.id;


--
-- Name: chart_type; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.chart_type (
    id integer NOT NULL,
    name character varying(250) NOT NULL,
    "order" bigint NOT NULL
);


ALTER TABLE public.chart_type OWNER TO postgres;

--
-- Name: chart_type_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.chart_type_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.chart_type_id_seq OWNER TO postgres;

--
-- Name: chart_type_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.chart_type_id_seq OWNED BY public.chart_type.id;


--
-- Name: form_value; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.form_value (
    id integer NOT NULL,
    number_configuration_mask character varying(250),
    formula_configuration character varying(1000),
    created_at timestamp with time zone NOT NULL,
    updated_at timestamp with time zone NOT NULL,
    value text,
    company_id integer,
    date_configuration_date_format_type_id integer,
    field_id integer,
    field_type_id integer,
    form_id integer,
    form_field_as_option_id integer,
    number_configuration_number_format_type_id integer,
    period_configuration_period_interval_type_id integer,
    is_long_text_rich_text boolean
);


ALTER TABLE public.form_value OWNER TO postgres;

--
-- Name: client_value_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.client_value_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.client_value_id_seq OWNER TO postgres;

--
-- Name: client_value_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.client_value_id_seq OWNED BY public.form_value.id;


--
-- Name: company; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.company (
    id integer NOT NULL,
    name character varying(400) NOT NULL,
    endpoint character varying(280) NOT NULL,
    updated_at timestamp with time zone NOT NULL,
    created_at timestamp with time zone NOT NULL,
    is_active boolean NOT NULL,
    partner character varying(500),
    company_type_id integer,
    shared_by_id integer,
    logo_image_bucket character varying(200) NOT NULL,
    logo_image_path character varying(250) NOT NULL,
    logo_image_url character varying(1000)
);


ALTER TABLE public.company OWNER TO postgres;

--
-- Name: companies_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.companies_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.companies_id_seq OWNER TO postgres;

--
-- Name: companies_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.companies_id_seq OWNED BY public.company.id;


--
-- Name: company_billing; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.company_billing (
    id integer NOT NULL,
    address character varying(500),
    zip_code character varying(500),
    street character varying(500),
    number integer,
    neighborhood character varying(500),
    country character varying(280),
    state character varying(280),
    city character varying(280),
    cnpj character varying(280),
    additional_details character varying(280),
    is_supercompany boolean NOT NULL,
    is_paying_company boolean NOT NULL,
    vindi_plan_id character varying(280),
    vindi_client_id character varying(280),
    vindi_product_id character varying(280),
    vindi_payment_profile_id character varying(280),
    vindi_signature_id character varying(280),
    charge_frequency_type_id integer,
    company_id integer NOT NULL,
    invoice_date_type_id integer,
    payment_method_type_id integer
);


ALTER TABLE public.company_billing OWNER TO postgres;

--
-- Name: company_billing_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.company_billing_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.company_billing_id_seq OWNER TO postgres;

--
-- Name: company_billing_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.company_billing_id_seq OWNED BY public.company_billing.id;


--
-- Name: company_charge; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.company_charge (
    id integer NOT NULL,
    updated_at timestamp with time zone NOT NULL,
    created_at timestamp with time zone NOT NULL,
    total_value numeric(10,2) NOT NULL,
    attempt_count integer NOT NULL,
    company_id integer NOT NULL
);


ALTER TABLE public.company_charge OWNER TO postgres;

--
-- Name: company_charge_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.company_charge_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.company_charge_id_seq OWNER TO postgres;

--
-- Name: company_charge_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.company_charge_id_seq OWNED BY public.company_charge.id;


--
-- Name: company_coupon; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.company_coupon (
    id integer NOT NULL,
    company_id integer NOT NULL,
    discount_coupon_id integer NOT NULL
);


ALTER TABLE public.company_coupon OWNER TO postgres;

--
-- Name: company_coupon_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.company_coupon_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.company_coupon_id_seq OWNER TO postgres;

--
-- Name: company_coupon_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.company_coupon_id_seq OWNED BY public.company_coupon.id;


--
-- Name: company_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.company_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.company_id_seq OWNER TO postgres;

--
-- Name: company_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.company_id_seq OWNED BY public.company.id;


--
-- Name: company_invoice_mails; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.company_invoice_mails (
    id integer NOT NULL,
    email character varying(254) NOT NULL,
    company_id integer NOT NULL
);


ALTER TABLE public.company_invoice_mails OWNER TO postgres;

--
-- Name: company_invoice_mails_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.company_invoice_mails_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.company_invoice_mails_id_seq OWNER TO postgres;

--
-- Name: company_invoice_mails_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.company_invoice_mails_id_seq OWNED BY public.company_invoice_mails.id;


--
-- Name: company_type; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.company_type (
    id integer NOT NULL,
    name character varying(200) NOT NULL,
    label_name character varying(200),
    "order" bigint NOT NULL
);


ALTER TABLE public.company_type OWNER TO postgres;

--
-- Name: theme_type; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.theme_type (
    id integer NOT NULL,
    name character varying(200) NOT NULL,
    label_name character varying(200),
    "order" bigint NOT NULL
);


ALTER TABLE public.theme_type OWNER TO postgres;

--
-- Name: company_type_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.company_type_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.company_type_id_seq OWNER TO postgres;

--
-- Name: company_type_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.company_type_id_seq OWNED BY public.theme_type.id;


--
-- Name: company_type_id_seq1; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.company_type_id_seq1
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.company_type_id_seq1 OWNER TO postgres;

--
-- Name: company_type_id_seq1; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.company_type_id_seq1 OWNED BY public.company_type.id;


--
-- Name: conditional_type; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.conditional_type (
    id integer NOT NULL,
    type character varying(150) NOT NULL,
    label_name character varying(250),
    "order" bigint NOT NULL
);


ALTER TABLE public.conditional_type OWNER TO postgres;

--
-- Name: conditional_type_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.conditional_type_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.conditional_type_id_seq OWNER TO postgres;

--
-- Name: conditional_type_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.conditional_type_id_seq OWNED BY public.conditional_type.id;


--
-- Name: current_company_charge; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.current_company_charge (
    id integer NOT NULL,
    updated_at timestamp with time zone NOT NULL,
    created_at timestamp with time zone NOT NULL,
    quantity integer NOT NULL,
    company_id integer NOT NULL,
    discount_by_individual_value_id integer,
    individual_charge_value_type_id integer NOT NULL
);


ALTER TABLE public.current_company_charge OWNER TO postgres;

--
-- Name: current_company_charge_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.current_company_charge_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.current_company_charge_id_seq OWNER TO postgres;

--
-- Name: current_company_charge_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.current_company_charge_id_seq OWNED BY public.current_company_charge.id;


--
-- Name: dashboard_chart_configuration; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.dashboard_chart_configuration (
    id integer NOT NULL,
    name character varying(350) NOT NULL,
    for_company boolean NOT NULL,
    aggregation_type_id integer NOT NULL,
    chart_type_id integer NOT NULL,
    company_id integer NOT NULL,
    form_id integer NOT NULL,
    label_field_id integer NOT NULL,
    number_format_type_id integer NOT NULL,
    user_id integer NOT NULL,
    value_field_id integer NOT NULL
);


ALTER TABLE public.dashboard_chart_configuration OWNER TO postgres;

--
-- Name: dashboard_chart_configuration_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.dashboard_chart_configuration_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.dashboard_chart_configuration_id_seq OWNER TO postgres;

--
-- Name: dashboard_chart_configuration_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.dashboard_chart_configuration_id_seq OWNED BY public.dashboard_chart_configuration.id;


--
-- Name: data_type_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.data_type_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.data_type_id_seq OWNER TO postgres;

--
-- Name: data_type_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.data_type_id_seq OWNED BY public.data_type.id;


--
-- Name: field_date_format_type; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.field_date_format_type (
    id integer NOT NULL,
    type character varying(200) NOT NULL,
    label_name character varying(250) NOT NULL,
    format character varying(250) NOT NULL,
    "order" bigint NOT NULL
);


ALTER TABLE public.field_date_format_type OWNER TO postgres;

--
-- Name: date_format_type_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.date_format_type_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.date_format_type_id_seq OWNER TO postgres;

--
-- Name: date_format_type_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.date_format_type_id_seq OWNED BY public.field_date_format_type.id;


--
-- Name: default_attachments; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.default_attachments (
    id integer NOT NULL,
    created_at timestamp with time zone NOT NULL,
    updated_at timestamp with time zone NOT NULL,
    file character varying(500),
    bucket character varying(200) NOT NULL,
    file_default_attachments_path character varying(250) NOT NULL,
    file_url character varying(1000),
    file_size bigint NOT NULL
);


ALTER TABLE public.default_attachments OWNER TO postgres;

--
-- Name: default_attachments_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.default_attachments_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.default_attachments_id_seq OWNER TO postgres;

--
-- Name: default_attachments_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.default_attachments_id_seq OWNED BY public.default_attachments.id;


--
-- Name: default_field_value; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.default_field_value (
    id integer NOT NULL,
    created_at timestamp with time zone NOT NULL,
    updated_at timestamp with time zone NOT NULL,
    value text NOT NULL,
    field_id integer NOT NULL,
    default_attachment_id integer
);


ALTER TABLE public.default_field_value OWNER TO postgres;

--
-- Name: default_field_value_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.default_field_value_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.default_field_value_id_seq OWNER TO postgres;

--
-- Name: default_field_value_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.default_field_value_id_seq OWNED BY public.default_field_value.id;


--
-- Name: discount_by_individual_name_for_company; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.discount_by_individual_name_for_company (
    id integer NOT NULL,
    value numeric(10,2) NOT NULL,
    name character varying(250) NOT NULL,
    company_id integer NOT NULL,
    individual_charge_value_type_id integer NOT NULL
);


ALTER TABLE public.discount_by_individual_name_for_company OWNER TO postgres;

--
-- Name: discount_by_individual_name_for_company_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.discount_by_individual_name_for_company_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.discount_by_individual_name_for_company_id_seq OWNER TO postgres;

--
-- Name: discount_by_individual_name_for_company_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.discount_by_individual_name_for_company_id_seq OWNED BY public.discount_by_individual_name_for_company.id;


--
-- Name: discount_by_individual_value_quantity; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.discount_by_individual_value_quantity (
    id integer NOT NULL,
    quantity integer NOT NULL,
    value numeric(10,2) NOT NULL,
    name character varying(250) NOT NULL,
    individual_charge_value_type_id integer NOT NULL
);


ALTER TABLE public.discount_by_individual_value_quantity OWNER TO postgres;

--
-- Name: discount_by_individual_value_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.discount_by_individual_value_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.discount_by_individual_value_id_seq OWNER TO postgres;

--
-- Name: discount_by_individual_value_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.discount_by_individual_value_id_seq OWNED BY public.discount_by_individual_value_quantity.id;


--
-- Name: discount_coupon; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.discount_coupon (
    id integer NOT NULL,
    name character varying(250) NOT NULL,
    value numeric(10,2) NOT NULL,
    permanent boolean NOT NULL,
    start_at timestamp with time zone,
    end_at timestamp with time zone
);


ALTER TABLE public.discount_coupon OWNER TO postgres;

--
-- Name: discount_coupon_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.discount_coupon_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.discount_coupon_id_seq OWNER TO postgres;

--
-- Name: discount_coupon_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.discount_coupon_id_seq OWNED BY public.discount_coupon.id;


--
-- Name: django_admin_log; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.django_admin_log (
    id integer NOT NULL,
    action_time timestamp with time zone NOT NULL,
    object_id text,
    object_repr character varying(200) NOT NULL,
    action_flag smallint NOT NULL,
    change_message text NOT NULL,
    content_type_id integer,
    user_id integer NOT NULL,
    CONSTRAINT django_admin_log_action_flag_check CHECK ((action_flag >= 0))
);


ALTER TABLE public.django_admin_log OWNER TO postgres;

--
-- Name: django_admin_log_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.django_admin_log_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.django_admin_log_id_seq OWNER TO postgres;

--
-- Name: django_admin_log_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.django_admin_log_id_seq OWNED BY public.django_admin_log.id;


--
-- Name: django_celery_results_taskresult; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.django_celery_results_taskresult (
    id integer NOT NULL,
    task_id character varying(255) NOT NULL,
    status character varying(50) NOT NULL,
    content_type character varying(128) NOT NULL,
    content_encoding character varying(64) NOT NULL,
    result text,
    date_done timestamp with time zone NOT NULL,
    traceback text,
    hidden boolean NOT NULL,
    meta text,
    task_args text,
    task_kwargs text,
    task_name character varying(255)
);


ALTER TABLE public.django_celery_results_taskresult OWNER TO postgres;

--
-- Name: django_celery_results_taskresult_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.django_celery_results_taskresult_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.django_celery_results_taskresult_id_seq OWNER TO postgres;

--
-- Name: django_celery_results_taskresult_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.django_celery_results_taskresult_id_seq OWNED BY public.django_celery_results_taskresult.id;


--
-- Name: django_content_type; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.django_content_type (
    id integer NOT NULL,
    app_label character varying(100) NOT NULL,
    model character varying(100) NOT NULL
);


ALTER TABLE public.django_content_type OWNER TO postgres;

--
-- Name: django_content_type_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.django_content_type_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.django_content_type_id_seq OWNER TO postgres;

--
-- Name: django_content_type_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.django_content_type_id_seq OWNED BY public.django_content_type.id;


--
-- Name: django_migrations; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.django_migrations (
    id integer NOT NULL,
    app character varying(255) NOT NULL,
    name character varying(255) NOT NULL,
    applied timestamp with time zone NOT NULL
);


ALTER TABLE public.django_migrations OWNER TO postgres;

--
-- Name: django_migrations_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.django_migrations_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.django_migrations_id_seq OWNER TO postgres;

--
-- Name: django_migrations_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.django_migrations_id_seq OWNED BY public.django_migrations.id;


--
-- Name: django_session; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.django_session (
    session_key character varying(40) NOT NULL,
    session_data text NOT NULL,
    expire_date timestamp with time zone NOT NULL
);


ALTER TABLE public.django_session OWNER TO postgres;

--
-- Name: draft; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.draft (
    id integer NOT NULL,
    created_at timestamp with time zone NOT NULL,
    updated_at timestamp with time zone NOT NULL,
    bucket character varying(200),
    file_draft_path character varying(250),
    file_url character varying(1000),
    file_size bigint,
    value text,
    company_id integer,
    draft_type_id integer NOT NULL,
    user_id integer,
    is_public boolean NOT NULL
);


ALTER TABLE public.draft OWNER TO postgres;

--
-- Name: draft_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.draft_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.draft_id_seq OWNER TO postgres;

--
-- Name: draft_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.draft_id_seq OWNED BY public.draft.id;


--
-- Name: draft_type; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.draft_type (
    id integer NOT NULL,
    name character varying(250) NOT NULL,
    "order" bigint NOT NULL
);


ALTER TABLE public.draft_type OWNER TO postgres;

--
-- Name: draft_type_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.draft_type_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.draft_type_id_seq OWNER TO postgres;

--
-- Name: draft_type_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.draft_type_id_seq OWNED BY public.draft_type.id;


--
-- Name: dynamic_forms; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.dynamic_forms (
    id integer NOT NULL,
    created_at timestamp with time zone NOT NULL,
    updated_at timestamp with time zone NOT NULL,
    company_id integer,
    depends_on_id integer,
    form_id integer NOT NULL,
    user_id integer,
    uuid uuid
);


ALTER TABLE public.dynamic_forms OWNER TO postgres;

--
-- Name: dynamic_forms_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.dynamic_forms_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.dynamic_forms_id_seq OWNER TO postgres;

--
-- Name: dynamic_forms_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.dynamic_forms_id_seq OWNED BY public.dynamic_forms.id;


--
-- Name: extract_file_data; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.extract_file_data (
    id integer NOT NULL,
    created_at timestamp with time zone NOT NULL,
    updated_at timestamp with time zone NOT NULL,
    file_id uuid NOT NULL,
    file text NOT NULL,
    file_format character varying(10) NOT NULL,
    company_id integer NOT NULL,
    form_id integer NOT NULL,
    user_id integer NOT NULL
);


ALTER TABLE public.extract_file_data OWNER TO postgres;

--
-- Name: extract_file_data_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.extract_file_data_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.extract_file_data_id_seq OWNER TO postgres;

--
-- Name: extract_file_data_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.extract_file_data_id_seq OWNED BY public.extract_file_data.id;


--
-- Name: field; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.field (
    id integer NOT NULL,
    number_configuration_mask character varying(250),
    formula_configuration character varying(1000),
    created_at timestamp with time zone NOT NULL,
    updated_at timestamp with time zone NOT NULL,
    name character varying(300) NOT NULL,
    label_name character varying(300),
    placeholder character varying(450),
    required boolean NOT NULL,
    "order" bigint NOT NULL,
    is_unique boolean NOT NULL,
    field_is_hidden boolean NOT NULL,
    label_is_hidden boolean NOT NULL,
    date_configuration_auto_create boolean NOT NULL,
    date_configuration_auto_update boolean NOT NULL,
    number_configuration_allow_negative boolean NOT NULL,
    number_configuration_allow_zero boolean NOT NULL,
    enabled boolean NOT NULL,
    date_configuration_date_format_type_id integer,
    form_id integer NOT NULL,
    form_field_as_option_id integer,
    number_configuration_number_format_type_id integer,
    period_configuration_period_interval_type_id integer,
    type_id integer NOT NULL,
    uuid uuid NOT NULL,
    is_long_text_rich_text boolean
);


ALTER TABLE public.field OWNER TO postgres;

--
-- Name: field_date_format_type_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.field_date_format_type_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.field_date_format_type_id_seq OWNER TO postgres;

--
-- Name: field_date_format_type_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.field_date_format_type_id_seq OWNED BY public.field_date_format_type.id;


--
-- Name: field_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.field_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.field_id_seq OWNER TO postgres;

--
-- Name: field_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.field_id_seq OWNED BY public.field.id;


--
-- Name: field_number_format_type; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.field_number_format_type (
    id integer NOT NULL,
    type character varying(200) NOT NULL,
    label_name character varying(250) NOT NULL,
    "precision" bigint NOT NULL,
    prefix character varying(250),
    suffix character varying(250),
    thousand_separator character varying(10),
    decimal_separator character varying(10),
    "order" bigint NOT NULL,
    base bigint NOT NULL,
    has_to_enforce_decimal boolean NOT NULL
);


ALTER TABLE public.field_number_format_type OWNER TO postgres;

--
-- Name: field_number_format_type_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.field_number_format_type_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.field_number_format_type_id_seq OWNER TO postgres;

--
-- Name: field_number_format_type_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.field_number_format_type_id_seq OWNED BY public.field_number_format_type.id;


--
-- Name: field_options; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.field_options (
    id integer NOT NULL,
    created_at timestamp with time zone NOT NULL,
    updated_at timestamp with time zone NOT NULL,
    option character varying(500) NOT NULL,
    "order" bigint NOT NULL,
    field_id integer NOT NULL,
    uuid uuid NOT NULL
);


ALTER TABLE public.field_options OWNER TO postgres;

--
-- Name: field_options_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.field_options_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.field_options_id_seq OWNER TO postgres;

--
-- Name: field_options_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.field_options_id_seq OWNED BY public.field_options.id;


--
-- Name: field_period_interval_type; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.field_period_interval_type (
    id integer NOT NULL,
    type character varying(200) NOT NULL,
    label_name character varying(250) NOT NULL,
    in_seconds bigint NOT NULL,
    "order" bigint NOT NULL
);


ALTER TABLE public.field_period_interval_type OWNER TO postgres;

--
-- Name: field_period_interval_type_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.field_period_interval_type_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.field_period_interval_type_id_seq OWNER TO postgres;

--
-- Name: field_period_interval_type_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.field_period_interval_type_id_seq OWNED BY public.field_period_interval_type.id;


--
-- Name: field_type; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.field_type (
    id integer NOT NULL,
    type character varying(200) NOT NULL,
    label_name character varying(250),
    "order" bigint NOT NULL,
    is_dynamic_evaluated boolean NOT NULL
);


ALTER TABLE public.field_type OWNER TO postgres;

--
-- Name: field_type_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.field_type_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.field_type_id_seq OWNER TO postgres;

--
-- Name: field_type_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.field_type_id_seq OWNED BY public.field_type.id;


--
-- Name: form; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.form (
    id integer NOT NULL,
    created_at timestamp with time zone NOT NULL,
    updated_at timestamp with time zone NOT NULL,
    form_name character varying(150) NOT NULL,
    label_name character varying(150) NOT NULL,
    "order" bigint NOT NULL,
    conditional_value character varying(200),
    enabled boolean NOT NULL,
    company_id integer NOT NULL,
    conditional_on_field_id integer,
    conditional_type_id integer,
    depends_on_id integer,
    group_id integer,
    type_id integer NOT NULL,
    uuid uuid NOT NULL,
    conditional_excludes_data_if_not_set boolean NOT NULL,
    show_label_name boolean NOT NULL
);


ALTER TABLE public.form OWNER TO postgres;

--
-- Name: form_accessed_by; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.form_accessed_by (
    id integer NOT NULL,
    created_at timestamp with time zone NOT NULL,
    updated_at timestamp with time zone NOT NULL,
    form_id integer NOT NULL,
    user_id integer NOT NULL
);


ALTER TABLE public.form_accessed_by OWNER TO postgres;

--
-- Name: form_accessed_by_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.form_accessed_by_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.form_accessed_by_id_seq OWNER TO postgres;

--
-- Name: form_accessed_by_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.form_accessed_by_id_seq OWNED BY public.form_accessed_by.id;


--
-- Name: form_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.form_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.form_id_seq OWNER TO postgres;

--
-- Name: form_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.form_id_seq OWNED BY public.form.id;


--
-- Name: form_type; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.form_type (
    id integer NOT NULL,
    type character varying(150) NOT NULL,
    label_name character varying(250),
    "order" bigint NOT NULL
);


ALTER TABLE public.form_type OWNER TO postgres;

--
-- Name: form_type_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.form_type_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.form_type_id_seq OWNER TO postgres;

--
-- Name: form_type_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.form_type_id_seq OWNED BY public.form_type.id;


--
-- Name: form_value_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.form_value_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.form_value_id_seq OWNER TO postgres;

--
-- Name: form_value_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.form_value_id_seq OWNED BY public.form_value.id;


--
-- Name: formula_attribute_type; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.formula_attribute_type (
    id integer NOT NULL,
    name character varying(280) NOT NULL,
    "order" integer NOT NULL
);


ALTER TABLE public.formula_attribute_type OWNER TO postgres;

--
-- Name: formula_attribute_type_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.formula_attribute_type_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.formula_attribute_type_id_seq OWNER TO postgres;

--
-- Name: formula_attribute_type_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.formula_attribute_type_id_seq OWNED BY public.formula_attribute_type.id;


--
-- Name: formula_context_attribute_type; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.formula_context_attribute_type (
    id integer NOT NULL,
    translation text NOT NULL,
    attribute_type_id integer NOT NULL,
    context_type_id integer NOT NULL
);


ALTER TABLE public.formula_context_attribute_type OWNER TO postgres;

--
-- Name: formula_context_attribute_type_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.formula_context_attribute_type_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.formula_context_attribute_type_id_seq OWNER TO postgres;

--
-- Name: formula_context_attribute_type_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.formula_context_attribute_type_id_seq OWNED BY public.formula_context_attribute_type.id;


--
-- Name: formula_context_for_company; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.formula_context_for_company (
    id integer NOT NULL,
    company_id integer NOT NULL,
    context_type_id integer NOT NULL
);


ALTER TABLE public.formula_context_for_company OWNER TO postgres;

--
-- Name: formula_context_for_company_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.formula_context_for_company_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.formula_context_for_company_id_seq OWNER TO postgres;

--
-- Name: formula_context_for_company_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.formula_context_for_company_id_seq OWNED BY public.formula_context_for_company.id;


--
-- Name: formula_context_type; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.formula_context_type (
    id integer NOT NULL,
    language character varying(280) NOT NULL,
    name character varying(280) NOT NULL,
    "order" integer NOT NULL
);


ALTER TABLE public.formula_context_type OWNER TO postgres;

--
-- Name: formula_context_type_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.formula_context_type_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.formula_context_type_id_seq OWNER TO postgres;

--
-- Name: formula_context_type_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.formula_context_type_id_seq OWNED BY public.formula_context_type.id;


--
-- Name: formula_parameters_type; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.formula_parameters_type (
    id integer NOT NULL,
    name character varying(250) NOT NULL,
    formula_type_id integer NOT NULL,
    raw_data_type_id integer,
    is_list boolean NOT NULL
);


ALTER TABLE public.formula_parameters_type OWNER TO postgres;

--
-- Name: formula_parameters_type_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.formula_parameters_type_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.formula_parameters_type_id_seq OWNER TO postgres;

--
-- Name: formula_parameters_type_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.formula_parameters_type_id_seq OWNED BY public.formula_parameters_type.id;


--
-- Name: formula_variable; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.formula_variable (
    id integer NOT NULL,
    "order" bigint NOT NULL,
    field_id integer NOT NULL,
    variable_id integer NOT NULL
);


ALTER TABLE public.formula_variable OWNER TO postgres;

--
-- Name: formula_variable_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.formula_variable_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.formula_variable_id_seq OWNER TO postgres;

--
-- Name: formula_variable_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.formula_variable_id_seq OWNED BY public.formula_variable.id;


--
-- Name: group; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public."group" (
    id integer NOT NULL,
    name character varying(500) NOT NULL,
    enabled boolean NOT NULL,
    "order" bigint NOT NULL,
    company_id integer NOT NULL
);


ALTER TABLE public."group" OWNER TO postgres;

--
-- Name: group_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.group_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.group_id_seq OWNER TO postgres;

--
-- Name: group_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.group_id_seq OWNED BY public."group".id;


--
-- Name: individual_charge_value_type; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.individual_charge_value_type (
    id integer NOT NULL,
    name character varying(250) NOT NULL,
    value numeric(10,2) NOT NULL,
    default_quantity integer,
    charge_frequency_type_id integer NOT NULL,
    charge_type_id integer NOT NULL,
    "order" bigint NOT NULL,
    charge_group_name character varying(250) NOT NULL
);


ALTER TABLE public.individual_charge_value_type OWNER TO postgres;

--
-- Name: individual_charge_value_type_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.individual_charge_value_type_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.individual_charge_value_type_id_seq OWNER TO postgres;

--
-- Name: individual_charge_value_type_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.individual_charge_value_type_id_seq OWNED BY public.individual_charge_value_type.id;


--
-- Name: invoice_date_type; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.invoice_date_type (
    id integer NOT NULL,
    date integer NOT NULL,
    "order" bigint NOT NULL
);


ALTER TABLE public.invoice_date_type OWNER TO postgres;

--
-- Name: invoice_date_type_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.invoice_date_type_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.invoice_date_type_id_seq OWNER TO postgres;

--
-- Name: invoice_date_type_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.invoice_date_type_id_seq OWNED BY public.invoice_date_type.id;


--
-- Name: kanban_card; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.kanban_card (
    id integer NOT NULL,
    created_at timestamp with time zone NOT NULL,
    updated_at timestamp with time zone NOT NULL,
    "default" boolean NOT NULL,
    user_id integer NOT NULL,
    company_id integer,
    form_id integer
);


ALTER TABLE public.kanban_card OWNER TO postgres;

--
-- Name: kanban_card_field; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.kanban_card_field (
    id integer NOT NULL,
    created_at timestamp with time zone NOT NULL,
    updated_at timestamp with time zone NOT NULL,
    field_id integer,
    kanban_card_id integer,
    "order" integer NOT NULL
);


ALTER TABLE public.kanban_card_field OWNER TO postgres;

--
-- Name: kanban_card_field_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.kanban_card_field_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.kanban_card_field_id_seq OWNER TO postgres;

--
-- Name: kanban_card_field_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.kanban_card_field_id_seq OWNED BY public.kanban_card_field.id;


--
-- Name: kanban_card_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.kanban_card_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.kanban_card_id_seq OWNER TO postgres;

--
-- Name: kanban_card_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.kanban_card_id_seq OWNED BY public.kanban_card.id;


--
-- Name: kanban_collapsed_option; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.kanban_collapsed_option (
    id integer NOT NULL,
    company_id integer NOT NULL,
    field_option_id integer NOT NULL,
    user_id integer NOT NULL
);


ALTER TABLE public.kanban_collapsed_option OWNER TO postgres;

--
-- Name: kanban_collapsed_option_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.kanban_collapsed_option_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.kanban_collapsed_option_id_seq OWNER TO postgres;

--
-- Name: kanban_collapsed_option_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.kanban_collapsed_option_id_seq OWNED BY public.kanban_collapsed_option.id;


--
-- Name: kanban_default; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.kanban_default (
    id integer NOT NULL,
    company_id integer NOT NULL,
    form_id integer NOT NULL,
    kanban_card_id integer,
    kanban_dimension_id integer,
    user_id integer NOT NULL
);


ALTER TABLE public.kanban_default OWNER TO postgres;

--
-- Name: kanban_default_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.kanban_default_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.kanban_default_id_seq OWNER TO postgres;

--
-- Name: kanban_default_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.kanban_default_id_seq OWNED BY public.kanban_default.id;


--
-- Name: kanban_dimension_order; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.kanban_dimension_order (
    id integer NOT NULL,
    created_at timestamp with time zone NOT NULL,
    updated_at timestamp with time zone NOT NULL,
    options character varying(500) NOT NULL,
    "order" bigint NOT NULL,
    "default" boolean NOT NULL,
    dimension_id integer,
    user_id integer NOT NULL
);


ALTER TABLE public.kanban_dimension_order OWNER TO postgres;

--
-- Name: kanban_dimension_order_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.kanban_dimension_order_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.kanban_dimension_order_id_seq OWNER TO postgres;

--
-- Name: kanban_dimension_order_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.kanban_dimension_order_id_seq OWNED BY public.kanban_dimension_order.id;


--
-- Name: listing_selected_fields; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.listing_selected_fields (
    id integer NOT NULL,
    field_id integer NOT NULL,
    user_id integer NOT NULL,
    is_selected boolean NOT NULL
);


ALTER TABLE public.listing_selected_fields OWNER TO postgres;

--
-- Name: listing_selected_fields_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.listing_selected_fields_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.listing_selected_fields_id_seq OWNER TO postgres;

--
-- Name: listing_selected_fields_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.listing_selected_fields_id_seq OWNED BY public.listing_selected_fields.id;


--
-- Name: notification; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.notification (
    id integer NOT NULL,
    created_at timestamp with time zone NOT NULL,
    updated_at timestamp with time zone NOT NULL,
    notification character varying(500) NOT NULL,
    form_id integer NOT NULL,
    notification_configuration_id integer,
    user_id integer
);


ALTER TABLE public.notification OWNER TO postgres;

--
-- Name: notification_configuration; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.notification_configuration (
    id integer NOT NULL,
    created_at timestamp with time zone NOT NULL,
    updated_at timestamp with time zone NOT NULL,
    for_company boolean NOT NULL,
    name character varying(500) NOT NULL,
    text character varying(500) NOT NULL,
    days_diff character varying(100) NOT NULL,
    field_id integer NOT NULL,
    form_id integer NOT NULL,
    user_id integer
);


ALTER TABLE public.notification_configuration OWNER TO postgres;

--
-- Name: notification_configuration_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.notification_configuration_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.notification_configuration_id_seq OWNER TO postgres;

--
-- Name: notification_configuration_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.notification_configuration_id_seq OWNED BY public.notification_configuration.id;


--
-- Name: notification_configuration_variable; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.notification_configuration_variable (
    id integer NOT NULL,
    field_id integer NOT NULL,
    notification_configuration_id integer NOT NULL,
    "order" bigint NOT NULL
);


ALTER TABLE public.notification_configuration_variable OWNER TO postgres;

--
-- Name: notification_configuration_variable_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.notification_configuration_variable_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.notification_configuration_variable_id_seq OWNER TO postgres;

--
-- Name: notification_configuration_variable_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.notification_configuration_variable_id_seq OWNED BY public.notification_configuration_variable.id;


--
-- Name: notification_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.notification_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.notification_id_seq OWNER TO postgres;

--
-- Name: notification_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.notification_id_seq OWNED BY public.notification.id;


--
-- Name: option_accessed_by; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.option_accessed_by (
    id integer NOT NULL,
    created_at timestamp with time zone NOT NULL,
    updated_at timestamp with time zone NOT NULL,
    field_option_id integer NOT NULL,
    user_id integer NOT NULL
);


ALTER TABLE public.option_accessed_by OWNER TO postgres;

--
-- Name: option_accessed_by_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.option_accessed_by_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.option_accessed_by_id_seq OWNER TO postgres;

--
-- Name: option_accessed_by_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.option_accessed_by_id_seq OWNED BY public.option_accessed_by.id;


--
-- Name: partner_default_and_discounts; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.partner_default_and_discounts (
    id integer NOT NULL,
    partner_name character varying(200) NOT NULL,
    discount_value numeric(10,2) NOT NULL,
    default_quantity integer,
    individual_charge_value_type_id integer NOT NULL
);


ALTER TABLE public.partner_default_and_discounts OWNER TO postgres;

--
-- Name: partner_default_and_discounts_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.partner_default_and_discounts_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.partner_default_and_discounts_id_seq OWNER TO postgres;

--
-- Name: partner_default_and_discounts_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.partner_default_and_discounts_id_seq OWNED BY public.partner_default_and_discounts.id;


--
-- Name: payment_method_type; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.payment_method_type (
    id integer NOT NULL,
    name character varying(250) NOT NULL,
    "order" bigint NOT NULL
);


ALTER TABLE public.payment_method_type OWNER TO postgres;

--
-- Name: payment_method_type_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.payment_method_type_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.payment_method_type_id_seq OWNER TO postgres;

--
-- Name: payment_method_type_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.payment_method_type_id_seq OWNED BY public.payment_method_type.id;


--
-- Name: pdf_generated; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.pdf_generated (
    id integer NOT NULL,
    created_at timestamp with time zone NOT NULL,
    updated_at timestamp with time zone NOT NULL,
    company_id integer NOT NULL,
    pdf_template_id integer NOT NULL,
    user_id integer NOT NULL
);


ALTER TABLE public.pdf_generated OWNER TO postgres;

--
-- Name: pdf_generated_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.pdf_generated_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.pdf_generated_id_seq OWNER TO postgres;

--
-- Name: pdf_generated_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.pdf_generated_id_seq OWNED BY public.pdf_generated.id;


--
-- Name: pdf_template_allowed_text_block; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.pdf_template_allowed_text_block (
    id integer NOT NULL,
    block_id integer NOT NULL
);


ALTER TABLE public.pdf_template_allowed_text_block OWNER TO postgres;

--
-- Name: pdf_template_allowed_text_block_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.pdf_template_allowed_text_block_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.pdf_template_allowed_text_block_id_seq OWNER TO postgres;

--
-- Name: pdf_template_allowed_text_block_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.pdf_template_allowed_text_block_id_seq OWNED BY public.pdf_template_allowed_text_block.id;


--
-- Name: pdf_template_configuration; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.pdf_template_configuration (
    id integer NOT NULL,
    created_at timestamp with time zone NOT NULL,
    updated_at timestamp with time zone NOT NULL,
    name character varying(500) NOT NULL,
    company_id integer NOT NULL,
    form_id integer NOT NULL,
    user_id integer NOT NULL,
    rich_text_page_id integer
);


ALTER TABLE public.pdf_template_configuration OWNER TO postgres;

--
-- Name: pdf_template_configuration_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.pdf_template_configuration_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.pdf_template_configuration_id_seq OWNER TO postgres;

--
-- Name: pdf_template_configuration_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.pdf_template_configuration_id_seq OWNED BY public.pdf_template_configuration.id;


--
-- Name: pdf_template_configuration_variables; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.pdf_template_configuration_variables (
    id integer NOT NULL,
    field_id integer NOT NULL,
    pdf_template_id integer NOT NULL
);


ALTER TABLE public.pdf_template_configuration_variables OWNER TO postgres;

--
-- Name: pdf_template_configuration_variables_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.pdf_template_configuration_variables_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.pdf_template_configuration_variables_id_seq OWNER TO postgres;

--
-- Name: pdf_template_configuration_variables_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.pdf_template_configuration_variables_id_seq OWNED BY public.pdf_template_configuration_variables.id;


--
-- Name: period_interval_type_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.period_interval_type_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.period_interval_type_id_seq OWNER TO postgres;

--
-- Name: period_interval_type_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.period_interval_type_id_seq OWNED BY public.field_period_interval_type.id;


--
-- Name: pre_notification; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.pre_notification (
    id integer NOT NULL,
    "when" timestamp with time zone NOT NULL,
    notification_configuration_id integer NOT NULL,
    user_id integer NOT NULL,
    dynamic_form_id integer NOT NULL,
    has_sent boolean NOT NULL,
    is_sending boolean NOT NULL
);


ALTER TABLE public.pre_notification OWNER TO postgres;

--
-- Name: pre_notification_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.pre_notification_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.pre_notification_id_seq OWNER TO postgres;

--
-- Name: pre_notification_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.pre_notification_id_seq OWNED BY public.pre_notification.id;


--
-- Name: profiles; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.profiles (
    id integer NOT NULL,
    name character varying(200) NOT NULL,
    label_name character varying(200),
    can_edit boolean NOT NULL,
    "order" bigint NOT NULL
);


ALTER TABLE public.profiles OWNER TO postgres;

--
-- Name: profiles_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.profiles_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.profiles_id_seq OWNER TO postgres;

--
-- Name: profiles_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.profiles_id_seq OWNED BY public.profiles.id;


--
-- Name: public_access; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.public_access (
    id integer NOT NULL,
    public_key uuid,
    company_id integer NOT NULL,
    user_id integer NOT NULL
);


ALTER TABLE public.public_access OWNER TO postgres;

--
-- Name: public_access_field; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.public_access_field (
    id integer NOT NULL,
    field_id integer NOT NULL,
    public_access_id integer NOT NULL,
    public_form_id integer NOT NULL
);


ALTER TABLE public.public_access_field OWNER TO postgres;

--
-- Name: public_access_form; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.public_access_form (
    id integer NOT NULL,
    form_id integer NOT NULL,
    public_access_id integer NOT NULL,
    description_message text,
    greetings_message text,
    is_to_submit_another_response_button boolean NOT NULL
);


ALTER TABLE public.public_access_form OWNER TO postgres;

--
-- Name: public_access_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.public_access_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.public_access_id_seq OWNER TO postgres;

--
-- Name: public_access_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.public_access_id_seq OWNED BY public.public_access.id;


--
-- Name: public_field_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.public_field_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.public_field_id_seq OWNER TO postgres;

--
-- Name: public_field_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.public_field_id_seq OWNED BY public.public_access_field.id;


--
-- Name: public_form_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.public_form_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.public_form_id_seq OWNER TO postgres;

--
-- Name: public_form_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.public_form_id_seq OWNED BY public.public_access_form.id;


--
-- Name: push_notification; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.push_notification (
    id integer NOT NULL,
    token character varying(1000) NOT NULL,
    endpoint character varying(1000) NOT NULL,
    push_notification_tag_type_id integer NOT NULL,
    user_id integer NOT NULL
);


ALTER TABLE public.push_notification OWNER TO postgres;

--
-- Name: push_notification_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.push_notification_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.push_notification_id_seq OWNER TO postgres;

--
-- Name: push_notification_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.push_notification_id_seq OWNED BY public.push_notification.id;


--
-- Name: push_notification_tag_type; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.push_notification_tag_type (
    id integer NOT NULL,
    name character varying(100) NOT NULL,
    "order" bigint NOT NULL
);


ALTER TABLE public.push_notification_tag_type OWNER TO postgres;

--
-- Name: push_notification_tag_type_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.push_notification_tag_type_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.push_notification_tag_type_id_seq OWNER TO postgres;

--
-- Name: push_notification_tag_type_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.push_notification_tag_type_id_seq OWNED BY public.push_notification_tag_type.id;


--
-- Name: raw_data_type; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.raw_data_type (
    id integer NOT NULL,
    type character varying(20) NOT NULL
);


ALTER TABLE public.raw_data_type OWNER TO postgres;

--
-- Name: raw_data_type_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.raw_data_type_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.raw_data_type_id_seq OWNER TO postgres;

--
-- Name: raw_data_type_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.raw_data_type_id_seq OWNED BY public.raw_data_type.id;


--
-- Name: user_notification; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.user_notification (
    id integer NOT NULL,
    created_at timestamp with time zone NOT NULL,
    updated_at timestamp with time zone NOT NULL,
    notification_id integer NOT NULL,
    user_id integer,
    has_read boolean NOT NULL,
    is_new boolean NOT NULL
);


ALTER TABLE public.user_notification OWNER TO postgres;

--
-- Name: read_notification_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.read_notification_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.read_notification_id_seq OWNER TO postgres;

--
-- Name: read_notification_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.read_notification_id_seq OWNED BY public.user_notification.id;


--
-- Name: text_alignment_type; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.text_alignment_type (
    id integer NOT NULL,
    name character varying(250) NOT NULL,
    "order" bigint NOT NULL
);


ALTER TABLE public.text_alignment_type OWNER TO postgres;

--
-- Name: text_alignment_type_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.text_alignment_type_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.text_alignment_type_id_seq OWNER TO postgres;

--
-- Name: text_alignment_type_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.text_alignment_type_id_seq OWNED BY public.text_alignment_type.id;


--
-- Name: text_block; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.text_block (
    id integer NOT NULL,
    created_at timestamp with time zone NOT NULL,
    updated_at timestamp with time zone NOT NULL,
    "order" bigint NOT NULL,
    block_type_id integer NOT NULL,
    depends_on_id integer,
    image_option_id integer,
    list_option_id integer,
    page_id integer NOT NULL,
    table_option_id integer,
    text_option_id integer,
    uuid uuid NOT NULL
);


ALTER TABLE public.text_block OWNER TO postgres;

--
-- Name: text_block_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.text_block_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.text_block_id_seq OWNER TO postgres;

--
-- Name: text_block_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.text_block_id_seq OWNED BY public.text_block.id;


--
-- Name: text_block_type; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.text_block_type (
    id integer NOT NULL,
    name character varying(250) NOT NULL,
    is_primitive boolean NOT NULL,
    "order" bigint NOT NULL
);


ALTER TABLE public.text_block_type OWNER TO postgres;

--
-- Name: text_block_type_can_contain_type; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.text_block_type_can_contain_type (
    id integer NOT NULL,
    block_id integer NOT NULL,
    contain_id integer NOT NULL
);


ALTER TABLE public.text_block_type_can_contain_type OWNER TO postgres;

--
-- Name: text_block_type_can_contain_type_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.text_block_type_can_contain_type_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.text_block_type_can_contain_type_id_seq OWNER TO postgres;

--
-- Name: text_block_type_can_contain_type_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.text_block_type_can_contain_type_id_seq OWNED BY public.text_block_type_can_contain_type.id;


--
-- Name: text_block_type_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.text_block_type_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.text_block_type_id_seq OWNER TO postgres;

--
-- Name: text_block_type_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.text_block_type_id_seq OWNED BY public.text_block_type.id;


--
-- Name: text_content; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.text_content (
    id integer NOT NULL,
    created_at timestamp with time zone NOT NULL,
    updated_at timestamp with time zone NOT NULL,
    "order" bigint NOT NULL,
    text text,
    is_bold boolean NOT NULL,
    is_italic boolean NOT NULL,
    is_underline boolean NOT NULL,
    is_code boolean NOT NULL,
    latex_equation text,
    marker_color character varying(150),
    text_color character varying(150),
    block_id integer NOT NULL,
    link text,
    uuid uuid NOT NULL,
    custom_value text,
    is_custom boolean NOT NULL,
    text_size integer NOT NULL
);


ALTER TABLE public.text_content OWNER TO postgres;

--
-- Name: text_content_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.text_content_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.text_content_id_seq OWNER TO postgres;

--
-- Name: text_content_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.text_content_id_seq OWNED BY public.text_content.id;


--
-- Name: text_image_option; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.text_image_option (
    id integer NOT NULL,
    link text,
    bucket character varying(200),
    file_image_path character varying(250),
    file_name text,
    file_size bigint,
    file_url character varying(1000),
    size_relative_to_view numeric(25,20) NOT NULL,
    file_image_uuid uuid NOT NULL
);


ALTER TABLE public.text_image_option OWNER TO postgres;

--
-- Name: text_image_option_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.text_image_option_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.text_image_option_id_seq OWNER TO postgres;

--
-- Name: text_image_option_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.text_image_option_id_seq OWNED BY public.text_image_option.id;


--
-- Name: text_list_option; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.text_list_option (
    id integer NOT NULL,
    list_type_id integer NOT NULL
);


ALTER TABLE public.text_list_option OWNER TO postgres;

--
-- Name: text_list_option_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.text_list_option_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.text_list_option_id_seq OWNER TO postgres;

--
-- Name: text_list_option_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.text_list_option_id_seq OWNED BY public.text_list_option.id;


--
-- Name: text_list_type; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.text_list_type (
    id integer NOT NULL,
    name character varying(250) NOT NULL,
    "order" bigint NOT NULL
);


ALTER TABLE public.text_list_type OWNER TO postgres;

--
-- Name: text_list_type_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.text_list_type_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.text_list_type_id_seq OWNER TO postgres;

--
-- Name: text_list_type_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.text_list_type_id_seq OWNED BY public.text_list_type.id;


--
-- Name: text_page; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.text_page (
    id integer NOT NULL,
    created_at timestamp with time zone NOT NULL,
    updated_at timestamp with time zone NOT NULL,
    raw_text text,
    markdown_text text,
    company_id integer,
    user_id integer
);


ALTER TABLE public.text_page OWNER TO postgres;

--
-- Name: text_page_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.text_page_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.text_page_id_seq OWNER TO postgres;

--
-- Name: text_page_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.text_page_id_seq OWNED BY public.text_page.id;


--
-- Name: text_table_option; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.text_table_option (
    id integer NOT NULL,
    border_color character varying(150)
);


ALTER TABLE public.text_table_option OWNER TO postgres;

--
-- Name: text_table_option_column_dimension; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.text_table_option_column_dimension (
    id integer NOT NULL,
    width double precision,
    text_table_option_id integer NOT NULL,
    "order" bigint NOT NULL
);


ALTER TABLE public.text_table_option_column_dimension OWNER TO postgres;

--
-- Name: text_table_option_column_dimension_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.text_table_option_column_dimension_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.text_table_option_column_dimension_id_seq OWNER TO postgres;

--
-- Name: text_table_option_column_dimension_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.text_table_option_column_dimension_id_seq OWNED BY public.text_table_option_column_dimension.id;


--
-- Name: text_table_option_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.text_table_option_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.text_table_option_id_seq OWNER TO postgres;

--
-- Name: text_table_option_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.text_table_option_id_seq OWNED BY public.text_table_option.id;


--
-- Name: text_table_option_row_dimension; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.text_table_option_row_dimension (
    id integer NOT NULL,
    height bigint,
    text_table_option_id integer NOT NULL,
    "order" bigint NOT NULL
);


ALTER TABLE public.text_table_option_row_dimension OWNER TO postgres;

--
-- Name: text_table_option_row_dimension_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.text_table_option_row_dimension_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.text_table_option_row_dimension_id_seq OWNER TO postgres;

--
-- Name: text_table_option_row_dimension_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.text_table_option_row_dimension_id_seq OWNED BY public.text_table_option_row_dimension.id;


--
-- Name: text_text_option; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.text_text_option (
    id integer NOT NULL,
    alignment_type_id integer NOT NULL
);


ALTER TABLE public.text_text_option OWNER TO postgres;

--
-- Name: text_text_option_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.text_text_option_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.text_text_option_id_seq OWNER TO postgres;

--
-- Name: text_text_option_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.text_text_option_id_seq OWNED BY public.text_text_option.id;


--
-- Name: theme; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.theme (
    id integer NOT NULL,
    display_name character varying(300) NOT NULL,
    created_at timestamp with time zone NOT NULL,
    theme_type_id integer,
    user_id integer,
    description character varying(500) NOT NULL,
    is_public boolean NOT NULL,
    company_id integer
);


ALTER TABLE public.theme OWNER TO postgres;

--
-- Name: theme_dashboard_chart_configuration; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.theme_dashboard_chart_configuration (
    id integer NOT NULL,
    name character varying(350) NOT NULL,
    for_company boolean NOT NULL,
    aggregation_type_id integer NOT NULL,
    chart_type_id integer NOT NULL,
    form_id integer NOT NULL,
    label_field_id integer NOT NULL,
    number_format_type_id integer NOT NULL,
    theme_id integer NOT NULL,
    value_field_id integer NOT NULL
);


ALTER TABLE public.theme_dashboard_chart_configuration OWNER TO postgres;

--
-- Name: theme_dashboard_chart_configuration_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.theme_dashboard_chart_configuration_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.theme_dashboard_chart_configuration_id_seq OWNER TO postgres;

--
-- Name: theme_dashboard_chart_configuration_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.theme_dashboard_chart_configuration_id_seq OWNED BY public.theme_dashboard_chart_configuration.id;


--
-- Name: theme_field; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.theme_field (
    id integer NOT NULL,
    created_at timestamp with time zone NOT NULL,
    updated_at timestamp with time zone NOT NULL,
    name character varying(300) NOT NULL,
    label_name character varying(300),
    placeholder character varying(450),
    required boolean NOT NULL,
    "order" bigint NOT NULL,
    label_is_hidden boolean NOT NULL,
    form_id integer,
    form_field_as_option_id integer,
    type_id integer NOT NULL,
    field_is_hidden boolean NOT NULL,
    is_unique boolean NOT NULL,
    number_configuration_mask character varying(250),
    date_configuration_auto_create boolean NOT NULL,
    date_configuration_auto_update boolean NOT NULL,
    date_configuration_date_format_type_id integer,
    period_configuration_period_interval_type_id integer,
    formula_configuration character varying(1000),
    number_configuration_allow_negative boolean NOT NULL,
    number_configuration_allow_zero boolean NOT NULL,
    number_configuration_number_format_type_id integer,
    uuid uuid NOT NULL,
    is_long_text_rich_text boolean
);


ALTER TABLE public.theme_field OWNER TO postgres;

--
-- Name: theme_field_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.theme_field_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.theme_field_id_seq OWNER TO postgres;

--
-- Name: theme_field_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.theme_field_id_seq OWNED BY public.theme_field.id;


--
-- Name: theme_field_options; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.theme_field_options (
    id integer NOT NULL,
    created_at timestamp with time zone NOT NULL,
    updated_at timestamp with time zone NOT NULL,
    option character varying(500) NOT NULL,
    "order" bigint NOT NULL,
    field_id integer,
    uuid uuid NOT NULL
);


ALTER TABLE public.theme_field_options OWNER TO postgres;

--
-- Name: theme_field_options_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.theme_field_options_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.theme_field_options_id_seq OWNER TO postgres;

--
-- Name: theme_field_options_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.theme_field_options_id_seq OWNED BY public.theme_field_options.id;


--
-- Name: theme_form; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.theme_form (
    id integer NOT NULL,
    created_at timestamp with time zone NOT NULL,
    updated_at timestamp with time zone NOT NULL,
    form_name character varying(150) NOT NULL,
    label_name character varying(150) NOT NULL,
    "order" bigint NOT NULL,
    conditional_value character varying(200),
    conditional_on_field_id integer,
    conditional_type_id integer,
    depends_on_id integer,
    theme_id integer NOT NULL,
    type_id integer NOT NULL,
    form_id bigint,
    uuid uuid NOT NULL,
    conditional_excludes_data_if_not_set boolean NOT NULL,
    show_label_name boolean NOT NULL
);


ALTER TABLE public.theme_form OWNER TO postgres;

--
-- Name: theme_form_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.theme_form_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.theme_form_id_seq OWNER TO postgres;

--
-- Name: theme_form_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.theme_form_id_seq OWNED BY public.theme_form.id;


--
-- Name: theme_formula_variable; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.theme_formula_variable (
    id integer NOT NULL,
    "order" bigint NOT NULL,
    field_id integer NOT NULL,
    variable_id integer NOT NULL
);


ALTER TABLE public.theme_formula_variable OWNER TO postgres;

--
-- Name: theme_formula_variable_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.theme_formula_variable_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.theme_formula_variable_id_seq OWNER TO postgres;

--
-- Name: theme_formula_variable_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.theme_formula_variable_id_seq OWNED BY public.theme_formula_variable.id;


--
-- Name: theme_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.theme_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.theme_id_seq OWNER TO postgres;

--
-- Name: theme_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.theme_id_seq OWNED BY public.theme.id;


--
-- Name: theme_kanban_card; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.theme_kanban_card (
    id integer NOT NULL,
    created_at timestamp with time zone NOT NULL,
    updated_at timestamp with time zone NOT NULL,
    "default" boolean NOT NULL,
    theme_id integer NOT NULL
);


ALTER TABLE public.theme_kanban_card OWNER TO postgres;

--
-- Name: theme_kanban_card_field; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.theme_kanban_card_field (
    id integer NOT NULL,
    created_at timestamp with time zone NOT NULL,
    updated_at timestamp with time zone NOT NULL,
    field_id integer,
    kanban_card_id integer,
    "order" integer NOT NULL
);


ALTER TABLE public.theme_kanban_card_field OWNER TO postgres;

--
-- Name: theme_kanban_card_field_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.theme_kanban_card_field_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.theme_kanban_card_field_id_seq OWNER TO postgres;

--
-- Name: theme_kanban_card_field_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.theme_kanban_card_field_id_seq OWNED BY public.theme_kanban_card_field.id;


--
-- Name: theme_kanban_card_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.theme_kanban_card_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.theme_kanban_card_id_seq OWNER TO postgres;

--
-- Name: theme_kanban_card_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.theme_kanban_card_id_seq OWNED BY public.theme_kanban_card.id;


--
-- Name: theme_kanban_default; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.theme_kanban_default (
    id integer NOT NULL,
    form_id integer NOT NULL,
    kanban_card_id integer,
    kanban_dimension_id integer,
    theme_id integer NOT NULL
);


ALTER TABLE public.theme_kanban_default OWNER TO postgres;

--
-- Name: theme_kanban_default_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.theme_kanban_default_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.theme_kanban_default_id_seq OWNER TO postgres;

--
-- Name: theme_kanban_default_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.theme_kanban_default_id_seq OWNED BY public.theme_kanban_default.id;


--
-- Name: theme_kanban_dimension_order; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.theme_kanban_dimension_order (
    id integer NOT NULL,
    created_at timestamp with time zone NOT NULL,
    updated_at timestamp with time zone NOT NULL,
    options character varying(500) NOT NULL,
    "order" bigint NOT NULL,
    "default" boolean NOT NULL,
    dimension_id integer,
    theme_id integer NOT NULL
);


ALTER TABLE public.theme_kanban_dimension_order OWNER TO postgres;

--
-- Name: theme_kanban_dimension_order_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.theme_kanban_dimension_order_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.theme_kanban_dimension_order_id_seq OWNER TO postgres;

--
-- Name: theme_kanban_dimension_order_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.theme_kanban_dimension_order_id_seq OWNED BY public.theme_kanban_dimension_order.id;


--
-- Name: theme_notification_configuration; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.theme_notification_configuration (
    id integer NOT NULL,
    created_at timestamp with time zone NOT NULL,
    updated_at timestamp with time zone NOT NULL,
    for_company boolean NOT NULL,
    name character varying(500) NOT NULL,
    text character varying(500) NOT NULL,
    days_diff character varying(100) NOT NULL,
    field_id integer NOT NULL,
    form_id integer NOT NULL
);


ALTER TABLE public.theme_notification_configuration OWNER TO postgres;

--
-- Name: theme_notification_configuration_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.theme_notification_configuration_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.theme_notification_configuration_id_seq OWNER TO postgres;

--
-- Name: theme_notification_configuration_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.theme_notification_configuration_id_seq OWNED BY public.theme_notification_configuration.id;


--
-- Name: theme_notification_configuration_variable; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.theme_notification_configuration_variable (
    id integer NOT NULL,
    "order" bigint NOT NULL,
    field_id integer NOT NULL,
    notification_configuration_id integer NOT NULL
);


ALTER TABLE public.theme_notification_configuration_variable OWNER TO postgres;

--
-- Name: theme_notification_configuration_variable_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.theme_notification_configuration_variable_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.theme_notification_configuration_variable_id_seq OWNER TO postgres;

--
-- Name: theme_notification_configuration_variable_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.theme_notification_configuration_variable_id_seq OWNED BY public.theme_notification_configuration_variable.id;


--
-- Name: theme_photos; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.theme_photos (
    id integer NOT NULL,
    image_name character varying(300) NOT NULL,
    url character varying(1000) NOT NULL,
    theme_id integer NOT NULL
);


ALTER TABLE public.theme_photos OWNER TO postgres;

--
-- Name: theme_photos_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.theme_photos_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.theme_photos_id_seq OWNER TO postgres;

--
-- Name: theme_photos_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.theme_photos_id_seq OWNED BY public.theme_photos.id;


--
-- Name: user_accessed_by; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.user_accessed_by (
    id integer NOT NULL,
    created_at timestamp with time zone NOT NULL,
    updated_at timestamp with time zone NOT NULL,
    field_id integer NOT NULL,
    user_id integer NOT NULL,
    user_option_id integer NOT NULL
);


ALTER TABLE public.user_accessed_by OWNER TO postgres;

--
-- Name: user_accessed_by_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.user_accessed_by_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.user_accessed_by_id_seq OWNER TO postgres;

--
-- Name: user_accessed_by_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.user_accessed_by_id_seq OWNED BY public.user_accessed_by.id;


--
-- Name: users; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.users (
    id integer NOT NULL,
    password character varying(128) NOT NULL,
    last_login timestamp with time zone,
    is_superuser boolean NOT NULL,
    username character varying(150) NOT NULL,
    first_name character varying(150) NOT NULL,
    last_name character varying(150) NOT NULL,
    email character varying(254) NOT NULL,
    is_staff boolean NOT NULL,
    is_active boolean NOT NULL,
    date_joined timestamp with time zone NOT NULL,
    phone character varying(250),
    timezone integer NOT NULL,
    is_admin boolean NOT NULL,
    temp_password character varying(250),
    company_id integer NOT NULL,
    data_type_id integer,
    profile_id integer NOT NULL
);


ALTER TABLE public.users OWNER TO postgres;

--
-- Name: users_groups; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.users_groups (
    id integer NOT NULL,
    userextended_id integer NOT NULL,
    group_id integer NOT NULL
);


ALTER TABLE public.users_groups OWNER TO postgres;

--
-- Name: users_groups_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.users_groups_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.users_groups_id_seq OWNER TO postgres;

--
-- Name: users_groups_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.users_groups_id_seq OWNED BY public.users_groups.id;


--
-- Name: users_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.users_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.users_id_seq OWNER TO postgres;

--
-- Name: users_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.users_id_seq OWNED BY public.users.id;


--
-- Name: users_user_permissions; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.users_user_permissions (
    id integer NOT NULL,
    userextended_id integer NOT NULL,
    permission_id integer NOT NULL
);


ALTER TABLE public.users_user_permissions OWNER TO postgres;

--
-- Name: users_user_permissions_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.users_user_permissions_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.users_user_permissions_id_seq OWNER TO postgres;

--
-- Name: users_user_permissions_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.users_user_permissions_id_seq OWNED BY public.users_user_permissions.id;


--
-- Name: address_helper id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.address_helper ALTER COLUMN id SET DEFAULT nextval('public.address_type_id_seq'::regclass);


--
-- Name: aggregation_type id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.aggregation_type ALTER COLUMN id SET DEFAULT nextval('public.aggregation_type_id_seq'::regclass);


--
-- Name: attachments id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.attachments ALTER COLUMN id SET DEFAULT nextval('public.attachments_id_seq'::regclass);


--
-- Name: auth_group id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.auth_group ALTER COLUMN id SET DEFAULT nextval('public.auth_group_id_seq'::regclass);


--
-- Name: auth_group_permissions id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.auth_group_permissions ALTER COLUMN id SET DEFAULT nextval('public.auth_group_permissions_id_seq'::regclass);


--
-- Name: auth_permission id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.auth_permission ALTER COLUMN id SET DEFAULT nextval('public.auth_permission_id_seq'::regclass);


--
-- Name: charge_frequency_type id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.charge_frequency_type ALTER COLUMN id SET DEFAULT nextval('public.charge_frequency_type_id_seq'::regclass);


--
-- Name: charge_type id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.charge_type ALTER COLUMN id SET DEFAULT nextval('public.charge_type_id_seq'::regclass);


--
-- Name: chart_type id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.chart_type ALTER COLUMN id SET DEFAULT nextval('public.chart_type_id_seq'::regclass);


--
-- Name: company id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.company ALTER COLUMN id SET DEFAULT nextval('public.companies_id_seq'::regclass);


--
-- Name: company_billing id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.company_billing ALTER COLUMN id SET DEFAULT nextval('public.company_billing_id_seq'::regclass);


--
-- Name: company_charge id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.company_charge ALTER COLUMN id SET DEFAULT nextval('public.company_charge_id_seq'::regclass);


--
-- Name: company_coupon id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.company_coupon ALTER COLUMN id SET DEFAULT nextval('public.company_coupon_id_seq'::regclass);


--
-- Name: company_invoice_mails id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.company_invoice_mails ALTER COLUMN id SET DEFAULT nextval('public.company_invoice_mails_id_seq'::regclass);


--
-- Name: company_type id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.company_type ALTER COLUMN id SET DEFAULT nextval('public.company_type_id_seq1'::regclass);


--
-- Name: conditional_type id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.conditional_type ALTER COLUMN id SET DEFAULT nextval('public.conditional_type_id_seq'::regclass);


--
-- Name: current_company_charge id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.current_company_charge ALTER COLUMN id SET DEFAULT nextval('public.current_company_charge_id_seq'::regclass);


--
-- Name: dashboard_chart_configuration id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.dashboard_chart_configuration ALTER COLUMN id SET DEFAULT nextval('public.dashboard_chart_configuration_id_seq'::regclass);


--
-- Name: data_type id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.data_type ALTER COLUMN id SET DEFAULT nextval('public.app_id_seq'::regclass);


--
-- Name: default_attachments id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.default_attachments ALTER COLUMN id SET DEFAULT nextval('public.default_attachments_id_seq'::regclass);


--
-- Name: default_field_value id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.default_field_value ALTER COLUMN id SET DEFAULT nextval('public.default_field_value_id_seq'::regclass);


--
-- Name: discount_by_individual_name_for_company id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.discount_by_individual_name_for_company ALTER COLUMN id SET DEFAULT nextval('public.discount_by_individual_name_for_company_id_seq'::regclass);


--
-- Name: discount_by_individual_value_quantity id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.discount_by_individual_value_quantity ALTER COLUMN id SET DEFAULT nextval('public.discount_by_individual_value_id_seq'::regclass);


--
-- Name: discount_coupon id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.discount_coupon ALTER COLUMN id SET DEFAULT nextval('public.discount_coupon_id_seq'::regclass);


--
-- Name: django_admin_log id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.django_admin_log ALTER COLUMN id SET DEFAULT nextval('public.django_admin_log_id_seq'::regclass);


--
-- Name: django_celery_results_taskresult id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.django_celery_results_taskresult ALTER COLUMN id SET DEFAULT nextval('public.django_celery_results_taskresult_id_seq'::regclass);


--
-- Name: django_content_type id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.django_content_type ALTER COLUMN id SET DEFAULT nextval('public.django_content_type_id_seq'::regclass);


--
-- Name: django_migrations id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.django_migrations ALTER COLUMN id SET DEFAULT nextval('public.django_migrations_id_seq'::regclass);


--
-- Name: draft id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.draft ALTER COLUMN id SET DEFAULT nextval('public.draft_id_seq'::regclass);


--
-- Name: draft_type id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.draft_type ALTER COLUMN id SET DEFAULT nextval('public.draft_type_id_seq'::regclass);


--
-- Name: dynamic_forms id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.dynamic_forms ALTER COLUMN id SET DEFAULT nextval('public.dynamic_forms_id_seq'::regclass);


--
-- Name: extract_file_data id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.extract_file_data ALTER COLUMN id SET DEFAULT nextval('public.extract_file_data_id_seq'::regclass);


--
-- Name: field id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.field ALTER COLUMN id SET DEFAULT nextval('public.field_id_seq'::regclass);


--
-- Name: field_date_format_type id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.field_date_format_type ALTER COLUMN id SET DEFAULT nextval('public.date_format_type_id_seq'::regclass);


--
-- Name: field_number_format_type id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.field_number_format_type ALTER COLUMN id SET DEFAULT nextval('public.field_number_format_type_id_seq'::regclass);


--
-- Name: field_options id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.field_options ALTER COLUMN id SET DEFAULT nextval('public.field_options_id_seq'::regclass);


--
-- Name: field_period_interval_type id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.field_period_interval_type ALTER COLUMN id SET DEFAULT nextval('public.period_interval_type_id_seq'::regclass);


--
-- Name: field_type id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.field_type ALTER COLUMN id SET DEFAULT nextval('public.field_type_id_seq'::regclass);


--
-- Name: form id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.form ALTER COLUMN id SET DEFAULT nextval('public.form_id_seq'::regclass);


--
-- Name: form_accessed_by id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.form_accessed_by ALTER COLUMN id SET DEFAULT nextval('public.form_accessed_by_id_seq'::regclass);


--
-- Name: form_type id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.form_type ALTER COLUMN id SET DEFAULT nextval('public.form_type_id_seq'::regclass);


--
-- Name: form_value id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.form_value ALTER COLUMN id SET DEFAULT nextval('public.client_value_id_seq'::regclass);


--
-- Name: formula_attribute_type id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.formula_attribute_type ALTER COLUMN id SET DEFAULT nextval('public.formula_attribute_type_id_seq'::regclass);


--
-- Name: formula_context_attribute_type id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.formula_context_attribute_type ALTER COLUMN id SET DEFAULT nextval('public.formula_context_attribute_type_id_seq'::regclass);


--
-- Name: formula_context_for_company id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.formula_context_for_company ALTER COLUMN id SET DEFAULT nextval('public.formula_context_for_company_id_seq'::regclass);


--
-- Name: formula_context_type id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.formula_context_type ALTER COLUMN id SET DEFAULT nextval('public.formula_context_type_id_seq'::regclass);


--
-- Name: formula_parameters_type id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.formula_parameters_type ALTER COLUMN id SET DEFAULT nextval('public.formula_parameters_type_id_seq'::regclass);


--
-- Name: formula_variable id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.formula_variable ALTER COLUMN id SET DEFAULT nextval('public.formula_variable_id_seq'::regclass);


--
-- Name: group id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."group" ALTER COLUMN id SET DEFAULT nextval('public.group_id_seq'::regclass);


--
-- Name: individual_charge_value_type id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.individual_charge_value_type ALTER COLUMN id SET DEFAULT nextval('public.individual_charge_value_type_id_seq'::regclass);


--
-- Name: invoice_date_type id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.invoice_date_type ALTER COLUMN id SET DEFAULT nextval('public.invoice_date_type_id_seq'::regclass);


--
-- Name: kanban_card id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.kanban_card ALTER COLUMN id SET DEFAULT nextval('public.kanban_card_id_seq'::regclass);


--
-- Name: kanban_card_field id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.kanban_card_field ALTER COLUMN id SET DEFAULT nextval('public.kanban_card_field_id_seq'::regclass);


--
-- Name: kanban_collapsed_option id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.kanban_collapsed_option ALTER COLUMN id SET DEFAULT nextval('public.kanban_collapsed_option_id_seq'::regclass);


--
-- Name: kanban_default id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.kanban_default ALTER COLUMN id SET DEFAULT nextval('public.kanban_default_id_seq'::regclass);


--
-- Name: kanban_dimension_order id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.kanban_dimension_order ALTER COLUMN id SET DEFAULT nextval('public.kanban_dimension_order_id_seq'::regclass);


--
-- Name: listing_selected_fields id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.listing_selected_fields ALTER COLUMN id SET DEFAULT nextval('public.listing_selected_fields_id_seq'::regclass);


--
-- Name: notification id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.notification ALTER COLUMN id SET DEFAULT nextval('public.notification_id_seq'::regclass);


--
-- Name: notification_configuration id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.notification_configuration ALTER COLUMN id SET DEFAULT nextval('public.notification_configuration_id_seq'::regclass);


--
-- Name: notification_configuration_variable id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.notification_configuration_variable ALTER COLUMN id SET DEFAULT nextval('public.notification_configuration_variable_id_seq'::regclass);


--
-- Name: option_accessed_by id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.option_accessed_by ALTER COLUMN id SET DEFAULT nextval('public.option_accessed_by_id_seq'::regclass);


--
-- Name: partner_default_and_discounts id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.partner_default_and_discounts ALTER COLUMN id SET DEFAULT nextval('public.partner_default_and_discounts_id_seq'::regclass);


--
-- Name: payment_method_type id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.payment_method_type ALTER COLUMN id SET DEFAULT nextval('public.payment_method_type_id_seq'::regclass);


--
-- Name: pdf_generated id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.pdf_generated ALTER COLUMN id SET DEFAULT nextval('public.pdf_generated_id_seq'::regclass);


--
-- Name: pdf_template_allowed_text_block id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.pdf_template_allowed_text_block ALTER COLUMN id SET DEFAULT nextval('public.pdf_template_allowed_text_block_id_seq'::regclass);


--
-- Name: pdf_template_configuration id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.pdf_template_configuration ALTER COLUMN id SET DEFAULT nextval('public.pdf_template_configuration_id_seq'::regclass);


--
-- Name: pdf_template_configuration_variables id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.pdf_template_configuration_variables ALTER COLUMN id SET DEFAULT nextval('public.pdf_template_configuration_variables_id_seq'::regclass);


--
-- Name: pre_notification id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.pre_notification ALTER COLUMN id SET DEFAULT nextval('public.pre_notification_id_seq'::regclass);


--
-- Name: profiles id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.profiles ALTER COLUMN id SET DEFAULT nextval('public.profiles_id_seq'::regclass);


--
-- Name: public_access id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.public_access ALTER COLUMN id SET DEFAULT nextval('public.public_access_id_seq'::regclass);


--
-- Name: public_access_field id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.public_access_field ALTER COLUMN id SET DEFAULT nextval('public.public_field_id_seq'::regclass);


--
-- Name: public_access_form id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.public_access_form ALTER COLUMN id SET DEFAULT nextval('public.public_form_id_seq'::regclass);


--
-- Name: push_notification id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.push_notification ALTER COLUMN id SET DEFAULT nextval('public.push_notification_id_seq'::regclass);


--
-- Name: push_notification_tag_type id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.push_notification_tag_type ALTER COLUMN id SET DEFAULT nextval('public.push_notification_tag_type_id_seq'::regclass);


--
-- Name: raw_data_type id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.raw_data_type ALTER COLUMN id SET DEFAULT nextval('public.raw_data_type_id_seq'::regclass);


--
-- Name: text_alignment_type id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.text_alignment_type ALTER COLUMN id SET DEFAULT nextval('public.text_alignment_type_id_seq'::regclass);


--
-- Name: text_block id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.text_block ALTER COLUMN id SET DEFAULT nextval('public.text_block_id_seq'::regclass);


--
-- Name: text_block_type id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.text_block_type ALTER COLUMN id SET DEFAULT nextval('public.text_block_type_id_seq'::regclass);


--
-- Name: text_block_type_can_contain_type id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.text_block_type_can_contain_type ALTER COLUMN id SET DEFAULT nextval('public.text_block_type_can_contain_type_id_seq'::regclass);


--
-- Name: text_content id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.text_content ALTER COLUMN id SET DEFAULT nextval('public.text_content_id_seq'::regclass);


--
-- Name: text_image_option id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.text_image_option ALTER COLUMN id SET DEFAULT nextval('public.text_image_option_id_seq'::regclass);


--
-- Name: text_list_option id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.text_list_option ALTER COLUMN id SET DEFAULT nextval('public.text_list_option_id_seq'::regclass);


--
-- Name: text_list_type id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.text_list_type ALTER COLUMN id SET DEFAULT nextval('public.text_list_type_id_seq'::regclass);


--
-- Name: text_page id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.text_page ALTER COLUMN id SET DEFAULT nextval('public.text_page_id_seq'::regclass);


--
-- Name: text_table_option id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.text_table_option ALTER COLUMN id SET DEFAULT nextval('public.text_table_option_id_seq'::regclass);


--
-- Name: text_table_option_column_dimension id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.text_table_option_column_dimension ALTER COLUMN id SET DEFAULT nextval('public.text_table_option_column_dimension_id_seq'::regclass);


--
-- Name: text_table_option_row_dimension id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.text_table_option_row_dimension ALTER COLUMN id SET DEFAULT nextval('public.text_table_option_row_dimension_id_seq'::regclass);


--
-- Name: text_text_option id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.text_text_option ALTER COLUMN id SET DEFAULT nextval('public.text_text_option_id_seq'::regclass);


--
-- Name: theme id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.theme ALTER COLUMN id SET DEFAULT nextval('public.theme_id_seq'::regclass);


--
-- Name: theme_dashboard_chart_configuration id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.theme_dashboard_chart_configuration ALTER COLUMN id SET DEFAULT nextval('public.theme_dashboard_chart_configuration_id_seq'::regclass);


--
-- Name: theme_field id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.theme_field ALTER COLUMN id SET DEFAULT nextval('public.theme_field_id_seq'::regclass);


--
-- Name: theme_field_options id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.theme_field_options ALTER COLUMN id SET DEFAULT nextval('public.theme_field_options_id_seq'::regclass);


--
-- Name: theme_form id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.theme_form ALTER COLUMN id SET DEFAULT nextval('public.theme_form_id_seq'::regclass);


--
-- Name: theme_formula_variable id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.theme_formula_variable ALTER COLUMN id SET DEFAULT nextval('public.theme_formula_variable_id_seq'::regclass);


--
-- Name: theme_kanban_card id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.theme_kanban_card ALTER COLUMN id SET DEFAULT nextval('public.theme_kanban_card_id_seq'::regclass);


--
-- Name: theme_kanban_card_field id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.theme_kanban_card_field ALTER COLUMN id SET DEFAULT nextval('public.theme_kanban_card_field_id_seq'::regclass);


--
-- Name: theme_kanban_default id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.theme_kanban_default ALTER COLUMN id SET DEFAULT nextval('public.theme_kanban_default_id_seq'::regclass);


--
-- Name: theme_kanban_dimension_order id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.theme_kanban_dimension_order ALTER COLUMN id SET DEFAULT nextval('public.theme_kanban_dimension_order_id_seq'::regclass);


--
-- Name: theme_notification_configuration id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.theme_notification_configuration ALTER COLUMN id SET DEFAULT nextval('public.theme_notification_configuration_id_seq'::regclass);


--
-- Name: theme_notification_configuration_variable id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.theme_notification_configuration_variable ALTER COLUMN id SET DEFAULT nextval('public.theme_notification_configuration_variable_id_seq'::regclass);


--
-- Name: theme_photos id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.theme_photos ALTER COLUMN id SET DEFAULT nextval('public.theme_photos_id_seq'::regclass);


--
-- Name: theme_type id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.theme_type ALTER COLUMN id SET DEFAULT nextval('public.company_type_id_seq'::regclass);


--
-- Name: user_accessed_by id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.user_accessed_by ALTER COLUMN id SET DEFAULT nextval('public.user_accessed_by_id_seq'::regclass);


--
-- Name: user_notification id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.user_notification ALTER COLUMN id SET DEFAULT nextval('public.read_notification_id_seq'::regclass);


--
-- Name: users id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.users ALTER COLUMN id SET DEFAULT nextval('public.users_id_seq'::regclass);


--
-- Name: users_groups id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.users_groups ALTER COLUMN id SET DEFAULT nextval('public.users_groups_id_seq'::regclass);


--
-- Name: users_user_permissions id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.users_user_permissions ALTER COLUMN id SET DEFAULT nextval('public.users_user_permissions_id_seq'::regclass);


--
-- Data for Name: address_helper; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.address_helper (id, country_code, country_name, state, state_code, city, "order") FROM stdin;
78	BR	Brasil	Amazonas	AM	Anori	78
133	BR	Brasil	Amazonas	AM	Tonantins	133
209	BR	Brasil	Pará	PA	Itaituba	209
220	BR	Brasil	Pará	PA	Marituba	220
245	BR	Brasil	Pará	PA	Placas	245
278	BR	Brasil	Pará	PA	São Sebastião da Boa Vista	278
424	BR	Brasil	Tocantins	TO	Sampaio	424
910	BR	Brasil	Ceará	CE	Assaré	910
1585	BR	Brasil	Pernambuco	PE	Passira	1585
1586	BR	Brasil	Pernambuco	PE	Paudalho	1586
1593	BR	Brasil	Pernambuco	PE	Pombos	1593
1594	BR	Brasil	Pernambuco	PE	Primavera	1594
1595	BR	Brasil	Pernambuco	PE	Quipapá	1595
1596	BR	Brasil	Pernambuco	PE	Quixaba	1596
1597	BR	Brasil	Pernambuco	PE	Recife	1597
1598	BR	Brasil	Pernambuco	PE	Riacho Das Almas	1598
1690	BR	Brasil	Alagoas	AL	Jaramataia	1690
1691	BR	Brasil	Alagoas	AL	Jequiá da Praia	1691
1692	BR	Brasil	Alagoas	AL	Joaquim Gomes	1692
1710	BR	Brasil	Alagoas	AL	Novo Lino	1710
1720	BR	Brasil	Alagoas	AL	Paripueira	1720
1729	BR	Brasil	Alagoas	AL	Porto Calvo	1729
1730	BR	Brasil	Alagoas	AL	Porto de Pedras	1730
1731	BR	Brasil	Alagoas	AL	Porto Real do Colégio	1731
1732	BR	Brasil	Alagoas	AL	Quebrangulo	1732
1733	BR	Brasil	Alagoas	AL	Rio Largo	1733
1734	BR	Brasil	Alagoas	AL	Roteiro	1734
1735	BR	Brasil	Alagoas	AL	Santa Luzia do Norte	1735
1736	BR	Brasil	Alagoas	AL	Santana do Ipanema	1736
1737	BR	Brasil	Alagoas	AL	Santana do Mundaú	1737
1738	BR	Brasil	Alagoas	AL	São Brás	1738
1739	BR	Brasil	Alagoas	AL	São José da Laje	1739
1740	BR	Brasil	Alagoas	AL	São José da Tapera	1740
1741	BR	Brasil	Alagoas	AL	São Luís do Quitunde	1741
1742	BR	Brasil	Alagoas	AL	São Miguel Dos Campos	1742
1743	BR	Brasil	Alagoas	AL	São Miguel Dos Milagres	1743
1744	BR	Brasil	Alagoas	AL	São Sebastião	1744
1745	BR	Brasil	Alagoas	AL	Satuba	1745
1746	BR	Brasil	Alagoas	AL	Senador Rui Palmeira	1746
1747	BR	Brasil	Alagoas	AL	Tanque D´arca	1747
1748	BR	Brasil	Alagoas	AL	Taquarana	1748
1749	BR	Brasil	Alagoas	AL	Teotônio Vilela	1749
1750	BR	Brasil	Alagoas	AL	Traipu	1750
1751	BR	Brasil	Alagoas	AL	União Dos Palmares	1751
1752	BR	Brasil	Alagoas	AL	Viçosa	1752
1753	BR	Brasil	Sergipe	SE	Amparo de São Francisco	1753
1754	BR	Brasil	Sergipe	SE	Aquidabã	1754
4942	BR	Brasil	Rio Grande do Sul	RS	Quaraí	4942
5023	BR	Brasil	Rio Grande do Sul	RS	São Vendelino	5023
5024	BR	Brasil	Rio Grande do Sul	RS	São Vicente do Sul	5024
143	BR	Brasil	Roraima	RR	Caroebe	143
181	BR	Brasil	Pará	PA	Cachoeira do Piriá	181
308	BR	Brasil	Amapá	AP	Pracuúba	308
345	BR	Brasil	Tocantins	TO	Caseara	345
569	BR	Brasil	Maranhão	MA	Miranda do Norte	569
570	BR	Brasil	Maranhão	MA	Mirinzal	570
571	BR	Brasil	Maranhão	MA	Monção	571
572	BR	Brasil	Maranhão	MA	Montes Altos	572
573	BR	Brasil	Maranhão	MA	Morros	573
574	BR	Brasil	Maranhão	MA	Nina Rodrigues	574
575	BR	Brasil	Maranhão	MA	Nova Colinas	575
576	BR	Brasil	Maranhão	MA	Nova Iorque	576
577	BR	Brasil	Maranhão	MA	Nova Olinda do Maranhão	577
578	BR	Brasil	Maranhão	MA	Olho D´água Das Cunhãs	578
579	BR	Brasil	Maranhão	MA	Olinda Nova do Maranhão	579
580	BR	Brasil	Maranhão	MA	Paço do Lumiar	580
581	BR	Brasil	Maranhão	MA	Palmeirândia	581
583	BR	Brasil	Maranhão	MA	Parnarama	583
584	BR	Brasil	Maranhão	MA	Passagem Franca	584
585	BR	Brasil	Maranhão	MA	Pastos Bons	585
586	BR	Brasil	Maranhão	MA	Paulino Neves	586
587	BR	Brasil	Maranhão	MA	Paulo Ramos	587
588	BR	Brasil	Maranhão	MA	Pedreiras	588
589	BR	Brasil	Maranhão	MA	Pedro do Rosário	589
590	BR	Brasil	Maranhão	MA	Penalva	590
591	BR	Brasil	Maranhão	MA	Peri Mirim	591
592	BR	Brasil	Maranhão	MA	Peritoró	592
593	BR	Brasil	Maranhão	MA	Pindaré-mirim	593
594	BR	Brasil	Maranhão	MA	Pinheiro	594
595	BR	Brasil	Maranhão	MA	Pio Xii	595
596	BR	Brasil	Maranhão	MA	Pirapemas	596
597	BR	Brasil	Maranhão	MA	Poção de Pedras	597
598	BR	Brasil	Maranhão	MA	Porto Franco	598
599	BR	Brasil	Maranhão	MA	Porto Rico do Maranhão	599
600	BR	Brasil	Maranhão	MA	Presidente Dutra	600
601	BR	Brasil	Maranhão	MA	Presidente Juscelino	601
602	BR	Brasil	Maranhão	MA	Presidente Médici	602
603	BR	Brasil	Maranhão	MA	Presidente Sarney	603
605	BR	Brasil	Maranhão	MA	Primeira Cruz	605
606	BR	Brasil	Maranhão	MA	Raposa	606
607	BR	Brasil	Maranhão	MA	Riachão	607
3471	BR	Brasil	São Paulo	SP	Guaraci	3471
4988	BR	Brasil	Rio Grande do Sul	RS	São Borja	4988
5018	BR	Brasil	Rio Grande do Sul	RS	São Sebastião do Caí	5018
5021	BR	Brasil	Rio Grande do Sul	RS	São Valentim do Sul	5021
5022	BR	Brasil	Rio Grande do Sul	RS	São Valério do Sul	5022
182	BR	Brasil	Pará	PA	Cachoeira do Arari	182
309	BR	Brasil	Amapá	AP	Santana	309
894	BR	Brasil	Ceará	CE	Acaraú	894
1140	BR	Brasil	Rio Grande do Norte	RN	João Dias	1140
1771	BR	Brasil	Sergipe	SE	Estância	1771
4051	BR	Brasil	Paraná	PR	Ibaiti	4051
4365	BR	Brasil	Santa Catarina	SC	Campo Alegre	4365
4888	BR	Brasil	Rio Grande do Sul	RS	Nova Prata	4888
4893	BR	Brasil	Rio Grande do Sul	RS	Novo Hamburgo	4893
4894	BR	Brasil	Rio Grande do Sul	RS	Novo Machado	4894
4897	BR	Brasil	Rio Grande do Sul	RS	Novo Barreiro	4897
4898	BR	Brasil	Rio Grande do Sul	RS	Osório	4898
4936	BR	Brasil	Rio Grande do Sul	RS	Porto Xavier	4936
4943	BR	Brasil	Rio Grande do Sul	RS	Quatro Irmãos	4943
4944	BR	Brasil	Rio Grande do Sul	RS	Quevedos	4944
4945	BR	Brasil	Rio Grande do Sul	RS	Quinze de Novembro	4945
4946	BR	Brasil	Rio Grande do Sul	RS	Redentora	4946
4947	BR	Brasil	Rio Grande do Sul	RS	Relvado	4947
4948	BR	Brasil	Rio Grande do Sul	RS	Restinga Seca	4948
4950	BR	Brasil	Rio Grande do Sul	RS	Rio Grande	4950
4952	BR	Brasil	Rio Grande do Sul	RS	Riozinho	4952
4953	BR	Brasil	Rio Grande do Sul	RS	Roca Sales	4953
4954	BR	Brasil	Rio Grande do Sul	RS	Rodeio Bonito	4954
4956	BR	Brasil	Rio Grande do Sul	RS	Rolante	4956
4957	BR	Brasil	Rio Grande do Sul	RS	Ronda Alta	4957
4958	BR	Brasil	Rio Grande do Sul	RS	Rondinha	4958
4959	BR	Brasil	Rio Grande do Sul	RS	Roque Gonzales	4959
4960	BR	Brasil	Rio Grande do Sul	RS	Rosário do Sul	4960
4961	BR	Brasil	Rio Grande do Sul	RS	Sagrada Família	4961
4962	BR	Brasil	Rio Grande do Sul	RS	Saldanha Marinho	4962
4963	BR	Brasil	Rio Grande do Sul	RS	Salto do Jacuí	4963
4964	BR	Brasil	Rio Grande do Sul	RS	Salvador Das Missões	4964
4965	BR	Brasil	Rio Grande do Sul	RS	Salvador do Sul	4965
4967	BR	Brasil	Rio Grande do Sul	RS	Santa Bárbara do Sul	4967
4968	BR	Brasil	Rio Grande do Sul	RS	Santa Cecília do Sul	4968
4969	BR	Brasil	Rio Grande do Sul	RS	Santa Clara do Sul	4969
4978	BR	Brasil	Rio Grande do Sul	RS	Santa Vitória do Palmar	4978
4980	BR	Brasil	Rio Grande do Sul	RS	Santo Ângelo	4980
4981	BR	Brasil	Rio Grande do Sul	RS	Santo Antônio do Palma	4981
4982	BR	Brasil	Rio Grande do Sul	RS	Santo Antônio da Patrulha	4982
4984	BR	Brasil	Rio Grande do Sul	RS	Santo Antônio do Planalto	4984
4986	BR	Brasil	Rio Grande do Sul	RS	Santo Cristo	4986
4987	BR	Brasil	Rio Grande do Sul	RS	Santo Expedito do Sul	4987
5028	BR	Brasil	Rio Grande do Sul	RS	Seberi	5028
35	BR	Brasil	Rondônia	RO	Cujubim	35
106	BR	Brasil	Amazonas	AM	Japurá	106
221	BR	Brasil	Pará	PA	Medicilândia	221
222	BR	Brasil	Pará	PA	Melgaço	222
262	BR	Brasil	Pará	PA	Santa Maria Das Barreiras	262
328	BR	Brasil	Tocantins	TO	Augustinópolis	328
333	BR	Brasil	Tocantins	TO	Barra do Ouro	333
379	BR	Brasil	Tocantins	TO	Lajeado	379
404	BR	Brasil	Tocantins	TO	Pau D´arco	404
412	BR	Brasil	Tocantins	TO	Ponte Alta do Bom Jesus	412
4696	BR	Brasil	Rio Grande do Sul	RS	Caraá	4696
4697	BR	Brasil	Rio Grande do Sul	RS	Carlos Barbosa	4697
4698	BR	Brasil	Rio Grande do Sul	RS	Carlos Gomes	4698
4739	BR	Brasil	Rio Grande do Sul	RS	Dois Irmãos Das Missões	4739
4740	BR	Brasil	Rio Grande do Sul	RS	Dois Lajeados	4740
4741	BR	Brasil	Rio Grande do Sul	RS	Dom Feliciano	4741
4763	BR	Brasil	Rio Grande do Sul	RS	Estância Velha	4763
4764	BR	Brasil	Rio Grande do Sul	RS	Esteio	4764
4847	BR	Brasil	Rio Grande do Sul	RS	Manoel Viana	4847
4848	BR	Brasil	Rio Grande do Sul	RS	Maquiné	4848
4849	BR	Brasil	Rio Grande do Sul	RS	Maratá	4849
4850	BR	Brasil	Rio Grande do Sul	RS	Marau	4850
4851	BR	Brasil	Rio Grande do Sul	RS	Marcelino Ramos	4851
4852	BR	Brasil	Rio Grande do Sul	RS	Mariana Pimentel	4852
4853	BR	Brasil	Rio Grande do Sul	RS	Mariano Moro	4853
4854	BR	Brasil	Rio Grande do Sul	RS	Marques de Souza	4854
4856	BR	Brasil	Rio Grande do Sul	RS	Mato Castelhano	4856
4857	BR	Brasil	Rio Grande do Sul	RS	Mato Leitão	4857
4858	BR	Brasil	Rio Grande do Sul	RS	Mato Queimado	4858
4859	BR	Brasil	Rio Grande do Sul	RS	Maximiliano de Almeida	4859
4860	BR	Brasil	Rio Grande do Sul	RS	Minas do Leão	4860
4883	BR	Brasil	Rio Grande do Sul	RS	Nova Esperança do Sul	4883
4884	BR	Brasil	Rio Grande do Sul	RS	Nova Hartz	4884
4885	BR	Brasil	Rio Grande do Sul	RS	Nova Pádua	4885
4886	BR	Brasil	Rio Grande do Sul	RS	Nova Palma	4886
4906	BR	Brasil	Rio Grande do Sul	RS	Paraíso do Sul	4906
4925	BR	Brasil	Rio Grande do Sul	RS	Pirapó	4925
4926	BR	Brasil	Rio Grande do Sul	RS	Piratini	4926
4927	BR	Brasil	Rio Grande do Sul	RS	Planalto	4927
4928	BR	Brasil	Rio Grande do Sul	RS	Poço Das Antas	4928
4929	BR	Brasil	Rio Grande do Sul	RS	Pontão	4929
4930	BR	Brasil	Rio Grande do Sul	RS	Ponte Preta	4930
4931	BR	Brasil	Rio Grande do Sul	RS	Portão	4931
4932	BR	Brasil	Rio Grande do Sul	RS	Porto Alegre	4932
4933	BR	Brasil	Rio Grande do Sul	RS	Porto Lucena	4933
189	BR	Brasil	Pará	PA	Colares	189
226	BR	Brasil	Pará	PA	Monte Alegre	226
257	BR	Brasil	Pará	PA	Salvaterra	257
272	BR	Brasil	Pará	PA	São Francisco do Pará	272
311	BR	Brasil	Amapá	AP	Vitória do Jari	311
347	BR	Brasil	Tocantins	TO	Chapada de Areia	347
394	BR	Brasil	Tocantins	TO	Nova Olinda	394
608	BR	Brasil	Maranhão	MA	Ribamar Fiquene	608
847	BR	Brasil	Piauí	PI	Santa Rosa do Piauí	847
1772	BR	Brasil	Sergipe	SE	Feira Nova	1772
3472	BR	Brasil	São Paulo	SP	Guarani D´oeste	3472
4458	BR	Brasil	Santa Catarina	SC	Leoberto Leal	4458
4637	BR	Brasil	Rio Grande do Sul	RS	Balneário Pinhal	4637
4638	BR	Brasil	Rio Grande do Sul	RS	Barão	4638
4639	BR	Brasil	Rio Grande do Sul	RS	Barão de Cotegipe	4639
4640	BR	Brasil	Rio Grande do Sul	RS	Barão do Triunfo	4640
4641	BR	Brasil	Rio Grande do Sul	RS	Barracão	4641
4642	BR	Brasil	Rio Grande do Sul	RS	Barra do Guarita	4642
4643	BR	Brasil	Rio Grande do Sul	RS	Barra do Quaraí	4643
4644	BR	Brasil	Rio Grande do Sul	RS	Barra do Ribeiro	4644
4645	BR	Brasil	Rio Grande do Sul	RS	Barra do Rio Azul	4645
4646	BR	Brasil	Rio Grande do Sul	RS	Barra Funda	4646
4647	BR	Brasil	Rio Grande do Sul	RS	Barros Cassal	4647
4648	BR	Brasil	Rio Grande do Sul	RS	Benjamin Constant do Sul	4648
4649	BR	Brasil	Rio Grande do Sul	RS	Bento Gonçalves	4649
4650	BR	Brasil	Rio Grande do Sul	RS	Boa Vista Das Missões	4650
4651	BR	Brasil	Rio Grande do Sul	RS	Boa Vista do Buricá	4651
4655	BR	Brasil	Rio Grande do Sul	RS	Bom Jesus	4655
4675	BR	Brasil	Rio Grande do Sul	RS	Campestre da Serra	4675
4676	BR	Brasil	Rio Grande do Sul	RS	Campina Das Missões	4676
4677	BR	Brasil	Rio Grande do Sul	RS	Campinas do Sul	4677
4678	BR	Brasil	Rio Grande do Sul	RS	Campo Bom	4678
4679	BR	Brasil	Rio Grande do Sul	RS	Campo Novo	4679
4686	BR	Brasil	Rio Grande do Sul	RS	Canoas	4686
4687	BR	Brasil	Rio Grande do Sul	RS	Canudos do Vale	4687
4688	BR	Brasil	Rio Grande do Sul	RS	Capão Bonito do Sul	4688
4689	BR	Brasil	Rio Grande do Sul	RS	Capão da Canoa	4689
4690	BR	Brasil	Rio Grande do Sul	RS	Capão do Cipó	4690
4691	BR	Brasil	Rio Grande do Sul	RS	Capão do Leão	4691
4692	BR	Brasil	Rio Grande do Sul	RS	Capivari do Sul	4692
4693	BR	Brasil	Rio Grande do Sul	RS	Capela de Santana	4693
4694	BR	Brasil	Rio Grande do Sul	RS	Capitão	4694
5041	BR	Brasil	Rio Grande do Sul	RS	Sinimbu	5041
5043	BR	Brasil	Rio Grande do Sul	RS	Soledade	5043
77	BR	Brasil	Amazonas	AM	Anamã	77
4459	BR	Brasil	Santa Catarina	SC	Lindóia do Sul	4459
4460	BR	Brasil	Santa Catarina	SC	Lontras	4460
4461	BR	Brasil	Santa Catarina	SC	Luiz Alves	4461
4549	BR	Brasil	Santa Catarina	SC	São Bento do Sul	4549
4551	BR	Brasil	Santa Catarina	SC	São Carlos	4551
4552	BR	Brasil	Santa Catarina	SC	São Cristovão do Sul	4552
4553	BR	Brasil	Santa Catarina	SC	São Domingos	4553
4554	BR	Brasil	Santa Catarina	SC	São Francisco do Sul	4554
4555	BR	Brasil	Santa Catarina	SC	São João do Oeste	4555
4558	BR	Brasil	Santa Catarina	SC	São João do Sul	4558
4559	BR	Brasil	Santa Catarina	SC	São Joaquim	4559
4560	BR	Brasil	Santa Catarina	SC	São José	4560
4561	BR	Brasil	Santa Catarina	SC	São José do Cedro	4561
4562	BR	Brasil	Santa Catarina	SC	São José do Cerrito	4562
4563	BR	Brasil	Santa Catarina	SC	São Lourenço do Oeste	4563
4564	BR	Brasil	Santa Catarina	SC	São Ludgero	4564
4565	BR	Brasil	Santa Catarina	SC	São Martinho	4565
4699	BR	Brasil	Rio Grande do Sul	RS	Casca	4699
4720	BR	Brasil	Rio Grande do Sul	RS	Constantina	4720
4721	BR	Brasil	Rio Grande do Sul	RS	Coqueiro Baixo	4721
4722	BR	Brasil	Rio Grande do Sul	RS	Coqueiros do Sul	4722
4723	BR	Brasil	Rio Grande do Sul	RS	Coronel Barros	4723
4724	BR	Brasil	Rio Grande do Sul	RS	Coronel Bicaco	4724
4725	BR	Brasil	Rio Grande do Sul	RS	Coronel Pilar	4725
4726	BR	Brasil	Rio Grande do Sul	RS	Cotiporã	4726
4727	BR	Brasil	Rio Grande do Sul	RS	Coxilha	4727
4728	BR	Brasil	Rio Grande do Sul	RS	Crissiumal	4728
4732	BR	Brasil	Rio Grande do Sul	RS	Cruzaltense	4732
4735	BR	Brasil	Rio Grande do Sul	RS	Derrubadas	4735
4736	BR	Brasil	Rio Grande do Sul	RS	Dezesseis de Novembro	4736
4737	BR	Brasil	Rio Grande do Sul	RS	Dilermando de Aguiar	4737
4738	BR	Brasil	Rio Grande do Sul	RS	Dois Irmãos	4738
5007	BR	Brasil	Rio Grande do Sul	RS	São Luiz Gonzaga	5007
5008	BR	Brasil	Rio Grande do Sul	RS	São Marcos	5008
5009	BR	Brasil	Rio Grande do Sul	RS	São Martinho	5009
5010	BR	Brasil	Rio Grande do Sul	RS	São Martinho da Serra	5010
5044	BR	Brasil	Rio Grande do Sul	RS	Tabaí	5044
5046	BR	Brasil	Rio Grande do Sul	RS	Tapera	5046
5048	BR	Brasil	Rio Grande do Sul	RS	Taquara	5048
5052	BR	Brasil	Rio Grande do Sul	RS	Tenente Portela	5052
5053	BR	Brasil	Rio Grande do Sul	RS	Terra de Areia	5053
5055	BR	Brasil	Rio Grande do Sul	RS	Tio Hugo	5055
5063	BR	Brasil	Rio Grande do Sul	RS	Três Coroas	5063
114	BR	Brasil	Amazonas	AM	Maraã	114
144	BR	Brasil	Roraima	RR	Iracema	144
216	BR	Brasil	Pará	PA	Magalhães Barata	216
230	BR	Brasil	Pará	PA	Nova Timboteua	230
282	BR	Brasil	Pará	PA	Tailândia	282
355	BR	Brasil	Tocantins	TO	Darcinópolis	355
364	BR	Brasil	Tocantins	TO	Formoso do Araguaia	364
610	BR	Brasil	Maranhão	MA	Sambaíba	610
869	BR	Brasil	Piauí	PI	São Miguel da Baixa Grande	869
1773	BR	Brasil	Sergipe	SE	Frei Paulo	1773
2350	BR	Brasil	Minas Gerais	MG	Cachoeira de Minas	2350
2353	BR	Brasil	Minas Gerais	MG	Caeté	2353
4366	BR	Brasil	Santa Catarina	SC	Campo Belo do Sul	4366
4368	BR	Brasil	Santa Catarina	SC	Campos Novos	4368
4375	BR	Brasil	Santa Catarina	SC	Celso Ramos	4375
4382	BR	Brasil	Santa Catarina	SC	Coronel Freitas	4382
4385	BR	Brasil	Santa Catarina	SC	Correia Pinto	4385
4386	BR	Brasil	Santa Catarina	SC	Criciúma	4386
4387	BR	Brasil	Santa Catarina	SC	Cunha Porã	4387
4388	BR	Brasil	Santa Catarina	SC	Cunhataí	4388
4389	BR	Brasil	Santa Catarina	SC	Curitibanos	4389
4390	BR	Brasil	Santa Catarina	SC	Descanso	4390
4436	BR	Brasil	Santa Catarina	SC	Itaiópolis	4436
4437	BR	Brasil	Santa Catarina	SC	Itajaí	4437
4438	BR	Brasil	Santa Catarina	SC	Itapema	4438
4439	BR	Brasil	Santa Catarina	SC	Itapiranga	4439
4566	BR	Brasil	Santa Catarina	SC	São Miguel da Boa Vista	4566
4567	BR	Brasil	Santa Catarina	SC	São Miguel do Oeste	4567
4568	BR	Brasil	Santa Catarina	SC	São Pedro de Alcântara	4568
4569	BR	Brasil	Santa Catarina	SC	Saudades	4569
4570	BR	Brasil	Santa Catarina	SC	Schroeder	4570
4572	BR	Brasil	Santa Catarina	SC	Serra Alta	4572
4573	BR	Brasil	Santa Catarina	SC	Siderópolis	4573
4574	BR	Brasil	Santa Catarina	SC	Sombrio	4574
4627	BR	Brasil	Rio Grande do Sul	RS	Arroio do Meio	4627
4628	BR	Brasil	Rio Grande do Sul	RS	Arroio do Sal	4628
4629	BR	Brasil	Rio Grande do Sul	RS	Arroio do Padre	4629
4630	BR	Brasil	Rio Grande do Sul	RS	Arroio Dos Ratos	4630
4631	BR	Brasil	Rio Grande do Sul	RS	Arroio do Tigre	4631
4632	BR	Brasil	Rio Grande do Sul	RS	Arroio Grande	4632
4633	BR	Brasil	Rio Grande do Sul	RS	Arvorezinha	4633
4634	BR	Brasil	Rio Grande do Sul	RS	Augusto Pestana	4634
4635	BR	Brasil	Rio Grande do Sul	RS	Áurea	4635
4951	BR	Brasil	Rio Grande do Sul	RS	Rio Pardo	4951
290	BR	Brasil	Pará	PA	Ulianópolis	290
356	BR	Brasil	Tocantins	TO	Dianópolis	356
1328	BR	Brasil	Paraíba	PB	Gurjão	1328
1774	BR	Brasil	Sergipe	SE	Gararu	1774
3473	BR	Brasil	São Paulo	SP	Guarantã	3473
3474	BR	Brasil	São Paulo	SP	Guararapes	3474
4134	BR	Brasil	Paraná	PR	Miraselva	4134
4575	BR	Brasil	Santa Catarina	SC	Sul Brasil	4575
4576	BR	Brasil	Santa Catarina	SC	Taió	4576
4577	BR	Brasil	Santa Catarina	SC	Tangará	4577
4578	BR	Brasil	Santa Catarina	SC	Tigrinhos	4578
4579	BR	Brasil	Santa Catarina	SC	Tijucas	4579
4580	BR	Brasil	Santa Catarina	SC	Timbé do Sul	4580
4581	BR	Brasil	Santa Catarina	SC	Timbó	4581
4582	BR	Brasil	Santa Catarina	SC	Timbó Grande	4582
4584	BR	Brasil	Santa Catarina	SC	Treviso	4584
4585	BR	Brasil	Santa Catarina	SC	Treze de Maio	4585
4586	BR	Brasil	Santa Catarina	SC	Treze Tílias	4586
4587	BR	Brasil	Santa Catarina	SC	Trombudo Central	4587
4589	BR	Brasil	Santa Catarina	SC	Tunápolis	4589
4590	BR	Brasil	Santa Catarina	SC	Turvo	4590
4594	BR	Brasil	Santa Catarina	SC	Urussanga	4594
4595	BR	Brasil	Santa Catarina	SC	Vargeão	4595
4597	BR	Brasil	Santa Catarina	SC	Vargem Bonita	4597
4598	BR	Brasil	Santa Catarina	SC	Vidal Ramos	4598
4600	BR	Brasil	Santa Catarina	SC	Vitor Meireles	4600
4602	BR	Brasil	Santa Catarina	SC	Xanxerê	4602
4603	BR	Brasil	Santa Catarina	SC	Xavantina	4603
4606	BR	Brasil	Santa Catarina	SC	Balneário Rincão	4606
4607	BR	Brasil	Rio Grande do Sul	RS	Aceguá	4607
4608	BR	Brasil	Rio Grande do Sul	RS	Água Santa	4608
4609	BR	Brasil	Rio Grande do Sul	RS	Agudo	4609
4610	BR	Brasil	Rio Grande do Sul	RS	Ajuricaba	4610
4611	BR	Brasil	Rio Grande do Sul	RS	Alecrim	4611
4612	BR	Brasil	Rio Grande do Sul	RS	Alegrete	4612
4623	BR	Brasil	Rio Grande do Sul	RS	Antônio Prado	4623
4625	BR	Brasil	Rio Grande do Sul	RS	Araricá	4625
5004	BR	Brasil	Rio Grande do Sul	RS	São José Dos Ausentes	5004
5006	BR	Brasil	Rio Grande do Sul	RS	São Lourenço do Sul	5006
5011	BR	Brasil	Rio Grande do Sul	RS	São Miguel Das Missões	5011
5013	BR	Brasil	Rio Grande do Sul	RS	São Paulo Das Missões	5013
5015	BR	Brasil	Rio Grande do Sul	RS	São Pedro Das Missões	5015
5016	BR	Brasil	Rio Grande do Sul	RS	São Pedro do Butiá	5016
5017	BR	Brasil	Rio Grande do Sul	RS	São Pedro do Sul	5017
5020	BR	Brasil	Rio Grande do Sul	RS	São Valentim	5020
183	BR	Brasil	Pará	PA	Cametá	183
206	BR	Brasil	Pará	PA	Inhangapi	206
223	BR	Brasil	Pará	PA	Mocajuba	223
258	BR	Brasil	Pará	PA	Santa Bárbara do Pará	258
334	BR	Brasil	Tocantins	TO	Barrolândia	334
337	BR	Brasil	Tocantins	TO	Brasilândia do Tocantins	337
1785	BR	Brasil	Sergipe	SE	Lagarto	1785
1786	BR	Brasil	Sergipe	SE	Laranjeiras	1786
2354	BR	Brasil	Minas Gerais	MG	Caiana	2354
3712	BR	Brasil	São Paulo	SP	Poá	3712
3883	BR	Brasil	São Paulo	SP	Tuiuti	3883
4136	BR	Brasil	Paraná	PR	Moreira Sales	4136
4138	BR	Brasil	Paraná	PR	Munhoz de Melo	4138
4139	BR	Brasil	Paraná	PR	Nossa Senhora Das Graças	4139
4178	BR	Brasil	Paraná	PR	Pinhalão	4178
4179	BR	Brasil	Paraná	PR	Pinhal de São Bento	4179
4183	BR	Brasil	Paraná	PR	Pitanga	4183
4211	BR	Brasil	Paraná	PR	Rebouças	4211
4212	BR	Brasil	Paraná	PR	Renascença	4212
4214	BR	Brasil	Paraná	PR	Reserva do Iguaçu	4214
4215	BR	Brasil	Paraná	PR	Ribeirão Claro	4215
4216	BR	Brasil	Paraná	PR	Ribeirão do Pinhal	4216
4217	BR	Brasil	Paraná	PR	Rio Azul	4217
4218	BR	Brasil	Paraná	PR	Rio Bom	4218
4219	BR	Brasil	Paraná	PR	Rio Bonito do Iguaçu	4219
4220	BR	Brasil	Paraná	PR	Rio Branco do Ivaí	4220
4241	BR	Brasil	Paraná	PR	Santa Mariana	4241
4255	BR	Brasil	Paraná	PR	São João do Ivaí	4255
4256	BR	Brasil	Paraná	PR	São João do Triunfo	4256
4257	BR	Brasil	Paraná	PR	São Jorge D´oeste	4257
4258	BR	Brasil	Paraná	PR	São Jorge do Ivaí	4258
4259	BR	Brasil	Paraná	PR	São Jorge do Patrocínio	4259
4260	BR	Brasil	Paraná	PR	São José da Boa Vista	4260
4261	BR	Brasil	Paraná	PR	São José Das Palmeiras	4261
4262	BR	Brasil	Paraná	PR	São José Dos Pinhais	4262
4263	BR	Brasil	Paraná	PR	São Manoel do Paraná	4263
4264	BR	Brasil	Paraná	PR	São Mateus do Sul	4264
4265	BR	Brasil	Paraná	PR	São Miguel do Iguaçu	4265
4266	BR	Brasil	Paraná	PR	São Pedro do Iguaçu	4266
4267	BR	Brasil	Paraná	PR	São Pedro do Ivaí	4267
4268	BR	Brasil	Paraná	PR	São Pedro do Paraná	4268
4269	BR	Brasil	Paraná	PR	São Sebastião da Amoreira	4269
4315	BR	Brasil	Santa Catarina	SC	Agronômica	4315
120	BR	Brasil	Amazonas	AM	Parintins	120
121	BR	Brasil	Amazonas	AM	Pauini	121
291	BR	Brasil	Pará	PA	Uruará	291
341	BR	Brasil	Tocantins	TO	Campos Lindos	341
376	BR	Brasil	Tocantins	TO	Juarina	376
1787	BR	Brasil	Sergipe	SE	Macambira	1787
1788	BR	Brasil	Sergipe	SE	Malhada Dos Bois	1788
1789	BR	Brasil	Sergipe	SE	Malhador	1789
1790	BR	Brasil	Sergipe	SE	Maruim	1790
1791	BR	Brasil	Sergipe	SE	Moita Bonita	1791
1792	BR	Brasil	Sergipe	SE	Monte Alegre de Sergipe	1792
1793	BR	Brasil	Sergipe	SE	Muribeca	1793
1794	BR	Brasil	Sergipe	SE	Neópolis	1794
1795	BR	Brasil	Sergipe	SE	Nossa Senhora Aparecida	1795
1796	BR	Brasil	Sergipe	SE	Nossa Senhora da Glória	1796
1797	BR	Brasil	Sergipe	SE	Nossa Senhora Das Dores	1797
1798	BR	Brasil	Sergipe	SE	Nossa Senhora de Lourdes	1798
3475	BR	Brasil	São Paulo	SP	Guararema	3475
4361	BR	Brasil	Santa Catarina	SC	Caibi	4361
4391	BR	Brasil	Santa Catarina	SC	Dionísio Cerqueira	4391
4392	BR	Brasil	Santa Catarina	SC	Dona Emma	4392
4393	BR	Brasil	Santa Catarina	SC	Doutor Pedrinho	4393
4412	BR	Brasil	Santa Catarina	SC	Guaraciaba	4412
4418	BR	Brasil	Santa Catarina	SC	Ibicaré	4418
4419	BR	Brasil	Santa Catarina	SC	Ibirama	4419
4420	BR	Brasil	Santa Catarina	SC	Içara	4420
4421	BR	Brasil	Santa Catarina	SC	Ilhota	4421
4422	BR	Brasil	Santa Catarina	SC	Imaruí	4422
4423	BR	Brasil	Santa Catarina	SC	Imbituba	4423
4424	BR	Brasil	Santa Catarina	SC	Imbuia	4424
4426	BR	Brasil	Santa Catarina	SC	Iomerê	4426
4427	BR	Brasil	Santa Catarina	SC	Ipira	4427
4428	BR	Brasil	Santa Catarina	SC	Iporã do Oeste	4428
4429	BR	Brasil	Santa Catarina	SC	Ipuaçu	4429
4430	BR	Brasil	Santa Catarina	SC	Ipumirim	4430
4431	BR	Brasil	Santa Catarina	SC	Iraceminha	4431
4432	BR	Brasil	Santa Catarina	SC	Irani	4432
4434	BR	Brasil	Santa Catarina	SC	Irineópolis	4434
4970	BR	Brasil	Rio Grande do Sul	RS	Santa Cruz do Sul	4970
4972	BR	Brasil	Rio Grande do Sul	RS	Santa Maria do Herval	4972
4973	BR	Brasil	Rio Grande do Sul	RS	Santa Margarida do Sul	4973
4974	BR	Brasil	Rio Grande do Sul	RS	Santana da Boa Vista	4974
4975	BR	Brasil	Rio Grande do Sul	RS	Santana do Livramento	4975
5064	BR	Brasil	Rio Grande do Sul	RS	Três de Maio	5064
5065	BR	Brasil	Rio Grande do Sul	RS	Três Forquilhas	5065
79	BR	Brasil	Amazonas	AM	Apuí	79
207	BR	Brasil	Pará	PA	Ipixuna do Pará	207
237	BR	Brasil	Pará	PA	Ourilândia do Norte	237
263	BR	Brasil	Pará	PA	Santa Maria do Pará	263
357	BR	Brasil	Tocantins	TO	Divinópolis do Tocantins	357
870	BR	Brasil	Piauí	PI	São Miguel do Fidalgo	870
1334	BR	Brasil	Paraíba	PB	Itapororoca	1334
3476	BR	Brasil	São Paulo	SP	Guaratinguetá	3476
4326	BR	Brasil	Santa Catarina	SC	Antônio Carlos	4326
4327	BR	Brasil	Santa Catarina	SC	Apiúna	4327
4328	BR	Brasil	Santa Catarina	SC	Arabutã	4328
4329	BR	Brasil	Santa Catarina	SC	Araquari	4329
4330	BR	Brasil	Santa Catarina	SC	Araranguá	4330
4331	BR	Brasil	Santa Catarina	SC	Armazém	4331
4352	BR	Brasil	Santa Catarina	SC	Bom Jesus	4352
4353	BR	Brasil	Santa Catarina	SC	Bom Jesus do Oeste	4353
4354	BR	Brasil	Santa Catarina	SC	Bom Retiro	4354
4355	BR	Brasil	Santa Catarina	SC	Botuverá	4355
4356	BR	Brasil	Santa Catarina	SC	Braço do Norte	4356
4358	BR	Brasil	Santa Catarina	SC	Brunópolis	4358
4509	BR	Brasil	Santa Catarina	SC	Piratuba	4509
4510	BR	Brasil	Santa Catarina	SC	Planalto Alegre	4510
4511	BR	Brasil	Santa Catarina	SC	Pomerode	4511
4512	BR	Brasil	Santa Catarina	SC	Ponte Alta	4512
4513	BR	Brasil	Santa Catarina	SC	Ponte Alta do Norte	4513
4514	BR	Brasil	Santa Catarina	SC	Ponte Serrada	4514
4515	BR	Brasil	Santa Catarina	SC	Porto Belo	4515
4516	BR	Brasil	Santa Catarina	SC	Porto União	4516
4517	BR	Brasil	Santa Catarina	SC	Pouso Redondo	4517
4518	BR	Brasil	Santa Catarina	SC	Praia Grande	4518
4539	BR	Brasil	Santa Catarina	SC	Sangão	4539
4540	BR	Brasil	Santa Catarina	SC	Santa Cecília	4540
4541	BR	Brasil	Santa Catarina	SC	Santa Helena	4541
4542	BR	Brasil	Santa Catarina	SC	Santa Rosa de Lima	4542
4544	BR	Brasil	Santa Catarina	SC	Santa Terezinha	4544
4545	BR	Brasil	Santa Catarina	SC	Santa Terezinha do Progresso	4545
4546	BR	Brasil	Santa Catarina	SC	Santiago do Sul	4546
4547	BR	Brasil	Santa Catarina	SC	Santo Amaro da Imperatriz	4547
4548	BR	Brasil	Santa Catarina	SC	São Bernardino	4548
4934	BR	Brasil	Rio Grande do Sul	RS	Porto Mauá	4934
4935	BR	Brasil	Rio Grande do Sul	RS	Porto Vera Cruz	4935
4938	BR	Brasil	Rio Grande do Sul	RS	Presidente Lucena	4938
4939	BR	Brasil	Rio Grande do Sul	RS	Progresso	4939
4940	BR	Brasil	Rio Grande do Sul	RS	Protásio Alves	4940
4941	BR	Brasil	Rio Grande do Sul	RS	Putinga	4941
208	BR	Brasil	Pará	PA	Irituia	208
283	BR	Brasil	Pará	PA	Terra Alta	283
348	BR	Brasil	Tocantins	TO	Chapada da Natividade	348
1823	BR	Brasil	Sergipe	SE	Siriri	1823
2622	BR	Brasil	Minas Gerais	MG	Itapagipe	2622
3884	BR	Brasil	São Paulo	SP	Tupã	3884
3885	BR	Brasil	São Paulo	SP	Tupi Paulista	3885
3886	BR	Brasil	São Paulo	SP	Turiúba	3886
3887	BR	Brasil	São Paulo	SP	Turmalina	3887
3888	BR	Brasil	São Paulo	SP	Ubarana	3888
3889	BR	Brasil	São Paulo	SP	Ubatuba	3889
3894	BR	Brasil	São Paulo	SP	Uru	3894
3945	BR	Brasil	Paraná	PR	Bela Vista da Caroba	3945
3946	BR	Brasil	Paraná	PR	Bela Vista do Paraíso	3946
4032	BR	Brasil	Paraná	PR	Francisco Alves	4032
4033	BR	Brasil	Paraná	PR	Francisco Beltrão	4033
4034	BR	Brasil	Paraná	PR	Foz do Jordão	4034
4035	BR	Brasil	Paraná	PR	General Carneiro	4035
4036	BR	Brasil	Paraná	PR	Godoy Moreira	4036
4037	BR	Brasil	Paraná	PR	Goioerê	4037
4038	BR	Brasil	Paraná	PR	Goioxim	4038
4039	BR	Brasil	Paraná	PR	Grandes Rios	4039
4040	BR	Brasil	Paraná	PR	Guaíra	4040
4041	BR	Brasil	Paraná	PR	Guairaçá	4041
4042	BR	Brasil	Paraná	PR	Guamiranga	4042
4043	BR	Brasil	Paraná	PR	Guapirama	4043
4044	BR	Brasil	Paraná	PR	Guaporema	4044
4045	BR	Brasil	Paraná	PR	Guaraci	4045
4046	BR	Brasil	Paraná	PR	Guaraniaçu	4046
4047	BR	Brasil	Paraná	PR	Guarapuava	4047
4048	BR	Brasil	Paraná	PR	Guaraqueçaba	4048
4049	BR	Brasil	Paraná	PR	Guaratuba	4049
4050	BR	Brasil	Paraná	PR	Honório Serpa	4050
4052	BR	Brasil	Paraná	PR	Ibema	4052
4053	BR	Brasil	Paraná	PR	Ibiporã	4053
4054	BR	Brasil	Paraná	PR	Icaraíma	4054
4055	BR	Brasil	Paraná	PR	Iguaraçu	4055
4056	BR	Brasil	Paraná	PR	Iguatu	4056
4057	BR	Brasil	Paraná	PR	Imbaú	4057
4060	BR	Brasil	Paraná	PR	Inajá	4060
4061	BR	Brasil	Paraná	PR	Indianópolis	4061
4062	BR	Brasil	Paraná	PR	Ipiranga	4062
4063	BR	Brasil	Paraná	PR	Iporã	4063
4064	BR	Brasil	Paraná	PR	Iracema do Oeste	4064
4065	BR	Brasil	Paraná	PR	Irati	4065
4066	BR	Brasil	Paraná	PR	Iretama	4066
4067	BR	Brasil	Paraná	PR	Itaguajé	4067
4068	BR	Brasil	Paraná	PR	Itaipulândia	4068
4069	BR	Brasil	Paraná	PR	Itambaracá	4069
156	BR	Brasil	Pará	PA	Água Azul do Norte	156
169	BR	Brasil	Pará	PA	Barcarena	169
190	BR	Brasil	Pará	PA	Conceição do Araguaia	190
284	BR	Brasil	Pará	PA	Terra Santa	284
342	BR	Brasil	Tocantins	TO	Cariri do Tocantins	342
365	BR	Brasil	Tocantins	TO	Fortaleza do Tabocão	365
1335	BR	Brasil	Paraíba	PB	Itatuba	1335
1336	BR	Brasil	Paraíba	PB	Jacaraú	1336
2357	BR	Brasil	Minas Gerais	MG	Camacho	2357
3367	BR	Brasil	São Paulo	SP	Cafelândia	3367
3713	BR	Brasil	São Paulo	SP	Poloni	3713
3714	BR	Brasil	São Paulo	SP	Pompéia	3714
3739	BR	Brasil	São Paulo	SP	Quintana	3739
3740	BR	Brasil	São Paulo	SP	Rafard	3740
3741	BR	Brasil	São Paulo	SP	Rancharia	3741
3742	BR	Brasil	São Paulo	SP	Redenção da Serra	3742
3743	BR	Brasil	São Paulo	SP	Regente Feijó	3743
3744	BR	Brasil	São Paulo	SP	Reginópolis	3744
3745	BR	Brasil	São Paulo	SP	Registro	3745
3752	BR	Brasil	São Paulo	SP	Ribeirão Dos Índios	3752
3753	BR	Brasil	São Paulo	SP	Ribeirão Grande	3753
3754	BR	Brasil	São Paulo	SP	Ribeirão Pires	3754
3755	BR	Brasil	São Paulo	SP	Ribeirão Preto	3755
3756	BR	Brasil	São Paulo	SP	Riversul	3756
3757	BR	Brasil	São Paulo	SP	Rifaina	3757
3758	BR	Brasil	São Paulo	SP	Rincão	3758
3759	BR	Brasil	São Paulo	SP	Rinópolis	3759
3770	BR	Brasil	São Paulo	SP	Sales	3770
3771	BR	Brasil	São Paulo	SP	Sales Oliveira	3771
3772	BR	Brasil	São Paulo	SP	Salesópolis	3772
3773	BR	Brasil	São Paulo	SP	Salmourão	3773
3774	BR	Brasil	São Paulo	SP	Saltinho	3774
3775	BR	Brasil	São Paulo	SP	Salto	3775
3776	BR	Brasil	São Paulo	SP	Salto de Pirapora	3776
3777	BR	Brasil	São Paulo	SP	Salto Grande	3777
3778	BR	Brasil	São Paulo	SP	Sandovalina	3778
3779	BR	Brasil	São Paulo	SP	Santa Adélia	3779
3780	BR	Brasil	São Paulo	SP	Santa Albertina	3780
3781	BR	Brasil	São Paulo	SP	Santa Bárbara D´oeste	3781
3782	BR	Brasil	São Paulo	SP	Santa Branca	3782
3783	BR	Brasil	São Paulo	SP	Santa Clara D´oeste	3783
3784	BR	Brasil	São Paulo	SP	Santa Cruz da Conceição	3784
4882	BR	Brasil	Rio Grande do Sul	RS	Nova Candelária	4882
4887	BR	Brasil	Rio Grande do Sul	RS	Nova Petrópolis	4887
115	BR	Brasil	Amazonas	AM	Maués	115
145	BR	Brasil	Roraima	RR	Mucajaí	145
151	BR	Brasil	Roraima	RR	Uiramutã	151
218	BR	Brasil	Pará	PA	Maracanã	218
224	BR	Brasil	Pará	PA	Moju	224
368	BR	Brasil	Tocantins	TO	Guaraí	368
382	BR	Brasil	Tocantins	TO	Luzinópolis	382
612	BR	Brasil	Maranhão	MA	Santa Helena	612
3477	BR	Brasil	São Paulo	SP	Guareí	3477
3478	BR	Brasil	São Paulo	SP	Guariba	3478
3479	BR	Brasil	São Paulo	SP	Guarujá	3479
3480	BR	Brasil	São Paulo	SP	Guarulhos	3480
3481	BR	Brasil	São Paulo	SP	Guatapará	3481
3482	BR	Brasil	São Paulo	SP	Guzolândia	3482
3483	BR	Brasil	São Paulo	SP	Herculândia	3483
3484	BR	Brasil	São Paulo	SP	Holambra	3484
3485	BR	Brasil	São Paulo	SP	Hortolândia	3485
3486	BR	Brasil	São Paulo	SP	Iacanga	3486
3488	BR	Brasil	São Paulo	SP	Iaras	3488
3489	BR	Brasil	São Paulo	SP	Ibaté	3489
4221	BR	Brasil	Paraná	PR	Rio Branco do Sul	4221
4222	BR	Brasil	Paraná	PR	Rio Negro	4222
4223	BR	Brasil	Paraná	PR	Rolândia	4223
4224	BR	Brasil	Paraná	PR	Roncador	4224
4226	BR	Brasil	Paraná	PR	Rosário do Ivaí	4226
4227	BR	Brasil	Paraná	PR	Sabáudia	4227
4228	BR	Brasil	Paraná	PR	Salgado Filho	4228
4229	BR	Brasil	Paraná	PR	Salto do Itararé	4229
4230	BR	Brasil	Paraná	PR	Salto do Lontra	4230
4231	BR	Brasil	Paraná	PR	Santa Amélia	4231
4232	BR	Brasil	Paraná	PR	Santa Cecília do Pavão	4232
4233	BR	Brasil	Paraná	PR	Santa Cruz de Monte Castelo	4233
4234	BR	Brasil	Paraná	PR	Santa fé	4234
4235	BR	Brasil	Paraná	PR	Santa Helena	4235
4236	BR	Brasil	Paraná	PR	Santa Inês	4236
4237	BR	Brasil	Paraná	PR	Santa Isabel do Ivaí	4237
4238	BR	Brasil	Paraná	PR	Santa Izabel do Oeste	4238
4239	BR	Brasil	Paraná	PR	Santa Lúcia	4239
4240	BR	Brasil	Paraná	PR	Santa Maria do Oeste	4240
4583	BR	Brasil	Santa Catarina	SC	Três Barras	4583
4907	BR	Brasil	Rio Grande do Sul	RS	Pareci Novo	4907
4908	BR	Brasil	Rio Grande do Sul	RS	Parobé	4908
4909	BR	Brasil	Rio Grande do Sul	RS	Passa Sete	4909
4910	BR	Brasil	Rio Grande do Sul	RS	Passo do Sobrado	4910
4921	BR	Brasil	Rio Grande do Sul	RS	Pinhal Grande	4921
4922	BR	Brasil	Rio Grande do Sul	RS	Pinheirinho do Vale	4922
4923	BR	Brasil	Rio Grande do Sul	RS	Pinheiro Machado	4923
4924	BR	Brasil	Rio Grande do Sul	RS	Pinto Bandeira	4924
5042	BR	Brasil	Rio Grande do Sul	RS	Sobradinho	5042
92	BR	Brasil	Amazonas	AM	Careiro	92
93	BR	Brasil	Amazonas	AM	Careiro da Várzea	93
152	BR	Brasil	Pará	PA	Abaetetuba	152
285	BR	Brasil	Pará	PA	Tomé-açu	285
369	BR	Brasil	Tocantins	TO	Gurupi	369
2358	BR	Brasil	Minas Gerais	MG	Camanducaia	2358
4282	BR	Brasil	Paraná	PR	Tapejara	4282
4284	BR	Brasil	Paraná	PR	Teixeira Soares	4284
4285	BR	Brasil	Paraná	PR	Telêmaco Borba	4285
4286	BR	Brasil	Paraná	PR	Terra Boa	4286
4288	BR	Brasil	Paraná	PR	Terra Roxa	4288
4289	BR	Brasil	Paraná	PR	Tibagi	4289
4613	BR	Brasil	Rio Grande do Sul	RS	Alegria	4613
4614	BR	Brasil	Rio Grande do Sul	RS	Almirante Tamandaré do Sul	4614
4615	BR	Brasil	Rio Grande do Sul	RS	Alpestre	4615
4616	BR	Brasil	Rio Grande do Sul	RS	Alto Alegre	4616
4617	BR	Brasil	Rio Grande do Sul	RS	Alto Feliz	4617
4618	BR	Brasil	Rio Grande do Sul	RS	Alvorada	4618
4619	BR	Brasil	Rio Grande do Sul	RS	Amaral Ferrador	4619
4620	BR	Brasil	Rio Grande do Sul	RS	Ametista do Sul	4620
4621	BR	Brasil	Rio Grande do Sul	RS	André da Rocha	4621
4622	BR	Brasil	Rio Grande do Sul	RS	Anta Gorda	4622
4820	BR	Brasil	Rio Grande do Sul	RS	Itaqui	4820
4861	BR	Brasil	Rio Grande do Sul	RS	Miraguaí	4861
4862	BR	Brasil	Rio Grande do Sul	RS	Montauri	4862
4863	BR	Brasil	Rio Grande do Sul	RS	Monte Alegre Dos Campos	4863
4865	BR	Brasil	Rio Grande do Sul	RS	Montenegro	4865
4866	BR	Brasil	Rio Grande do Sul	RS	Mormaço	4866
4867	BR	Brasil	Rio Grande do Sul	RS	Morrinhos do Sul	4867
4868	BR	Brasil	Rio Grande do Sul	RS	Morro Redondo	4868
4869	BR	Brasil	Rio Grande do Sul	RS	Morro Reuter	4869
4870	BR	Brasil	Rio Grande do Sul	RS	Mostardas	4870
4871	BR	Brasil	Rio Grande do Sul	RS	Muçum	4871
4872	BR	Brasil	Rio Grande do Sul	RS	Muitos Capões	4872
4873	BR	Brasil	Rio Grande do Sul	RS	Muliterno	4873
4874	BR	Brasil	Rio Grande do Sul	RS	Não-me-toque	4874
4875	BR	Brasil	Rio Grande do Sul	RS	Nicolau Vergueiro	4875
4876	BR	Brasil	Rio Grande do Sul	RS	Nonoai	4876
4877	BR	Brasil	Rio Grande do Sul	RS	Nova Alvorada	4877
4878	BR	Brasil	Rio Grande do Sul	RS	Nova Araçá	4878
4879	BR	Brasil	Rio Grande do Sul	RS	Nova Bassano	4879
4880	BR	Brasil	Rio Grande do Sul	RS	Nova Boa Vista	4880
4881	BR	Brasil	Rio Grande do Sul	RS	Nova Bréscia	4881
71	BR	Brasil	Acre	AC	Sena Madureira	71
116	BR	Brasil	Amazonas	AM	Nhamundá	116
405	BR	Brasil	Tocantins	TO	Pedro Afonso	405
871	BR	Brasil	Piauí	PI	São Miguel do Tapuio	871
872	BR	Brasil	Piauí	PI	São Pedro do Piauí	872
1918	BR	Brasil	Bahia	BA	Castro Alves	1918
2364	BR	Brasil	Minas Gerais	MG	Campina Verde	2364
3977	BR	Brasil	Paraná	PR	Capanema	3977
3978	BR	Brasil	Paraná	PR	Capitão Leônidas Marques	3978
3981	BR	Brasil	Paraná	PR	Cascavel	3981
3983	BR	Brasil	Paraná	PR	Catanduvas	3983
3984	BR	Brasil	Paraná	PR	Centenário do Sul	3984
3985	BR	Brasil	Paraná	PR	Cerro Azul	3985
3986	BR	Brasil	Paraná	PR	Céu Azul	3986
3987	BR	Brasil	Paraná	PR	Chopinzinho	3987
3988	BR	Brasil	Paraná	PR	Cianorte	3988
3989	BR	Brasil	Paraná	PR	Cidade Gaúcha	3989
3990	BR	Brasil	Paraná	PR	Clevelândia	3990
3991	BR	Brasil	Paraná	PR	Colombo	3991
3992	BR	Brasil	Paraná	PR	Colorado	3992
3993	BR	Brasil	Paraná	PR	Congonhinhas	3993
3994	BR	Brasil	Paraná	PR	Conselheiro Mairinck	3994
3995	BR	Brasil	Paraná	PR	Contenda	3995
3996	BR	Brasil	Paraná	PR	Corbélia	3996
3997	BR	Brasil	Paraná	PR	Cornélio Procópio	3997
3998	BR	Brasil	Paraná	PR	Coronel Domingos Soares	3998
3999	BR	Brasil	Paraná	PR	Coronel Vivida	3999
4000	BR	Brasil	Paraná	PR	Corumbataí do Sul	4000
4001	BR	Brasil	Paraná	PR	Cruzeiro do Iguaçu	4001
4002	BR	Brasil	Paraná	PR	Cruzeiro do Oeste	4002
4003	BR	Brasil	Paraná	PR	Cruzeiro do Sul	4003
4004	BR	Brasil	Paraná	PR	Cruz Machado	4004
4005	BR	Brasil	Paraná	PR	Cruzmaltina	4005
4006	BR	Brasil	Paraná	PR	Curitiba	4006
4007	BR	Brasil	Paraná	PR	Curiúva	4007
4008	BR	Brasil	Paraná	PR	Diamante do Norte	4008
4015	BR	Brasil	Paraná	PR	Engenheiro Beltrão	4015
4016	BR	Brasil	Paraná	PR	Esperança Nova	4016
4017	BR	Brasil	Paraná	PR	Entre Rios do Oeste	4017
4018	BR	Brasil	Paraná	PR	Espigão Alto do Iguaçu	4018
4020	BR	Brasil	Paraná	PR	Faxinal	4020
4021	BR	Brasil	Paraná	PR	Fazenda Rio Grande	4021
4022	BR	Brasil	Paraná	PR	Fênix	4022
4023	BR	Brasil	Paraná	PR	Fernandes Pinheiro	4023
4024	BR	Brasil	Paraná	PR	Figueira	4024
4025	BR	Brasil	Paraná	PR	Floraí	4025
4026	BR	Brasil	Paraná	PR	Flor da Serra do Sul	4026
4028	BR	Brasil	Paraná	PR	Florestópolis	4028
4983	BR	Brasil	Rio Grande do Sul	RS	Santo Antônio Das Missões	4983
329	BR	Brasil	Tocantins	TO	Aurora do Tocantins	329
370	BR	Brasil	Tocantins	TO	Ipueiras	370
3088	BR	Brasil	Minas Gerais	MG	Viçosa	3088
3192	BR	Brasil	Rio de Janeiro	RJ	Campos Dos Goytacazes	3192
3193	BR	Brasil	Rio de Janeiro	RJ	Cantagalo	3193
3194	BR	Brasil	Rio de Janeiro	RJ	Cardoso Moreira	3194
3195	BR	Brasil	Rio de Janeiro	RJ	Carmo	3195
3196	BR	Brasil	Rio de Janeiro	RJ	Casimiro de Abreu	3196
3197	BR	Brasil	Rio de Janeiro	RJ	Conceição de Macabu	3197
3198	BR	Brasil	Rio de Janeiro	RJ	Cordeiro	3198
3199	BR	Brasil	Rio de Janeiro	RJ	Duas Barras	3199
3368	BR	Brasil	São Paulo	SP	Caiabu	3368
3369	BR	Brasil	São Paulo	SP	Caieiras	3369
3370	BR	Brasil	São Paulo	SP	Caiuá	3370
3371	BR	Brasil	São Paulo	SP	Cajamar	3371
3372	BR	Brasil	São Paulo	SP	Cajati	3372
3373	BR	Brasil	São Paulo	SP	Cajobi	3373
3375	BR	Brasil	São Paulo	SP	Campina do Monte Alegre	3375
3407	BR	Brasil	São Paulo	SP	Coroados	3407
3408	BR	Brasil	São Paulo	SP	Coronel Macedo	3408
3409	BR	Brasil	São Paulo	SP	Corumbataí	3409
3410	BR	Brasil	São Paulo	SP	Cosmópolis	3410
3411	BR	Brasil	São Paulo	SP	Cosmorama	3411
3413	BR	Brasil	São Paulo	SP	Cravinhos	3413
3870	BR	Brasil	São Paulo	SP	Tarumã	3870
3871	BR	Brasil	São Paulo	SP	Tatuí	3871
3872	BR	Brasil	São Paulo	SP	Taubaté	3872
3873	BR	Brasil	São Paulo	SP	Tejupá	3873
3874	BR	Brasil	São Paulo	SP	Teodoro Sampaio	3874
3875	BR	Brasil	São Paulo	SP	Terra Roxa	3875
3876	BR	Brasil	São Paulo	SP	Tietê	3876
3877	BR	Brasil	São Paulo	SP	Timburi	3877
3878	BR	Brasil	São Paulo	SP	Torre de Pedra	3878
3890	BR	Brasil	São Paulo	SP	Ubirajara	3890
3891	BR	Brasil	São Paulo	SP	Uchoa	3891
3892	BR	Brasil	São Paulo	SP	União Paulista	3892
3893	BR	Brasil	São Paulo	SP	Urânia	3893
3895	BR	Brasil	São Paulo	SP	Urupês	3895
3896	BR	Brasil	São Paulo	SP	Valentim Gentil	3896
3897	BR	Brasil	São Paulo	SP	Valinhos	3897
4899	BR	Brasil	Rio Grande do Sul	RS	Paim Filho	4899
4900	BR	Brasil	Rio Grande do Sul	RS	Palmares do Sul	4900
4901	BR	Brasil	Rio Grande do Sul	RS	Palmeira Das Missões	4901
4902	BR	Brasil	Rio Grande do Sul	RS	Palmitinho	4902
4903	BR	Brasil	Rio Grande do Sul	RS	Panambi	4903
4904	BR	Brasil	Rio Grande do Sul	RS	Pantano Grande	4904
4905	BR	Brasil	Rio Grande do Sul	RS	Paraí	4905
4985	BR	Brasil	Rio Grande do Sul	RS	Santo Augusto	4985
94	BR	Brasil	Amazonas	AM	Coari	94
128	BR	Brasil	Amazonas	AM	São Sebastião do Uatumã	128
153	BR	Brasil	Pará	PA	Abel Figueiredo	153
293	BR	Brasil	Pará	PA	Viseu	293
358	BR	Brasil	Tocantins	TO	Dois Irmãos do Tocantins	358
387	BR	Brasil	Tocantins	TO	Miranorte	387
1337	BR	Brasil	Paraíba	PB	Jericó	1337
1919	BR	Brasil	Bahia	BA	Catolândia	1919
1920	BR	Brasil	Bahia	BA	Catu	1920
1921	BR	Brasil	Bahia	BA	Caturama	1921
2365	BR	Brasil	Minas Gerais	MG	Campo Azul	2365
2623	BR	Brasil	Minas Gerais	MG	Itapecerica	2623
2624	BR	Brasil	Minas Gerais	MG	Itapeva	2624
2635	BR	Brasil	Minas Gerais	MG	Jaboticatubas	2635
2636	BR	Brasil	Minas Gerais	MG	Jacinto	2636
2637	BR	Brasil	Minas Gerais	MG	Jacuí	2637
2638	BR	Brasil	Minas Gerais	MG	Jacutinga	2638
2639	BR	Brasil	Minas Gerais	MG	Jaguaraçu	2639
2640	BR	Brasil	Minas Gerais	MG	Jaíba	2640
2641	BR	Brasil	Minas Gerais	MG	Jampruca	2641
2644	BR	Brasil	Minas Gerais	MG	Japaraíba	2644
2645	BR	Brasil	Minas Gerais	MG	Japonvar	2645
2646	BR	Brasil	Minas Gerais	MG	Jeceaba	2646
2647	BR	Brasil	Minas Gerais	MG	Jenipapo de Minas	2647
2648	BR	Brasil	Minas Gerais	MG	Jequeri	2648
2649	BR	Brasil	Minas Gerais	MG	Jequitaí	2649
2678	BR	Brasil	Minas Gerais	MG	Lamim	2678
3440	BR	Brasil	São Paulo	SP	Espírito Santo do Turvo	3440
3442	BR	Brasil	São Paulo	SP	Estrela do Norte	3442
3443	BR	Brasil	São Paulo	SP	Euclides da Cunha Paulista	3443
3444	BR	Brasil	São Paulo	SP	Fartura	3444
3445	BR	Brasil	São Paulo	SP	Fernandópolis	3445
3446	BR	Brasil	São Paulo	SP	Fernando Prestes	3446
3447	BR	Brasil	São Paulo	SP	Fernão	3447
3448	BR	Brasil	São Paulo	SP	Ferraz de Vasconcelos	3448
3449	BR	Brasil	São Paulo	SP	Flora Rica	3449
3450	BR	Brasil	São Paulo	SP	Floreal	3450
3451	BR	Brasil	São Paulo	SP	Flórida Paulista	3451
3452	BR	Brasil	São Paulo	SP	Florínia	3452
3461	BR	Brasil	São Paulo	SP	General Salgado	3461
3462	BR	Brasil	São Paulo	SP	Getulina	3462
3463	BR	Brasil	São Paulo	SP	Glicério	3463
3464	BR	Brasil	São Paulo	SP	Guaiçara	3464
3465	BR	Brasil	São Paulo	SP	Guaimbê	3465
3466	BR	Brasil	São Paulo	SP	Guaíra	3466
3467	BR	Brasil	São Paulo	SP	Guapiaçu	3467
3468	BR	Brasil	São Paulo	SP	Guapiara	3468
3469	BR	Brasil	São Paulo	SP	Guará	3469
3470	BR	Brasil	São Paulo	SP	Guaraçaí	3470
170	BR	Brasil	Pará	PA	Belém	170
210	BR	Brasil	Pará	PA	Itupiranga	210
238	BR	Brasil	Pará	PA	Pacajá	238
264	BR	Brasil	Pará	PA	Santana do Araguaia	264
314	BR	Brasil	Tocantins	TO	Aliança do Tocantins	314
343	BR	Brasil	Tocantins	TO	Carmolândia	343
1338	BR	Brasil	Paraíba	PB	João Pessoa	1338
1922	BR	Brasil	Bahia	BA	Central	1922
2404	BR	Brasil	Minas Gerais	MG	Carvalhópolis	2404
2405	BR	Brasil	Minas Gerais	MG	Carvalhos	2405
2406	BR	Brasil	Minas Gerais	MG	Casa Grande	2406
2407	BR	Brasil	Minas Gerais	MG	Cascalho Rico	2407
2462	BR	Brasil	Minas Gerais	MG	Córrego do Bom Jesus	2462
2463	BR	Brasil	Minas Gerais	MG	Córrego Fundo	2463
2464	BR	Brasil	Minas Gerais	MG	Córrego Novo	2464
2465	BR	Brasil	Minas Gerais	MG	Couto de Magalhães de Minas	2465
2466	BR	Brasil	Minas Gerais	MG	Crisólita	2466
2496	BR	Brasil	Minas Gerais	MG	Dom Cavati	2496
2497	BR	Brasil	Minas Gerais	MG	Dom Joaquim	2497
2510	BR	Brasil	Minas Gerais	MG	Engenheiro Navarro	2510
2511	BR	Brasil	Minas Gerais	MG	Entre Folhas	2511
2512	BR	Brasil	Minas Gerais	MG	Entre Rios de Minas	2512
2513	BR	Brasil	Minas Gerais	MG	Ervália	2513
2514	BR	Brasil	Minas Gerais	MG	Esmeraldas	2514
2515	BR	Brasil	Minas Gerais	MG	Espera Feliz	2515
2553	BR	Brasil	Minas Gerais	MG	Glaucilândia	2553
2554	BR	Brasil	Minas Gerais	MG	Goiabeira	2554
2555	BR	Brasil	Minas Gerais	MG	Goianá	2555
2605	BR	Brasil	Minas Gerais	MG	Itabira	2605
2606	BR	Brasil	Minas Gerais	MG	Itabirinha	2606
2607	BR	Brasil	Minas Gerais	MG	Itabirito	2607
2608	BR	Brasil	Minas Gerais	MG	Itacambira	2608
2609	BR	Brasil	Minas Gerais	MG	Itacarambi	2609
2610	BR	Brasil	Minas Gerais	MG	Itaguara	2610
2613	BR	Brasil	Minas Gerais	MG	Itamarandiba	2613
2617	BR	Brasil	Minas Gerais	MG	Itamogi	2617
2618	BR	Brasil	Minas Gerais	MG	Itamonte	2618
2619	BR	Brasil	Minas Gerais	MG	Itanhandu	2619
4765	BR	Brasil	Rio Grande do Sul	RS	Estrela	4765
4766	BR	Brasil	Rio Grande do Sul	RS	Estrela Velha	4766
4821	BR	Brasil	Rio Grande do Sul	RS	Itati	4821
4845	BR	Brasil	Rio Grande do Sul	RS	Maçambara	4845
4846	BR	Brasil	Rio Grande do Sul	RS	Mampituba	4846
4997	BR	Brasil	Rio Grande do Sul	RS	São José Das Missões	4997
95	BR	Brasil	Amazonas	AM	Codajás	95
146	BR	Brasil	Roraima	RR	Normandia	146
259	BR	Brasil	Pará	PA	Santa Cruz do Arari	259
265	BR	Brasil	Pará	PA	Santarém	265
613	BR	Brasil	Maranhão	MA	Santa Inês	613
614	BR	Brasil	Maranhão	MA	Santa Luzia	614
873	BR	Brasil	Piauí	PI	São Raimundo Nonato	873
877	BR	Brasil	Piauí	PI	Simões	877
1923	BR	Brasil	Bahia	BA	Chorrochó	1923
2620	BR	Brasil	Minas Gerais	MG	Itanhomi	2620
3613	BR	Brasil	São Paulo	SP	Moji-mirim	3613
3614	BR	Brasil	São Paulo	SP	Mombuca	3614
3615	BR	Brasil	São Paulo	SP	Monções	3615
3616	BR	Brasil	São Paulo	SP	Mongaguá	3616
3617	BR	Brasil	São Paulo	SP	Monte Alegre do Sul	3617
3618	BR	Brasil	São Paulo	SP	Monte Alto	3618
3619	BR	Brasil	São Paulo	SP	Monte Aprazível	3619
3620	BR	Brasil	São Paulo	SP	Monte Azul Paulista	3620
3621	BR	Brasil	São Paulo	SP	Monte Castelo	3621
3633	BR	Brasil	São Paulo	SP	Nhandeara	3633
4283	BR	Brasil	Paraná	PR	Tapira	4283
4433	BR	Brasil	Santa Catarina	SC	Irati	4433
4462	BR	Brasil	Santa Catarina	SC	Luzerna	4462
4463	BR	Brasil	Santa Catarina	SC	Macieira	4463
4464	BR	Brasil	Santa Catarina	SC	Mafra	4464
4491	BR	Brasil	Santa Catarina	SC	Painel	4491
4492	BR	Brasil	Santa Catarina	SC	Palhoça	4492
4493	BR	Brasil	Santa Catarina	SC	Palma Sola	4493
4494	BR	Brasil	Santa Catarina	SC	Palmeira	4494
4495	BR	Brasil	Santa Catarina	SC	Palmitos	4495
4496	BR	Brasil	Santa Catarina	SC	Papanduva	4496
4497	BR	Brasil	Santa Catarina	SC	Paraíso	4497
4498	BR	Brasil	Santa Catarina	SC	Passo de Torres	4498
4499	BR	Brasil	Santa Catarina	SC	Passos Maia	4499
4500	BR	Brasil	Santa Catarina	SC	Paulo Lopes	4500
4501	BR	Brasil	Santa Catarina	SC	Pedras Grandes	4501
4502	BR	Brasil	Santa Catarina	SC	Penha	4502
4503	BR	Brasil	Santa Catarina	SC	Peritiba	4503
4504	BR	Brasil	Santa Catarina	SC	Pescaria Brava	4504
4505	BR	Brasil	Santa Catarina	SC	Petrolândia	4505
4506	BR	Brasil	Santa Catarina	SC	Piçarras	4506
4507	BR	Brasil	Santa Catarina	SC	Pinhalzinho	4507
4508	BR	Brasil	Santa Catarina	SC	Pinheiro Preto	4508
4636	BR	Brasil	Rio Grande do Sul	RS	Bagé	4636
4695	BR	Brasil	Rio Grande do Sul	RS	Carazinho	4695
157	BR	Brasil	Pará	PA	Alenquer	157
191	BR	Brasil	Pará	PA	Concórdia do Pará	191
211	BR	Brasil	Pará	PA	Jacareacanga	211
616	BR	Brasil	Maranhão	MA	Santa Quitéria do Maranhão	616
892	BR	Brasil	Ceará	CE	Abaiara	892
3339	BR	Brasil	São Paulo	SP	Bertioga	3339
3746	BR	Brasil	São Paulo	SP	Restinga	3746
3747	BR	Brasil	São Paulo	SP	Ribeira	3747
3748	BR	Brasil	São Paulo	SP	Ribeirão Bonito	3748
3749	BR	Brasil	São Paulo	SP	Ribeirão Branco	3749
3750	BR	Brasil	São Paulo	SP	Ribeirão Corrente	3750
3751	BR	Brasil	São Paulo	SP	Ribeirão do Sul	3751
4519	BR	Brasil	Santa Catarina	SC	Presidente Castelo Branco	4519
4520	BR	Brasil	Santa Catarina	SC	Presidente Getúlio	4520
4521	BR	Brasil	Santa Catarina	SC	Presidente Nereu	4521
4522	BR	Brasil	Santa Catarina	SC	Princesa	4522
4523	BR	Brasil	Santa Catarina	SC	Quilombo	4523
4524	BR	Brasil	Santa Catarina	SC	Rancho Queimado	4524
4525	BR	Brasil	Santa Catarina	SC	Rio Das Antas	4525
4526	BR	Brasil	Santa Catarina	SC	Rio do Campo	4526
4527	BR	Brasil	Santa Catarina	SC	Rio do Oeste	4527
4528	BR	Brasil	Santa Catarina	SC	Rio Dos Cedros	4528
4538	BR	Brasil	Santa Catarina	SC	Salto Veloso	4538
4742	BR	Brasil	Rio Grande do Sul	RS	Dom Pedro de Alcântara	4742
4743	BR	Brasil	Rio Grande do Sul	RS	Dom Pedrito	4743
4744	BR	Brasil	Rio Grande do Sul	RS	Dona Francisca	4744
4745	BR	Brasil	Rio Grande do Sul	RS	Doutor Maurício Cardoso	4745
4746	BR	Brasil	Rio Grande do Sul	RS	Doutor Ricardo	4746
4747	BR	Brasil	Rio Grande do Sul	RS	Eldorado do Sul	4747
4748	BR	Brasil	Rio Grande do Sul	RS	Encantado	4748
4749	BR	Brasil	Rio Grande do Sul	RS	Encruzilhada do Sul	4749
4750	BR	Brasil	Rio Grande do Sul	RS	Engenho Velho	4750
4751	BR	Brasil	Rio Grande do Sul	RS	Entre-ijuís	4751
4752	BR	Brasil	Rio Grande do Sul	RS	Entre Rios do Sul	4752
4753	BR	Brasil	Rio Grande do Sul	RS	Erebango	4753
4754	BR	Brasil	Rio Grande do Sul	RS	Erechim	4754
4755	BR	Brasil	Rio Grande do Sul	RS	Ernestina	4755
4756	BR	Brasil	Rio Grande do Sul	RS	Herval	4756
4757	BR	Brasil	Rio Grande do Sul	RS	Erval Grande	4757
4758	BR	Brasil	Rio Grande do Sul	RS	Erval Seco	4758
4759	BR	Brasil	Rio Grande do Sul	RS	Esmeralda	4759
4760	BR	Brasil	Rio Grande do Sul	RS	Esperança do Sul	4760
4761	BR	Brasil	Rio Grande do Sul	RS	Espumoso	4761
4762	BR	Brasil	Rio Grande do Sul	RS	Estação	4762
72	BR	Brasil	Acre	AC	Tarauacá	72
299	BR	Brasil	Amapá	AP	Calçoene	299
300	BR	Brasil	Amapá	AP	Cutias	300
324	BR	Brasil	Tocantins	TO	Araguanã	324
395	BR	Brasil	Tocantins	TO	Nova Rosalândia	395
3491	BR	Brasil	São Paulo	SP	Ibirarema	3491
3492	BR	Brasil	São Paulo	SP	Ibitinga	3492
3513	BR	Brasil	São Paulo	SP	Iracemápolis	3513
3514	BR	Brasil	São Paulo	SP	Irapuã	3514
3515	BR	Brasil	São Paulo	SP	Irapuru	3515
3516	BR	Brasil	São Paulo	SP	Itaberá	3516
3517	BR	Brasil	São Paulo	SP	Itaí	3517
3518	BR	Brasil	São Paulo	SP	Itajobi	3518
3519	BR	Brasil	São Paulo	SP	Itaju	3519
3520	BR	Brasil	São Paulo	SP	Itanhaém	3520
3521	BR	Brasil	São Paulo	SP	Itaóca	3521
3522	BR	Brasil	São Paulo	SP	Itapecerica da Serra	3522
3523	BR	Brasil	São Paulo	SP	Itapetininga	3523
3524	BR	Brasil	São Paulo	SP	Itapeva	3524
3525	BR	Brasil	São Paulo	SP	Itapevi	3525
3526	BR	Brasil	São Paulo	SP	Itapira	3526
3527	BR	Brasil	São Paulo	SP	Itapirapuã Paulista	3527
3528	BR	Brasil	São Paulo	SP	Itápolis	3528
3529	BR	Brasil	São Paulo	SP	Itaporanga	3529
3530	BR	Brasil	São Paulo	SP	Itapuí	3530
3531	BR	Brasil	São Paulo	SP	Itapura	3531
3532	BR	Brasil	São Paulo	SP	Itaquaquecetuba	3532
3533	BR	Brasil	São Paulo	SP	Itararé	3533
3534	BR	Brasil	São Paulo	SP	Itariri	3534
3535	BR	Brasil	São Paulo	SP	Itatiba	3535
3536	BR	Brasil	São Paulo	SP	Itatinga	3536
3537	BR	Brasil	São Paulo	SP	Itirapina	3537
3538	BR	Brasil	São Paulo	SP	Itirapuã	3538
3539	BR	Brasil	São Paulo	SP	Itobi	3539
3541	BR	Brasil	São Paulo	SP	Itupeva	3541
3542	BR	Brasil	São Paulo	SP	Ituverava	3542
3543	BR	Brasil	São Paulo	SP	Jaborandi	3543
3544	BR	Brasil	São Paulo	SP	Jaboticabal	3544
3545	BR	Brasil	São Paulo	SP	Jacareí	3545
3546	BR	Brasil	São Paulo	SP	Jaci	3546
3552	BR	Brasil	São Paulo	SP	Jardinópolis	3552
3554	BR	Brasil	São Paulo	SP	Jaú	3554
3555	BR	Brasil	São Paulo	SP	Jeriquara	3555
3556	BR	Brasil	São Paulo	SP	Joanópolis	3556
3557	BR	Brasil	São Paulo	SP	João Ramalho	3557
3558	BR	Brasil	São Paulo	SP	José Bonifácio	3558
3559	BR	Brasil	São Paulo	SP	Júlio Mesquita	3559
3560	BR	Brasil	São Paulo	SP	Jumirim	3560
3561	BR	Brasil	São Paulo	SP	Jundiaí	3561
3562	BR	Brasil	São Paulo	SP	Junqueirópolis	3562
154	BR	Brasil	Pará	PA	Acará	154
2352	BR	Brasil	Minas Gerais	MG	Caetanópolis	2352
3972	BR	Brasil	Paraná	PR	Campo Magro	3972
3973	BR	Brasil	Paraná	PR	Campo Mourão	3973
4591	BR	Brasil	Santa Catarina	SC	União do Oeste	4591
4592	BR	Brasil	Santa Catarina	SC	Urubici	4592
4593	BR	Brasil	Santa Catarina	SC	Urupema	4593
4599	BR	Brasil	Santa Catarina	SC	Videira	4599
4767	BR	Brasil	Rio Grande do Sul	RS	Eugênio de Castro	4767
4768	BR	Brasil	Rio Grande do Sul	RS	Fagundes Varela	4768
4769	BR	Brasil	Rio Grande do Sul	RS	Farroupilha	4769
4770	BR	Brasil	Rio Grande do Sul	RS	Faxinal do Soturno	4770
4771	BR	Brasil	Rio Grande do Sul	RS	Faxinalzinho	4771
4772	BR	Brasil	Rio Grande do Sul	RS	Fazenda Vilanova	4772
4773	BR	Brasil	Rio Grande do Sul	RS	Feliz	4773
4774	BR	Brasil	Rio Grande do Sul	RS	Flores da Cunha	4774
4775	BR	Brasil	Rio Grande do Sul	RS	Floriano Peixoto	4775
4776	BR	Brasil	Rio Grande do Sul	RS	Fontoura Xavier	4776
4777	BR	Brasil	Rio Grande do Sul	RS	Formigueiro	4777
4778	BR	Brasil	Rio Grande do Sul	RS	Forquetinha	4778
4779	BR	Brasil	Rio Grande do Sul	RS	Fortaleza Dos Valos	4779
4780	BR	Brasil	Rio Grande do Sul	RS	Frederico Westphalen	4780
4781	BR	Brasil	Rio Grande do Sul	RS	Garibaldi	4781
4782	BR	Brasil	Rio Grande do Sul	RS	Garruchos	4782
4783	BR	Brasil	Rio Grande do Sul	RS	Gaurama	4783
4784	BR	Brasil	Rio Grande do Sul	RS	General Câmara	4784
4785	BR	Brasil	Rio Grande do Sul	RS	Gentil	4785
4786	BR	Brasil	Rio Grande do Sul	RS	Getúlio Vargas	4786
4787	BR	Brasil	Rio Grande do Sul	RS	Giruá	4787
4788	BR	Brasil	Rio Grande do Sul	RS	Glorinha	4788
4789	BR	Brasil	Rio Grande do Sul	RS	Gramado	4789
4790	BR	Brasil	Rio Grande do Sul	RS	Gramado Dos Loureiros	4790
4791	BR	Brasil	Rio Grande do Sul	RS	Gramado Xavier	4791
4807	BR	Brasil	Rio Grande do Sul	RS	Igrejinha	4807
4808	BR	Brasil	Rio Grande do Sul	RS	Ijuí	4808
4809	BR	Brasil	Rio Grande do Sul	RS	Ilópolis	4809
4810	BR	Brasil	Rio Grande do Sul	RS	Imbé	4810
4811	BR	Brasil	Rio Grande do Sul	RS	Imigrante	4811
4812	BR	Brasil	Rio Grande do Sul	RS	Independência	4812
4813	BR	Brasil	Rio Grande do Sul	RS	Inhacorá	4813
4815	BR	Brasil	Rio Grande do Sul	RS	Ipiranga do Sul	4815
4816	BR	Brasil	Rio Grande do Sul	RS	Iraí	4816
4817	BR	Brasil	Rio Grande do Sul	RS	Itaara	4817
4819	BR	Brasil	Rio Grande do Sul	RS	Itapuca	4819
893	BR	Brasil	Ceará	CE	Acarapé	893
1924	BR	Brasil	Bahia	BA	Cícero Dantas	1924
1925	BR	Brasil	Bahia	BA	Cipó	1925
3089	BR	Brasil	Minas Gerais	MG	Vieiras	3089
3090	BR	Brasil	Minas Gerais	MG	Mathias Lobato	3090
3091	BR	Brasil	Minas Gerais	MG	Virgem da Lapa	3091
3092	BR	Brasil	Minas Gerais	MG	Virgínia	3092
3093	BR	Brasil	Minas Gerais	MG	Virginópolis	3093
3094	BR	Brasil	Minas Gerais	MG	Virgolândia	3094
3095	BR	Brasil	Minas Gerais	MG	Visconde do Rio Branco	3095
3096	BR	Brasil	Minas Gerais	MG	Volta Grande	3096
3097	BR	Brasil	Minas Gerais	MG	Wenceslau Braz	3097
3098	BR	Brasil	Espírito Santo	ES	Afonso Cláudio	3098
3121	BR	Brasil	Espírito Santo	ES	Dores do Rio Preto	3121
3122	BR	Brasil	Espírito Santo	ES	Ecoporanga	3122
3123	BR	Brasil	Espírito Santo	ES	Fundão	3123
3124	BR	Brasil	Espírito Santo	ES	Governador Lindenberg	3124
3125	BR	Brasil	Espírito Santo	ES	Guaçuí	3125
3126	BR	Brasil	Espírito Santo	ES	Guarapari	3126
3127	BR	Brasil	Espírito Santo	ES	Ibatiba	3127
3128	BR	Brasil	Espírito Santo	ES	Ibiraçu	3128
3129	BR	Brasil	Espírito Santo	ES	Ibitirama	3129
3156	BR	Brasil	Espírito Santo	ES	Presidente Kennedy	3156
3158	BR	Brasil	Espírito Santo	ES	Rio Novo do Sul	3158
3159	BR	Brasil	Espírito Santo	ES	Santa Leopoldina	3159
3160	BR	Brasil	Espírito Santo	ES	Santa Maria de Jetibá	3160
3161	BR	Brasil	Espírito Santo	ES	Santa Teresa	3161
3162	BR	Brasil	Espírito Santo	ES	São Domingos do Norte	3162
3163	BR	Brasil	Espírito Santo	ES	São Gabriel da Palha	3163
3164	BR	Brasil	Espírito Santo	ES	São José do Calçado	3164
3171	BR	Brasil	Espírito Santo	ES	Viana	3171
3172	BR	Brasil	Espírito Santo	ES	Vila Pavão	3172
3173	BR	Brasil	Espírito Santo	ES	Vila Valério	3173
3174	BR	Brasil	Espírito Santo	ES	Vila Velha	3174
3175	BR	Brasil	Espírito Santo	ES	Vitória	3175
3176	BR	Brasil	Rio de Janeiro	RJ	Angra Dos Reis	3176
3177	BR	Brasil	Rio de Janeiro	RJ	Aperibé	3177
3178	BR	Brasil	Rio de Janeiro	RJ	Araruama	3178
3179	BR	Brasil	Rio de Janeiro	RJ	Areal	3179
3180	BR	Brasil	Rio de Janeiro	RJ	Armação Dos Búzios	3180
3181	BR	Brasil	Rio de Janeiro	RJ	Arraial do Cabo	3181
3182	BR	Brasil	Rio de Janeiro	RJ	Barra do Piraí	3182
4556	BR	Brasil	Santa Catarina	SC	São João Batista	4556
4557	BR	Brasil	Santa Catarina	SC	São João do Itaperiú	4557
5014	BR	Brasil	Rio Grande do Sul	RS	São Pedro da Serra	5014
5050	BR	Brasil	Rio Grande do Sul	RS	Taquaruçu do Sul	5050
122	BR	Brasil	Amazonas	AM	Presidente Figueiredo	122
417	BR	Brasil	Tocantins	TO	Presidente Kennedy	417
895	BR	Brasil	Ceará	CE	Acopiara	895
896	BR	Brasil	Ceará	CE	Aiuaba	896
897	BR	Brasil	Ceará	CE	Alcântaras	897
1926	BR	Brasil	Bahia	BA	Coaraci	1926
1927	BR	Brasil	Bahia	BA	Cocos	1927
3237	BR	Brasil	Rio de Janeiro	RJ	Quissamã	3237
3238	BR	Brasil	Rio de Janeiro	RJ	Resende	3238
3286	BR	Brasil	São Paulo	SP	Americana	3286
3309	BR	Brasil	São Paulo	SP	Areiópolis	3309
3310	BR	Brasil	São Paulo	SP	Ariranha	3310
3311	BR	Brasil	São Paulo	SP	Artur Nogueira	3311
3330	BR	Brasil	São Paulo	SP	Barretos	3330
4104	BR	Brasil	Paraná	PR	Luiziana	4104
4105	BR	Brasil	Paraná	PR	Lunardelli	4105
4106	BR	Brasil	Paraná	PR	Lupionópolis	4106
4107	BR	Brasil	Paraná	PR	Mallet	4107
4108	BR	Brasil	Paraná	PR	Mamborê	4108
4109	BR	Brasil	Paraná	PR	Mandaguaçu	4109
4110	BR	Brasil	Paraná	PR	Mandaguari	4110
4111	BR	Brasil	Paraná	PR	Mandirituba	4111
4112	BR	Brasil	Paraná	PR	Manfrinópolis	4112
4113	BR	Brasil	Paraná	PR	Mangueirinha	4113
4114	BR	Brasil	Paraná	PR	Manoel Ribas	4114
4115	BR	Brasil	Paraná	PR	Marechal Cândido Rondon	4115
4116	BR	Brasil	Paraná	PR	Maria Helena	4116
4117	BR	Brasil	Paraná	PR	Marialva	4117
4435	BR	Brasil	Santa Catarina	SC	Itá	4435
4440	BR	Brasil	Santa Catarina	SC	Itapoá	4440
4441	BR	Brasil	Santa Catarina	SC	Ituporanga	4441
4442	BR	Brasil	Santa Catarina	SC	Jaborá	4442
4443	BR	Brasil	Santa Catarina	SC	Jacinto Machado	4443
4444	BR	Brasil	Santa Catarina	SC	Jaguaruna	4444
4445	BR	Brasil	Santa Catarina	SC	Jaraguá do Sul	4445
4446	BR	Brasil	Santa Catarina	SC	Jardinópolis	4446
4447	BR	Brasil	Santa Catarina	SC	Joaçaba	4447
4448	BR	Brasil	Santa Catarina	SC	Joinville	4448
4449	BR	Brasil	Santa Catarina	SC	José Boiteux	4449
4450	BR	Brasil	Santa Catarina	SC	Jupiá	4450
4451	BR	Brasil	Santa Catarina	SC	Lacerdópolis	4451
4452	BR	Brasil	Santa Catarina	SC	Lages	4452
4455	BR	Brasil	Santa Catarina	SC	Laurentino	4455
4456	BR	Brasil	Santa Catarina	SC	Lauro Muller	4456
4457	BR	Brasil	Santa Catarina	SC	Lebon Régis	4457
73	BR	Brasil	Acre	AC	Xapuri	73
117	BR	Brasil	Amazonas	AM	Nova Olinda do Norte	117
246	BR	Brasil	Pará	PA	Ponta de Pedras	246
350	BR	Brasil	Tocantins	TO	Combinado	350
359	BR	Brasil	Tocantins	TO	Dueré	359
360	BR	Brasil	Tocantins	TO	Esperantina	360
388	BR	Brasil	Tocantins	TO	Monte do Carmo	388
620	BR	Brasil	Maranhão	MA	Santo Antônio Dos Lopes	620
1928	BR	Brasil	Bahia	BA	Conceição da Feira	1928
1929	BR	Brasil	Bahia	BA	Conceição do Almeida	1929
1930	BR	Brasil	Bahia	BA	Conceição do Coité	1930
1931	BR	Brasil	Bahia	BA	Conceição do Jacuípe	1931
1932	BR	Brasil	Bahia	BA	Conde	1932
1933	BR	Brasil	Bahia	BA	Condeúba	1933
1934	BR	Brasil	Bahia	BA	Contendas do Sincorá	1934
1935	BR	Brasil	Bahia	BA	Coração de Maria	1935
1936	BR	Brasil	Bahia	BA	Cordeiros	1936
1937	BR	Brasil	Bahia	BA	Coribe	1937
1938	BR	Brasil	Bahia	BA	Coronel João sá	1938
2516	BR	Brasil	Minas Gerais	MG	Espinosa	2516
2522	BR	Brasil	Minas Gerais	MG	Eugenópolis	2522
2523	BR	Brasil	Minas Gerais	MG	Ewbank da Câmara	2523
2524	BR	Brasil	Minas Gerais	MG	Extrema	2524
2525	BR	Brasil	Minas Gerais	MG	Fama	2525
2526	BR	Brasil	Minas Gerais	MG	Faria Lemos	2526
2527	BR	Brasil	Minas Gerais	MG	Felício Dos Santos	2527
2528	BR	Brasil	Minas Gerais	MG	São Gonçalo do Rio Preto	2528
2529	BR	Brasil	Minas Gerais	MG	Felisburgo	2529
2530	BR	Brasil	Minas Gerais	MG	Felixlândia	2530
2558	BR	Brasil	Minas Gerais	MG	Gouveia	2558
2559	BR	Brasil	Minas Gerais	MG	Governador Valadares	2559
2560	BR	Brasil	Minas Gerais	MG	Grão Mogol	2560
2561	BR	Brasil	Minas Gerais	MG	Grupiara	2561
2562	BR	Brasil	Minas Gerais	MG	Guanhães	2562
2563	BR	Brasil	Minas Gerais	MG	Guapé	2563
2601	BR	Brasil	Minas Gerais	MG	Ipatinga	2601
2602	BR	Brasil	Minas Gerais	MG	Ipiaçu	2602
2603	BR	Brasil	Minas Gerais	MG	Ipuiúna	2603
2604	BR	Brasil	Minas Gerais	MG	Iraí de Minas	2604
4995	BR	Brasil	Rio Grande do Sul	RS	São João do Polêsine	4995
4996	BR	Brasil	Rio Grande do Sul	RS	São Jorge	4996
4998	BR	Brasil	Rio Grande do Sul	RS	São José do Herval	4998
4999	BR	Brasil	Rio Grande do Sul	RS	São José do Hortêncio	4999
5000	BR	Brasil	Rio Grande do Sul	RS	São José do Inhacorá	5000
5001	BR	Brasil	Rio Grande do Sul	RS	São José do Norte	5001
5002	BR	Brasil	Rio Grande do Sul	RS	São José do Ouro	5002
5003	BR	Brasil	Rio Grande do Sul	RS	São José do Sul	5003
118	BR	Brasil	Amazonas	AM	Novo Airão	118
119	BR	Brasil	Amazonas	AM	Novo Aripuanã	119
130	BR	Brasil	Amazonas	AM	Tabatinga	130
155	BR	Brasil	Pará	PA	Afuá	155
171	BR	Brasil	Pará	PA	Belterra	171
260	BR	Brasil	Pará	PA	Santa Isabel do Pará	260
274	BR	Brasil	Pará	PA	São João da Ponta	274
286	BR	Brasil	Pará	PA	Tracuateua	286
294	BR	Brasil	Pará	PA	Vitória do Xingu	294
315	BR	Brasil	Tocantins	TO	Almas	315
330	BR	Brasil	Tocantins	TO	Axixá do Tocantins	330
396	BR	Brasil	Tocantins	TO	Novo Acordo	396
413	BR	Brasil	Tocantins	TO	Ponte Alta do Tocantins	413
621	BR	Brasil	Maranhão	MA	São Benedito do Rio Preto	621
1888	BR	Brasil	Bahia	BA	Cabaceiras do Paraguaçu	1888
1889	BR	Brasil	Bahia	BA	Cachoeira	1889
2643	BR	Brasil	Minas Gerais	MG	Januária	2643
3493	BR	Brasil	São Paulo	SP	Ibiúna	3493
3494	BR	Brasil	São Paulo	SP	Icém	3494
3497	BR	Brasil	São Paulo	SP	Igarapava	3497
3498	BR	Brasil	São Paulo	SP	Igaratá	3498
3499	BR	Brasil	São Paulo	SP	Iguape	3499
3500	BR	Brasil	São Paulo	SP	Ilhabela	3500
3501	BR	Brasil	São Paulo	SP	Ilha Comprida	3501
3502	BR	Brasil	São Paulo	SP	Ilha Solteira	3502
3503	BR	Brasil	São Paulo	SP	Indaiatuba	3503
3504	BR	Brasil	São Paulo	SP	Indiana	3504
3505	BR	Brasil	São Paulo	SP	Indiaporã	3505
3506	BR	Brasil	São Paulo	SP	Inúbia Paulista	3506
3507	BR	Brasil	São Paulo	SP	Ipaussu	3507
3508	BR	Brasil	São Paulo	SP	Iperó	3508
3509	BR	Brasil	São Paulo	SP	Ipeúna	3509
3510	BR	Brasil	São Paulo	SP	Ipiguá	3510
3511	BR	Brasil	São Paulo	SP	Iporanga	3511
4101	BR	Brasil	Paraná	PR	Loanda	4101
4626	BR	Brasil	Rio Grande do Sul	RS	Aratiba	4626
4912	BR	Brasil	Rio Grande do Sul	RS	Paulo Bento	4912
4913	BR	Brasil	Rio Grande do Sul	RS	Paverama	4913
4914	BR	Brasil	Rio Grande do Sul	RS	Pedras Altas	4914
4915	BR	Brasil	Rio Grande do Sul	RS	Pedro Osório	4915
4917	BR	Brasil	Rio Grande do Sul	RS	Pelotas	4917
4918	BR	Brasil	Rio Grande do Sul	RS	Picada Café	4918
4919	BR	Brasil	Rio Grande do Sul	RS	Pinhal	4919
4920	BR	Brasil	Rio Grande do Sul	RS	Pinhal da Serra	4920
212	BR	Brasil	Pará	PA	Jacundá	212
213	BR	Brasil	Pará	PA	Juruti	213
247	BR	Brasil	Pará	PA	Portel	247
361	BR	Brasil	Tocantins	TO	Fátima	361
623	BR	Brasil	Maranhão	MA	São Bernardo	623
1339	BR	Brasil	Paraíba	PB	Juarez Távora	1339
3547	BR	Brasil	São Paulo	SP	Jacupiranga	3547
3548	BR	Brasil	São Paulo	SP	Jaguariúna	3548
3549	BR	Brasil	São Paulo	SP	Jales	3549
3550	BR	Brasil	São Paulo	SP	Jambeiro	3550
3551	BR	Brasil	São Paulo	SP	Jandira	3551
3553	BR	Brasil	São Paulo	SP	Jarinu	3553
3964	BR	Brasil	Paraná	PR	Cambé	3964
4135	BR	Brasil	Paraná	PR	Missal	4135
4242	BR	Brasil	Paraná	PR	Santa Mônica	4242
4243	BR	Brasil	Paraná	PR	Santana do Itararé	4243
4244	BR	Brasil	Paraná	PR	Santa Tereza do Oeste	4244
4245	BR	Brasil	Paraná	PR	Santa Terezinha de Itaipu	4245
4246	BR	Brasil	Paraná	PR	Santo Antônio da Platina	4246
4247	BR	Brasil	Paraná	PR	Santo Antônio do Caiuá	4247
4248	BR	Brasil	Paraná	PR	Santo Antônio do Paraíso	4248
4249	BR	Brasil	Paraná	PR	Santo Antônio do Sudoeste	4249
4250	BR	Brasil	Paraná	PR	Santo Inácio	4250
4251	BR	Brasil	Paraná	PR	São Carlos do Ivaí	4251
4252	BR	Brasil	Paraná	PR	São Jerônimo da Serra	4252
4253	BR	Brasil	Paraná	PR	São João	4253
4254	BR	Brasil	Paraná	PR	São João do Caiuá	4254
4656	BR	Brasil	Rio Grande do Sul	RS	Bom Princípio	4656
4657	BR	Brasil	Rio Grande do Sul	RS	Bom Progresso	4657
4658	BR	Brasil	Rio Grande do Sul	RS	Bom Retiro do Sul	4658
4659	BR	Brasil	Rio Grande do Sul	RS	Boqueirão do Leão	4659
4661	BR	Brasil	Rio Grande do Sul	RS	Bozano	4661
4662	BR	Brasil	Rio Grande do Sul	RS	Braga	4662
4663	BR	Brasil	Rio Grande do Sul	RS	Brochier	4663
4664	BR	Brasil	Rio Grande do Sul	RS	Butiá	4664
4665	BR	Brasil	Rio Grande do Sul	RS	Caçapava do Sul	4665
4666	BR	Brasil	Rio Grande do Sul	RS	Cacequi	4666
4667	BR	Brasil	Rio Grande do Sul	RS	Cachoeira do Sul	4667
4668	BR	Brasil	Rio Grande do Sul	RS	Cachoeirinha	4668
4669	BR	Brasil	Rio Grande do Sul	RS	Cacique Doble	4669
4670	BR	Brasil	Rio Grande do Sul	RS	Caibaté	4670
4671	BR	Brasil	Rio Grande do Sul	RS	Caiçara	4671
4672	BR	Brasil	Rio Grande do Sul	RS	Camaquã	4672
4673	BR	Brasil	Rio Grande do Sul	RS	Camargo	4673
4674	BR	Brasil	Rio Grande do Sul	RS	Cambará do Sul	4674
275	BR	Brasil	Pará	PA	São João de Pirabas	275
325	BR	Brasil	Tocantins	TO	Araguatins	325
344	BR	Brasil	Tocantins	TO	Carrasco Bonito	344
1340	BR	Brasil	Paraíba	PB	Juazeirinho	1340
2408	BR	Brasil	Minas Gerais	MG	Cássia	2408
2409	BR	Brasil	Minas Gerais	MG	Conceição da Barra de Minas	2409
2410	BR	Brasil	Minas Gerais	MG	Cataguases	2410
2411	BR	Brasil	Minas Gerais	MG	Catas Altas	2411
2412	BR	Brasil	Minas Gerais	MG	Catas Altas da Noruega	2412
2433	BR	Brasil	Minas Gerais	MG	Conceição Das Pedras	2433
2434	BR	Brasil	Minas Gerais	MG	Conceição Das Alagoas	2434
2435	BR	Brasil	Minas Gerais	MG	Conceição de Ipanema	2435
2436	BR	Brasil	Minas Gerais	MG	Conceição do Mato Dentro	2436
2437	BR	Brasil	Minas Gerais	MG	Conceição do Pará	2437
2438	BR	Brasil	Minas Gerais	MG	Conceição do Rio Verde	2438
2439	BR	Brasil	Minas Gerais	MG	Conceição Dos Ouros	2439
2440	BR	Brasil	Minas Gerais	MG	Cônego Marinho	2440
2441	BR	Brasil	Minas Gerais	MG	Confins	2441
2442	BR	Brasil	Minas Gerais	MG	Congonhal	2442
2443	BR	Brasil	Minas Gerais	MG	Congonhas	2443
2444	BR	Brasil	Minas Gerais	MG	Congonhas do Norte	2444
2445	BR	Brasil	Minas Gerais	MG	Conquista	2445
2446	BR	Brasil	Minas Gerais	MG	Conselheiro Lafaiete	2446
2451	BR	Brasil	Minas Gerais	MG	Coração de Jesus	2451
2452	BR	Brasil	Minas Gerais	MG	Cordisburgo	2452
2475	BR	Brasil	Minas Gerais	MG	Curral de Dentro	2475
2495	BR	Brasil	Minas Gerais	MG	Dom Bosco	2495
3683	BR	Brasil	São Paulo	SP	Pedranópolis	3683
3684	BR	Brasil	São Paulo	SP	Pedregulho	3684
3685	BR	Brasil	São Paulo	SP	Pedreira	3685
3686	BR	Brasil	São Paulo	SP	Pedrinhas Paulista	3686
3687	BR	Brasil	São Paulo	SP	Pedro de Toledo	3687
3688	BR	Brasil	São Paulo	SP	Penápolis	3688
3689	BR	Brasil	São Paulo	SP	Pereira Barreto	3689
3690	BR	Brasil	São Paulo	SP	Pereiras	3690
3691	BR	Brasil	São Paulo	SP	Peruíbe	3691
3692	BR	Brasil	São Paulo	SP	Piacatu	3692
3693	BR	Brasil	São Paulo	SP	Piedade	3693
3694	BR	Brasil	São Paulo	SP	Pilar do Sul	3694
3703	BR	Brasil	São Paulo	SP	Pirajuí	3703
4680	BR	Brasil	Rio Grande do Sul	RS	Campos Borges	4680
4681	BR	Brasil	Rio Grande do Sul	RS	Candelária	4681
4682	BR	Brasil	Rio Grande do Sul	RS	Cândido Godói	4682
4683	BR	Brasil	Rio Grande do Sul	RS	Candiota	4683
4684	BR	Brasil	Rio Grande do Sul	RS	Canela	4684
4685	BR	Brasil	Rio Grande do Sul	RS	Canguçu	4685
5054	BR	Brasil	Rio Grande do Sul	RS	Teutônia	5054
96	BR	Brasil	Amazonas	AM	Eirunepé	96
131	BR	Brasil	Amazonas	AM	Tapauá	131
158	BR	Brasil	Pará	PA	Almeirim	158
192	BR	Brasil	Pará	PA	Cumaru do Norte	192
214	BR	Brasil	Pará	PA	Limoeiro do Ajuru	214
331	BR	Brasil	Tocantins	TO	Babaçulândia	331
335	BR	Brasil	Tocantins	TO	Bernardo Sayão	335
3704	BR	Brasil	São Paulo	SP	Pirangi	3704
3705	BR	Brasil	São Paulo	SP	Pirapora do Bom Jesus	3705
3706	BR	Brasil	São Paulo	SP	Pirapozinho	3706
3707	BR	Brasil	São Paulo	SP	Pirassununga	3707
3708	BR	Brasil	São Paulo	SP	Piratininga	3708
3709	BR	Brasil	São Paulo	SP	Pitangueiras	3709
3710	BR	Brasil	São Paulo	SP	Planalto	3710
4316	BR	Brasil	Santa Catarina	SC	Água Doce	4316
4317	BR	Brasil	Santa Catarina	SC	Águas de Chapecó	4317
4318	BR	Brasil	Santa Catarina	SC	Águas Frias	4318
4319	BR	Brasil	Santa Catarina	SC	Águas Mornas	4319
4320	BR	Brasil	Santa Catarina	SC	Alfredo Wagner	4320
4321	BR	Brasil	Santa Catarina	SC	Alto Bela Vista	4321
4322	BR	Brasil	Santa Catarina	SC	Anchieta	4322
4323	BR	Brasil	Santa Catarina	SC	Angelina	4323
4324	BR	Brasil	Santa Catarina	SC	Anita Garibaldi	4324
4325	BR	Brasil	Santa Catarina	SC	Anitápolis	4325
4332	BR	Brasil	Santa Catarina	SC	Arroio Trinta	4332
4333	BR	Brasil	Santa Catarina	SC	Arvoredo	4333
4334	BR	Brasil	Santa Catarina	SC	Ascurra	4334
4342	BR	Brasil	Santa Catarina	SC	Barra Bonita	4342
4343	BR	Brasil	Santa Catarina	SC	Barra Velha	4343
4344	BR	Brasil	Santa Catarina	SC	Bela Vista do Toldo	4344
4345	BR	Brasil	Santa Catarina	SC	Belmonte	4345
4346	BR	Brasil	Santa Catarina	SC	Benedito Novo	4346
4347	BR	Brasil	Santa Catarina	SC	Biguaçu	4347
4348	BR	Brasil	Santa Catarina	SC	Blumenau	4348
4349	BR	Brasil	Santa Catarina	SC	Bocaina do Sul	4349
4350	BR	Brasil	Santa Catarina	SC	Bombinhas	4350
4351	BR	Brasil	Santa Catarina	SC	Bom Jardim da Serra	4351
4357	BR	Brasil	Santa Catarina	SC	Braço do Trombudo	4357
4360	BR	Brasil	Santa Catarina	SC	Caçador	4360
4362	BR	Brasil	Santa Catarina	SC	Calmon	4362
4363	BR	Brasil	Santa Catarina	SC	Camboriú	4363
4364	BR	Brasil	Santa Catarina	SC	Capão Alto	4364
5056	BR	Brasil	Rio Grande do Sul	RS	Tiradentes do Sul	5056
5057	BR	Brasil	Rio Grande do Sul	RS	Toropi	5057
5058	BR	Brasil	Rio Grande do Sul	RS	Torres	5058
5062	BR	Brasil	Rio Grande do Sul	RS	Três Cachoeiras	5062
123	BR	Brasil	Amazonas	AM	Rio Preto da Eva	123
287	BR	Brasil	Pará	PA	Trairão	287
419	BR	Brasil	Tocantins	TO	Recursolândia	419
1341	BR	Brasil	Paraíba	PB	Junco do Seridó	1341
1342	BR	Brasil	Paraíba	PB	Juripiranga	1342
1343	BR	Brasil	Paraíba	PB	Juru	1343
1344	BR	Brasil	Paraíba	PB	Lagoa	1344
1345	BR	Brasil	Paraíba	PB	Lagoa de Dentro	1345
1346	BR	Brasil	Paraíba	PB	Lagoa Seca	1346
1347	BR	Brasil	Paraíba	PB	Lastro	1347
1348	BR	Brasil	Paraíba	PB	Livramento	1348
1349	BR	Brasil	Paraíba	PB	Logradouro	1349
1350	BR	Brasil	Paraíba	PB	Lucena	1350
1351	BR	Brasil	Paraíba	PB	Mãe D´água	1351
1352	BR	Brasil	Paraíba	PB	Malta	1352
1353	BR	Brasil	Paraíba	PB	Mamanguape	1353
1354	BR	Brasil	Paraíba	PB	Manaíra	1354
1355	BR	Brasil	Paraíba	PB	Marcação	1355
1356	BR	Brasil	Paraíba	PB	Mari	1356
1357	BR	Brasil	Paraíba	PB	Marizópolis	1357
1358	BR	Brasil	Paraíba	PB	Massaranduba	1358
1359	BR	Brasil	Paraíba	PB	Mataraca	1359
1360	BR	Brasil	Paraíba	PB	Matinhas	1360
1361	BR	Brasil	Paraíba	PB	Mato Grosso	1361
1362	BR	Brasil	Paraíba	PB	Maturéia	1362
1363	BR	Brasil	Paraíba	PB	Mogeiro	1363
1364	BR	Brasil	Paraíba	PB	Montadas	1364
3785	BR	Brasil	São Paulo	SP	Santa Cruz da Esperança	3785
3786	BR	Brasil	São Paulo	SP	Santa Cruz Das Palmeiras	3786
3787	BR	Brasil	São Paulo	SP	Santa Cruz do Rio Pardo	3787
3788	BR	Brasil	São Paulo	SP	Santa Ernestina	3788
3789	BR	Brasil	São Paulo	SP	Santa fé do Sul	3789
3790	BR	Brasil	São Paulo	SP	Santa Gertrudes	3790
3791	BR	Brasil	São Paulo	SP	Santa Isabel	3791
3792	BR	Brasil	São Paulo	SP	Santa Lúcia	3792
3793	BR	Brasil	São Paulo	SP	Santa Maria da Serra	3793
3794	BR	Brasil	São Paulo	SP	Santa Mercedes	3794
3795	BR	Brasil	São Paulo	SP	Santana da Ponte Pensa	3795
3796	BR	Brasil	São Paulo	SP	Santana de Parnaíba	3796
3797	BR	Brasil	São Paulo	SP	Santa Rita D´oeste	3797
3798	BR	Brasil	São Paulo	SP	Santa Rita do Passa Quatro	3798
3800	BR	Brasil	São Paulo	SP	Santa Salete	3800
3801	BR	Brasil	São Paulo	SP	Santo Anastácio	3801
3802	BR	Brasil	São Paulo	SP	Santo André	3802
3803	BR	Brasil	São Paulo	SP	Santo Antônio da Alegria	3803
3804	BR	Brasil	São Paulo	SP	Santo Antônio de Posse	3804
3806	BR	Brasil	São Paulo	SP	Santo Antônio do Jardim	3806
3807	BR	Brasil	São Paulo	SP	Santo Antônio do Pinhal	3807
4700	BR	Brasil	Rio Grande do Sul	RS	Caseiros	4700
362	BR	Brasil	Tocantins	TO	Figueirópolis	362
624	BR	Brasil	Maranhão	MA	São Domingos do Azeitão	624
3808	BR	Brasil	São Paulo	SP	Santo Expedito	3808
3809	BR	Brasil	São Paulo	SP	Santópolis do Aguapeí	3809
4394	BR	Brasil	Santa Catarina	SC	Entre Rios	4394
4396	BR	Brasil	Santa Catarina	SC	Erval Velho	4396
4397	BR	Brasil	Santa Catarina	SC	Faxinal Dos Guedes	4397
4398	BR	Brasil	Santa Catarina	SC	Flor do Sertão	4398
4399	BR	Brasil	Santa Catarina	SC	Florianópolis	4399
4400	BR	Brasil	Santa Catarina	SC	Formosa do Sul	4400
4401	BR	Brasil	Santa Catarina	SC	Forquilhinha	4401
4402	BR	Brasil	Santa Catarina	SC	Fraiburgo	4402
4403	BR	Brasil	Santa Catarina	SC	Frei Rogério	4403
4405	BR	Brasil	Santa Catarina	SC	Garopaba	4405
4407	BR	Brasil	Santa Catarina	SC	Gaspar	4407
4408	BR	Brasil	Santa Catarina	SC	Governador Celso Ramos	4408
4409	BR	Brasil	Santa Catarina	SC	Grão Pará	4409
4410	BR	Brasil	Santa Catarina	SC	Gravatal	4410
4411	BR	Brasil	Santa Catarina	SC	Guabiruba	4411
4413	BR	Brasil	Santa Catarina	SC	Guaramirim	4413
4414	BR	Brasil	Santa Catarina	SC	Guarujá do Sul	4414
4415	BR	Brasil	Santa Catarina	SC	Guatambú	4415
4416	BR	Brasil	Santa Catarina	SC	Herval D´oeste	4416
4701	BR	Brasil	Rio Grande do Sul	RS	Catuípe	4701
4702	BR	Brasil	Rio Grande do Sul	RS	Caxias do Sul	4702
4703	BR	Brasil	Rio Grande do Sul	RS	Centenário	4703
4704	BR	Brasil	Rio Grande do Sul	RS	Cerrito	4704
4705	BR	Brasil	Rio Grande do Sul	RS	Cerro Branco	4705
4706	BR	Brasil	Rio Grande do Sul	RS	Cerro Grande	4706
4707	BR	Brasil	Rio Grande do Sul	RS	Cerro Grande do Sul	4707
4708	BR	Brasil	Rio Grande do Sul	RS	Cerro Largo	4708
4709	BR	Brasil	Rio Grande do Sul	RS	Chapada	4709
4710	BR	Brasil	Rio Grande do Sul	RS	Charqueadas	4710
4711	BR	Brasil	Rio Grande do Sul	RS	Charrua	4711
4712	BR	Brasil	Rio Grande do Sul	RS	Chiapetta	4712
4713	BR	Brasil	Rio Grande do Sul	RS	Chuí	4713
4714	BR	Brasil	Rio Grande do Sul	RS	Chuvisca	4714
4715	BR	Brasil	Rio Grande do Sul	RS	Cidreira	4715
4716	BR	Brasil	Rio Grande do Sul	RS	Ciríaco	4716
4717	BR	Brasil	Rio Grande do Sul	RS	Colinas	4717
4718	BR	Brasil	Rio Grande do Sul	RS	Colorado	4718
4719	BR	Brasil	Rio Grande do Sul	RS	Condor	4719
5066	BR	Brasil	Rio Grande do Sul	RS	Três Palmeiras	5066
5090	BR	Brasil	Rio Grande do Sul	RS	Viadutos	5090
107	BR	Brasil	Amazonas	AM	Juruá	107
313	BR	Brasil	Tocantins	TO	Aguiarnópolis	313
397	BR	Brasil	Tocantins	TO	Novo Alegre	397
420	BR	Brasil	Tocantins	TO	Riachinho	420
625	BR	Brasil	Maranhão	MA	São Domingos do Maranhão	625
1250	BR	Brasil	Paraíba	PB	Alhandra	1250
1251	BR	Brasil	Paraíba	PB	São João do Rio do Peixe	1251
1252	BR	Brasil	Paraíba	PB	Amparo	1252
1253	BR	Brasil	Paraíba	PB	Aparecida	1253
1254	BR	Brasil	Paraíba	PB	Araçagi	1254
1256	BR	Brasil	Paraíba	PB	Araruna	1256
1257	BR	Brasil	Paraíba	PB	Areia	1257
1258	BR	Brasil	Paraíba	PB	Areia de Baraúnas	1258
1259	BR	Brasil	Paraíba	PB	Areial	1259
1260	BR	Brasil	Paraíba	PB	Aroeiras	1260
1261	BR	Brasil	Paraíba	PB	Assunção	1261
1262	BR	Brasil	Paraíba	PB	Baía da Traição	1262
1263	BR	Brasil	Paraíba	PB	Bananeiras	1263
1264	BR	Brasil	Paraíba	PB	Baraúna	1264
1265	BR	Brasil	Paraíba	PB	Barra de Santana	1265
1266	BR	Brasil	Paraíba	PB	Barra de Santa Rosa	1266
1267	BR	Brasil	Paraíba	PB	Barra de São Miguel	1267
1268	BR	Brasil	Paraíba	PB	Bayeux	1268
1269	BR	Brasil	Paraíba	PB	Belém	1269
1270	BR	Brasil	Paraíba	PB	Belém do Brejo do Cruz	1270
1271	BR	Brasil	Paraíba	PB	Bernardino Batista	1271
1272	BR	Brasil	Paraíba	PB	Boa Ventura	1272
1273	BR	Brasil	Paraíba	PB	Boa Vista	1273
1274	BR	Brasil	Paraíba	PB	Bom Jesus	1274
1275	BR	Brasil	Paraíba	PB	Bom Sucesso	1275
1276	BR	Brasil	Paraíba	PB	Bonito de Santa fé	1276
1277	BR	Brasil	Paraíba	PB	Boqueirão	1277
1278	BR	Brasil	Paraíba	PB	Igaracy	1278
1279	BR	Brasil	Paraíba	PB	Borborema	1279
1280	BR	Brasil	Paraíba	PB	Brejo do Cruz	1280
1281	BR	Brasil	Paraíba	PB	Brejo Dos Santos	1281
1282	BR	Brasil	Paraíba	PB	Caaporã	1282
4213	BR	Brasil	Paraná	PR	Reserva	4213
4417	BR	Brasil	Santa Catarina	SC	Ibiam	4417
4729	BR	Brasil	Rio Grande do Sul	RS	Cristal	4729
4730	BR	Brasil	Rio Grande do Sul	RS	Cristal do Sul	4730
4731	BR	Brasil	Rio Grande do Sul	RS	Cruz Alta	4731
4733	BR	Brasil	Rio Grande do Sul	RS	Cruzeiro do Sul	4733
4734	BR	Brasil	Rio Grande do Sul	RS	David Canabarro	4734
5067	BR	Brasil	Rio Grande do Sul	RS	Três Passos	5067
5068	BR	Brasil	Rio Grande do Sul	RS	Trindade do Sul	5068
5088	BR	Brasil	Rio Grande do Sul	RS	Veranópolis	5088
5089	BR	Brasil	Rio Grande do Sul	RS	Vespasiano Correa	5089
288	BR	Brasil	Pará	PA	Tucumã	288
1377	BR	Brasil	Paraíba	PB	Passagem	1377
3979	BR	Brasil	Paraná	PR	Carambeí	3979
3980	BR	Brasil	Paraná	PR	Carlópolis	3980
4270	BR	Brasil	Paraná	PR	São Tomé	4270
4271	BR	Brasil	Paraná	PR	Sapopema	4271
4272	BR	Brasil	Paraná	PR	Sarandi	4272
4273	BR	Brasil	Paraná	PR	Saudade do Iguaçu	4273
4278	BR	Brasil	Paraná	PR	Siqueira Campos	4278
4280	BR	Brasil	Paraná	PR	Tamarana	4280
4281	BR	Brasil	Paraná	PR	Tamboara	4281
4290	BR	Brasil	Paraná	PR	Tijucas do Sul	4290
4291	BR	Brasil	Paraná	PR	Toledo	4291
4292	BR	Brasil	Paraná	PR	Tomazina	4292
4293	BR	Brasil	Paraná	PR	Três Barras do Paraná	4293
4294	BR	Brasil	Paraná	PR	Tunas do Paraná	4294
4295	BR	Brasil	Paraná	PR	Tuneiras do Oeste	4295
4296	BR	Brasil	Paraná	PR	Tupãssi	4296
4299	BR	Brasil	Paraná	PR	Umuarama	4299
4300	BR	Brasil	Paraná	PR	União da Vitória	4300
4301	BR	Brasil	Paraná	PR	Uniflor	4301
4303	BR	Brasil	Paraná	PR	Wenceslau Braz	4303
4304	BR	Brasil	Paraná	PR	Ventania	4304
4305	BR	Brasil	Paraná	PR	Vera Cruz do Oeste	4305
4306	BR	Brasil	Paraná	PR	Verê	4306
4307	BR	Brasil	Paraná	PR	Vila Alta	4307
4308	BR	Brasil	Paraná	PR	Doutor Ulysses	4308
4310	BR	Brasil	Paraná	PR	Vitorino	4310
4311	BR	Brasil	Paraná	PR	Xambrê	4311
4312	BR	Brasil	Santa Catarina	SC	Abdon Batista	4312
4313	BR	Brasil	Santa Catarina	SC	Abelardo Luz	4313
4314	BR	Brasil	Santa Catarina	SC	Agrolândia	4314
4384	BR	Brasil	Santa Catarina	SC	Corupá	4384
5019	BR	Brasil	Rio Grande do Sul	RS	São Sepé	5019
398	BR	Brasil	Tocantins	TO	Novo Jardim	398
406	BR	Brasil	Tocantins	TO	Peixe	406
421	BR	Brasil	Tocantins	TO	Rio da Conceição	421
898	BR	Brasil	Ceará	CE	Altaneira	898
899	BR	Brasil	Ceará	CE	Alto Santo	899
3811	BR	Brasil	São Paulo	SP	São Bento do Sapucaí	3811
4070	BR	Brasil	Paraná	PR	Itambé	4070
4071	BR	Brasil	Paraná	PR	Itapejara D´oeste	4071
4072	BR	Brasil	Paraná	PR	Itaperuçu	4072
4073	BR	Brasil	Paraná	PR	Itaúna do Sul	4073
4074	BR	Brasil	Paraná	PR	Ivaí	4074
4075	BR	Brasil	Paraná	PR	Ivaiporã	4075
4076	BR	Brasil	Paraná	PR	Ivaté	4076
4078	BR	Brasil	Paraná	PR	Jaboti	4078
4079	BR	Brasil	Paraná	PR	Jacarezinho	4079
4080	BR	Brasil	Paraná	PR	Jaguapitã	4080
4081	BR	Brasil	Paraná	PR	Jaguariaíva	4081
4082	BR	Brasil	Paraná	PR	Jandaia do Sul	4082
4083	BR	Brasil	Paraná	PR	Janiópolis	4083
4084	BR	Brasil	Paraná	PR	Japira	4084
4085	BR	Brasil	Paraná	PR	Japurá	4085
4086	BR	Brasil	Paraná	PR	Jardim Alegre	4086
4087	BR	Brasil	Paraná	PR	Jardim Olinda	4087
4088	BR	Brasil	Paraná	PR	Jataizinho	4088
4089	BR	Brasil	Paraná	PR	Jesuítas	4089
4090	BR	Brasil	Paraná	PR	Joaquim Távora	4090
4091	BR	Brasil	Paraná	PR	Jundiaí do Sul	4091
4092	BR	Brasil	Paraná	PR	Juranda	4092
4093	BR	Brasil	Paraná	PR	Jussara	4093
4094	BR	Brasil	Paraná	PR	Kaloré	4094
4096	BR	Brasil	Paraná	PR	Laranjal	4096
4097	BR	Brasil	Paraná	PR	Laranjeiras do Sul	4097
4098	BR	Brasil	Paraná	PR	Leópolis	4098
4099	BR	Brasil	Paraná	PR	Lidianópolis	4099
4100	BR	Brasil	Paraná	PR	Lindoeste	4100
4103	BR	Brasil	Paraná	PR	Londrina	4103
4118	BR	Brasil	Paraná	PR	Marilândia do Sul	4118
4119	BR	Brasil	Paraná	PR	Marilena	4119
4120	BR	Brasil	Paraná	PR	Mariluz	4120
4121	BR	Brasil	Paraná	PR	Maringá	4121
4122	BR	Brasil	Paraná	PR	Mariópolis	4122
4123	BR	Brasil	Paraná	PR	Maripá	4123
4124	BR	Brasil	Paraná	PR	Marmeleiro	4124
4125	BR	Brasil	Paraná	PR	Marquinho	4125
4126	BR	Brasil	Paraná	PR	Marumbi	4126
4127	BR	Brasil	Paraná	PR	Matelândia	4127
4128	BR	Brasil	Paraná	PR	Matinhos	4128
4130	BR	Brasil	Paraná	PR	Mauá da Serra	4130
4132	BR	Brasil	Paraná	PR	Mercedes	4132
4133	BR	Brasil	Paraná	PR	Mirador	4133
80	BR	Brasil	Amazonas	AM	Atalaia do Norte	80
232	BR	Brasil	Pará	PA	Novo Repartimento	232
248	BR	Brasil	Pará	PA	Porto de Moz	248
276	BR	Brasil	Pará	PA	São João do Araguaia	276
317	BR	Brasil	Tocantins	TO	Ananás	317
1766	BR	Brasil	Sergipe	SE	Carmópolis	1766
3540	BR	Brasil	São Paulo	SP	Itu	3540
3812	BR	Brasil	São Paulo	SP	São Bernardo do Campo	3812
3813	BR	Brasil	São Paulo	SP	São Caetano do Sul	3813
3835	BR	Brasil	São Paulo	SP	São Sebastião da Grama	3835
3839	BR	Brasil	São Paulo	SP	Sarutaiá	3839
3844	BR	Brasil	São Paulo	SP	Sertãozinho	3844
3848	BR	Brasil	São Paulo	SP	Socorro	3848
3849	BR	Brasil	São Paulo	SP	Sorocaba	3849
3850	BR	Brasil	São Paulo	SP	Sud Mennucci	3850
3857	BR	Brasil	São Paulo	SP	Taciba	3857
3858	BR	Brasil	São Paulo	SP	Taguaí	3858
3859	BR	Brasil	São Paulo	SP	Taiaçu	3859
3860	BR	Brasil	São Paulo	SP	Taiúva	3860
3861	BR	Brasil	São Paulo	SP	Tambaú	3861
3862	BR	Brasil	São Paulo	SP	Tanabi	3862
3863	BR	Brasil	São Paulo	SP	Tapiraí	3863
3864	BR	Brasil	São Paulo	SP	Tapiratiba	3864
3865	BR	Brasil	São Paulo	SP	Taquaral	3865
3866	BR	Brasil	São Paulo	SP	Taquaritinga	3866
3867	BR	Brasil	São Paulo	SP	Taquarituba	3867
3879	BR	Brasil	São Paulo	SP	Torrinha	3879
3880	BR	Brasil	São Paulo	SP	Trabiju	3880
3881	BR	Brasil	São Paulo	SP	Tremembé	3881
3882	BR	Brasil	São Paulo	SP	Três Fronteiras	3882
4140	BR	Brasil	Paraná	PR	Nova Aliança do Ivaí	4140
4141	BR	Brasil	Paraná	PR	Nova América da Colina	4141
4142	BR	Brasil	Paraná	PR	Nova Aurora	4142
4143	BR	Brasil	Paraná	PR	Nova Cantu	4143
4144	BR	Brasil	Paraná	PR	Nova Esperança	4144
4163	BR	Brasil	Paraná	PR	Paraíso do Norte	4163
4164	BR	Brasil	Paraná	PR	Paranacity	4164
4165	BR	Brasil	Paraná	PR	Paranaguá	4165
4166	BR	Brasil	Paraná	PR	Paranapoema	4166
4174	BR	Brasil	Paraná	PR	Pérola	4174
4175	BR	Brasil	Paraná	PR	Pérola D´oeste	4175
4176	BR	Brasil	Paraná	PR	Piên	4176
4177	BR	Brasil	Paraná	PR	Pinhais	4177
4855	BR	Brasil	Rio Grande do Sul	RS	Mata	4855
5111	BR	Brasil	Mato Grosso do Sul	MS	Aparecida do Taboado	5111
5112	BR	Brasil	Mato Grosso do Sul	MS	Aquidauana	5112
5113	BR	Brasil	Mato Grosso do Sul	MS	Aral Moreira	5113
5148	BR	Brasil	Mato Grosso do Sul	MS	Jardim	5148
159	BR	Brasil	Pará	PA	Altamira	159
233	BR	Brasil	Pará	PA	Óbidos	233
289	BR	Brasil	Pará	PA	Tucuruí	289
295	BR	Brasil	Pará	PA	Xinguara	295
318	BR	Brasil	Tocantins	TO	Angico	318
338	BR	Brasil	Tocantins	TO	Brejinho de Nazaré	338
900	BR	Brasil	Ceará	CE	Amontada	900
3586	BR	Brasil	São Paulo	SP	Magda	3586
3589	BR	Brasil	São Paulo	SP	Manduri	3589
3610	BR	Brasil	São Paulo	SP	Mococa	3610
3611	BR	Brasil	São Paulo	SP	Moji Das Cruzes	3611
3612	BR	Brasil	São Paulo	SP	Mogi Guaçu	3612
3628	BR	Brasil	São Paulo	SP	Nantes	3628
3634	BR	Brasil	São Paulo	SP	Nipoã	3634
3635	BR	Brasil	São Paulo	SP	Nova Aliança	3635
3636	BR	Brasil	São Paulo	SP	Nova Campina	3636
3637	BR	Brasil	São Paulo	SP	Nova Canaã Paulista	3637
3638	BR	Brasil	São Paulo	SP	Nova Castilho	3638
3639	BR	Brasil	São Paulo	SP	Nova Europa	3639
3640	BR	Brasil	São Paulo	SP	Nova Granada	3640
3641	BR	Brasil	São Paulo	SP	Nova Guataporanga	3641
3642	BR	Brasil	São Paulo	SP	Nova Independência	3642
3643	BR	Brasil	São Paulo	SP	Novais	3643
3644	BR	Brasil	São Paulo	SP	Nova Luzitânia	3644
3646	BR	Brasil	São Paulo	SP	Novo Horizonte	3646
3647	BR	Brasil	São Paulo	SP	Nuporanga	3647
3648	BR	Brasil	São Paulo	SP	Ocauçu	3648
3649	BR	Brasil	São Paulo	SP	Óleo	3649
3650	BR	Brasil	São Paulo	SP	Olímpia	3650
3651	BR	Brasil	São Paulo	SP	Onda Verde	3651
3652	BR	Brasil	São Paulo	SP	Oriente	3652
3677	BR	Brasil	São Paulo	SP	Paulicéia	3677
3678	BR	Brasil	São Paulo	SP	Paulínia	3678
3679	BR	Brasil	São Paulo	SP	Paulistânia	3679
3680	BR	Brasil	São Paulo	SP	Paulo de Faria	3680
3681	BR	Brasil	São Paulo	SP	Pederneiras	3681
3682	BR	Brasil	São Paulo	SP	Pedra Bela	3682
3711	BR	Brasil	São Paulo	SP	Platina	3711
907	BR	Brasil	Ceará	CE	Araripe	907
5047	BR	Brasil	Rio Grande do Sul	RS	Tapes	5047
161	BR	Brasil	Pará	PA	Ananindeua	161
162	BR	Brasil	Pará	PA	Anapu	162
249	BR	Brasil	Pará	PA	Prainha	249
273	BR	Brasil	Pará	PA	São Geraldo do Araguaia	273
400	BR	Brasil	Tocantins	TO	Palmeirante	400
2001	BR	Brasil	Bahia	BA	Irecê	2001
3716	BR	Brasil	São Paulo	SP	Pontal	3716
3717	BR	Brasil	São Paulo	SP	Pontalinda	3717
3718	BR	Brasil	São Paulo	SP	Pontes Gestal	3718
3719	BR	Brasil	São Paulo	SP	Populina	3719
3720	BR	Brasil	São Paulo	SP	Porangaba	3720
3721	BR	Brasil	São Paulo	SP	Porto Feliz	3721
3722	BR	Brasil	São Paulo	SP	Porto Ferreira	3722
3723	BR	Brasil	São Paulo	SP	Potim	3723
3724	BR	Brasil	São Paulo	SP	Potirendaba	3724
3725	BR	Brasil	São Paulo	SP	Pracinha	3725
3726	BR	Brasil	São Paulo	SP	Pradópolis	3726
3727	BR	Brasil	São Paulo	SP	Praia Grande	3727
3728	BR	Brasil	São Paulo	SP	Pratânia	3728
3729	BR	Brasil	São Paulo	SP	Presidente Alves	3729
3730	BR	Brasil	São Paulo	SP	Presidente Bernardes	3730
3731	BR	Brasil	São Paulo	SP	Presidente Epitácio	3731
3732	BR	Brasil	São Paulo	SP	Presidente Prudente	3732
3733	BR	Brasil	São Paulo	SP	Presidente Venceslau	3733
3734	BR	Brasil	São Paulo	SP	Promissão	3734
3735	BR	Brasil	São Paulo	SP	Quadra	3735
3736	BR	Brasil	São Paulo	SP	Quatá	3736
3737	BR	Brasil	São Paulo	SP	Queiroz	3737
3738	BR	Brasil	São Paulo	SP	Queluz	3738
3805	BR	Brasil	São Paulo	SP	Santo Antônio do Aracanguá	3805
3810	BR	Brasil	São Paulo	SP	Santos	3810
3824	BR	Brasil	São Paulo	SP	São José do Rio Preto	3824
3826	BR	Brasil	São Paulo	SP	São Lourenço da Serra	3826
3827	BR	Brasil	São Paulo	SP	São Luís do Paraitinga	3827
3828	BR	Brasil	São Paulo	SP	São Manuel	3828
3829	BR	Brasil	São Paulo	SP	São Miguel Arcanjo	3829
3830	BR	Brasil	São Paulo	SP	São Paulo	3830
3831	BR	Brasil	São Paulo	SP	São Pedro	3831
3832	BR	Brasil	São Paulo	SP	São Pedro do Turvo	3832
3833	BR	Brasil	São Paulo	SP	São Roque	3833
3834	BR	Brasil	São Paulo	SP	São Sebastião	3834
251	BR	Brasil	Pará	PA	Quatipuru	251
319	BR	Brasil	Tocantins	TO	Aparecida do Rio Negro	319
363	BR	Brasil	Tocantins	TO	Filadélfia	363
414	BR	Brasil	Tocantins	TO	Porto Alegre do Tocantins	414
1762	BR	Brasil	Sergipe	SE	Canhoba	1762
1763	BR	Brasil	Sergipe	SE	Canindé de São Francisco	1763
1764	BR	Brasil	Sergipe	SE	Capela	1764
1765	BR	Brasil	Sergipe	SE	Carira	1765
1767	BR	Brasil	Sergipe	SE	Cedro de São João	1767
1768	BR	Brasil	Sergipe	SE	Cristinápolis	1768
1769	BR	Brasil	Sergipe	SE	Cumbe	1769
1770	BR	Brasil	Sergipe	SE	Divina Pastora	1770
1799	BR	Brasil	Sergipe	SE	Nossa Senhora do Socorro	1799
1800	BR	Brasil	Sergipe	SE	Pacatuba	1800
1801	BR	Brasil	Sergipe	SE	Pedra Mole	1801
1802	BR	Brasil	Sergipe	SE	Pedrinhas	1802
1803	BR	Brasil	Sergipe	SE	Pinhão	1803
1858	BR	Brasil	Bahia	BA	Baianópolis	1858
1859	BR	Brasil	Bahia	BA	Baixa Grande	1859
1860	BR	Brasil	Bahia	BA	Banzaê	1860
1865	BR	Brasil	Bahia	BA	Barra do Rocha	1865
1866	BR	Brasil	Bahia	BA	Barreiras	1866
1867	BR	Brasil	Bahia	BA	Barro Alto	1867
2129	BR	Brasil	Bahia	BA	Pintadas	2129
2130	BR	Brasil	Bahia	BA	Piraí do Norte	2130
2131	BR	Brasil	Bahia	BA	Piripá	2131
2132	BR	Brasil	Bahia	BA	Piritiba	2132
2133	BR	Brasil	Bahia	BA	Planaltino	2133
2134	BR	Brasil	Bahia	BA	Planalto	2134
2135	BR	Brasil	Bahia	BA	Poções	2135
2136	BR	Brasil	Bahia	BA	Pojuca	2136
2137	BR	Brasil	Bahia	BA	Ponto Novo	2137
2138	BR	Brasil	Bahia	BA	Porto Seguro	2138
2139	BR	Brasil	Bahia	BA	Potiraguá	2139
2140	BR	Brasil	Bahia	BA	Prado	2140
2141	BR	Brasil	Bahia	BA	Presidente Dutra	2141
2142	BR	Brasil	Bahia	BA	Presidente Jânio Quadros	2142
2143	BR	Brasil	Bahia	BA	Presidente Tancredo Neves	2143
2144	BR	Brasil	Bahia	BA	Queimadas	2144
2145	BR	Brasil	Bahia	BA	Quijingue	2145
2162	BR	Brasil	Bahia	BA	Salinas da Margarida	2162
2163	BR	Brasil	Bahia	BA	Salvador	2163
2165	BR	Brasil	Bahia	BA	Santa Brígida	2165
2166	BR	Brasil	Bahia	BA	Santa Cruz Cabrália	2166
2168	BR	Brasil	Bahia	BA	Santa Inês	2168
74	BR	Brasil	Acre	AC	Porto Acre	74
252	BR	Brasil	Pará	PA	Redenção	252
320	BR	Brasil	Tocantins	TO	Aragominas	320
326	BR	Brasil	Tocantins	TO	Arapoema	326
336	BR	Brasil	Tocantins	TO	Bom Jesus do Tocantins	336
346	BR	Brasil	Tocantins	TO	Centenário	346
367	BR	Brasil	Tocantins	TO	Goiatins	367
377	BR	Brasil	Tocantins	TO	Lagoa da Confusão	377
626	BR	Brasil	Maranhão	MA	São Félix de Balsas	626
627	BR	Brasil	Maranhão	MA	São Francisco do Brejão	627
665	BR	Brasil	Maranhão	MA	Vitória do Mearim	665
666	BR	Brasil	Maranhão	MA	Vitorino Freire	666
902	BR	Brasil	Ceará	CE	Apuiarés	902
903	BR	Brasil	Ceará	CE	Aquiraz	903
904	BR	Brasil	Ceará	CE	Aracati	904
905	BR	Brasil	Ceará	CE	Aracoiaba	905
906	BR	Brasil	Ceará	CE	Ararendá	906
908	BR	Brasil	Ceará	CE	Aratuba	908
909	BR	Brasil	Ceará	CE	Arneiroz	909
1868	BR	Brasil	Bahia	BA	Barrocas	1868
1869	BR	Brasil	Bahia	BA	Governador Lomanto Júnior	1869
1870	BR	Brasil	Bahia	BA	Belmonte	1870
1871	BR	Brasil	Bahia	BA	Belo Campo	1871
1872	BR	Brasil	Bahia	BA	Biritinga	1872
1873	BR	Brasil	Bahia	BA	Boa Nova	1873
1874	BR	Brasil	Bahia	BA	Boa Vista do Tupim	1874
1875	BR	Brasil	Bahia	BA	Bom Jesus da Lapa	1875
1876	BR	Brasil	Bahia	BA	Bom Jesus da Serra	1876
1877	BR	Brasil	Bahia	BA	Boninal	1877
1878	BR	Brasil	Bahia	BA	Bonito	1878
1879	BR	Brasil	Bahia	BA	Boquira	1879
1880	BR	Brasil	Bahia	BA	Botuporã	1880
1881	BR	Brasil	Bahia	BA	Brejões	1881
1882	BR	Brasil	Bahia	BA	Brejolândia	1882
1883	BR	Brasil	Bahia	BA	Brotas de Macaúbas	1883
1884	BR	Brasil	Bahia	BA	Brumado	1884
1885	BR	Brasil	Bahia	BA	Buerarema	1885
1886	BR	Brasil	Bahia	BA	Buritirama	1886
1887	BR	Brasil	Bahia	BA	Caatiba	1887
1890	BR	Brasil	Bahia	BA	Caculé	1890
4453	BR	Brasil	Santa Catarina	SC	Laguna	4453
4454	BR	Brasil	Santa Catarina	SC	Lajeado Grande	4454
4624	BR	Brasil	Rio Grande do Sul	RS	Arambaré	4624
97	BR	Brasil	Amazonas	AM	Envira	97
98	BR	Brasil	Amazonas	AM	Fonte Boa	98
225	BR	Brasil	Pará	PA	Mojuí dos Campos	225
234	BR	Brasil	Pará	PA	Oeiras do Pará	234
1087	BR	Brasil	Rio Grande do Norte	RN	Arês	1087
1088	BR	Brasil	Rio Grande do Norte	RN	Augusto Severo	1088
1089	BR	Brasil	Rio Grande do Norte	RN	Baía Formosa	1089
1090	BR	Brasil	Rio Grande do Norte	RN	Baraúna	1090
1091	BR	Brasil	Rio Grande do Norte	RN	Barcelona	1091
1092	BR	Brasil	Rio Grande do Norte	RN	Bento Fernandes	1092
1093	BR	Brasil	Rio Grande do Norte	RN	Bodó	1093
1094	BR	Brasil	Rio Grande do Norte	RN	Bom Jesus	1094
1095	BR	Brasil	Rio Grande do Norte	RN	Brejinho	1095
1107	BR	Brasil	Rio Grande do Norte	RN	Coronel João Pessoa	1107
1109	BR	Brasil	Rio Grande do Norte	RN	Currais Novos	1109
1110	BR	Brasil	Rio Grande do Norte	RN	Doutor Severiano	1110
1111	BR	Brasil	Rio Grande do Norte	RN	Parnamirim	1111
1112	BR	Brasil	Rio Grande do Norte	RN	Encanto	1112
1113	BR	Brasil	Rio Grande do Norte	RN	Equador	1113
1114	BR	Brasil	Rio Grande do Norte	RN	Espírito Santo	1114
1115	BR	Brasil	Rio Grande do Norte	RN	Extremoz	1115
1116	BR	Brasil	Rio Grande do Norte	RN	Felipe Guerra	1116
1121	BR	Brasil	Rio Grande do Norte	RN	Galinhos	1121
1122	BR	Brasil	Rio Grande do Norte	RN	Goianinha	1122
1123	BR	Brasil	Rio Grande do Norte	RN	Governador Dix-sept Rosado	1123
1124	BR	Brasil	Rio Grande do Norte	RN	Grossos	1124
1125	BR	Brasil	Rio Grande do Norte	RN	Guamaré	1125
1126	BR	Brasil	Rio Grande do Norte	RN	Ielmo Marinho	1126
1132	BR	Brasil	Rio Grande do Norte	RN	Jandaíra	1132
1133	BR	Brasil	Rio Grande do Norte	RN	Janduís	1133
1134	BR	Brasil	Rio Grande do Norte	RN	Januário Cicco	1134
1135	BR	Brasil	Rio Grande do Norte	RN	Japi	1135
1136	BR	Brasil	Rio Grande do Norte	RN	Jardim de Angicos	1136
1137	BR	Brasil	Rio Grande do Norte	RN	Jardim de Piranhas	1137
1138	BR	Brasil	Rio Grande do Norte	RN	Jardim do Seridó	1138
1139	BR	Brasil	Rio Grande do Norte	RN	João Câmara	1139
1141	BR	Brasil	Rio Grande do Norte	RN	José da Penha	1141
1142	BR	Brasil	Rio Grande do Norte	RN	Jucurutu	1142
1143	BR	Brasil	Rio Grande do Norte	RN	Jundiá	1143
1144	BR	Brasil	Rio Grande do Norte	RN	Lagoa D´anta	1144
1145	BR	Brasil	Rio Grande do Norte	RN	Lagoa de Pedras	1145
1146	BR	Brasil	Rio Grande do Norte	RN	Lagoa de Velhos	1146
1147	BR	Brasil	Rio Grande do Norte	RN	Lagoa Nova	1147
1148	BR	Brasil	Rio Grande do Norte	RN	Lagoa Salgada	1148
1152	BR	Brasil	Rio Grande do Norte	RN	Luís Gomes	1152
36	BR	Brasil	Rondônia	RO	Governador Jorge Teixeira	36
277	BR	Brasil	Pará	PA	São Miguel do Guamá	277
422	BR	Brasil	Tocantins	TO	Rio Dos Bois	422
508	BR	Brasil	Maranhão	MA	Cidelândia	508
509	BR	Brasil	Maranhão	MA	Codó	509
510	BR	Brasil	Maranhão	MA	Coelho Neto	510
511	BR	Brasil	Maranhão	MA	Colinas	511
512	BR	Brasil	Maranhão	MA	Conceição do Lago-açu	512
513	BR	Brasil	Maranhão	MA	Coroatá	513
514	BR	Brasil	Maranhão	MA	Cururupu	514
515	BR	Brasil	Maranhão	MA	Davinópolis	515
516	BR	Brasil	Maranhão	MA	Dom Pedro	516
517	BR	Brasil	Maranhão	MA	Duque Bacelar	517
518	BR	Brasil	Maranhão	MA	Esperantinópolis	518
520	BR	Brasil	Maranhão	MA	Feira Nova do Maranhão	520
521	BR	Brasil	Maranhão	MA	Fernando Falcão	521
522	BR	Brasil	Maranhão	MA	Formosa da Serra Negra	522
523	BR	Brasil	Maranhão	MA	Fortaleza Dos Nogueiras	523
525	BR	Brasil	Maranhão	MA	Godofredo Viana	525
532	BR	Brasil	Maranhão	MA	Governador Nunes Freire	532
533	BR	Brasil	Maranhão	MA	Graça Aranha	533
536	BR	Brasil	Maranhão	MA	Humberto de Campos	536
538	BR	Brasil	Maranhão	MA	Igarapé do Meio	538
539	BR	Brasil	Maranhão	MA	Igarapé Grande	539
540	BR	Brasil	Maranhão	MA	Imperatriz	540
541	BR	Brasil	Maranhão	MA	Itaipava do Grajaú	541
542	BR	Brasil	Maranhão	MA	Itapecuru Mirim	542
543	BR	Brasil	Maranhão	MA	Itinga do Maranhão	543
544	BR	Brasil	Maranhão	MA	Jatobá	544
546	BR	Brasil	Maranhão	MA	João Lisboa	546
547	BR	Brasil	Maranhão	MA	Joselândia	547
548	BR	Brasil	Maranhão	MA	Junco do Maranhão	548
549	BR	Brasil	Maranhão	MA	Lago da Pedra	549
550	BR	Brasil	Maranhão	MA	Lago do Junco	550
551	BR	Brasil	Maranhão	MA	Lago Verde	551
552	BR	Brasil	Maranhão	MA	Lagoa do Mato	552
553	BR	Brasil	Maranhão	MA	Lago Dos Rodrigues	553
554	BR	Brasil	Maranhão	MA	Lagoa Grande do Maranhão	554
555	BR	Brasil	Maranhão	MA	Lajeado Novo	555
556	BR	Brasil	Maranhão	MA	Lima Campos	556
557	BR	Brasil	Maranhão	MA	Loreto	557
558	BR	Brasil	Maranhão	MA	Luís Domingues	558
3814	BR	Brasil	São Paulo	SP	São Carlos	3814
163	BR	Brasil	Pará	PA	Augusto Corrêa	163
164	BR	Brasil	Pará	PA	Aurora do Pará	164
351	BR	Brasil	Tocantins	TO	Conceição do Tocantins	351
415	BR	Brasil	Tocantins	TO	Porto Nacional	415
423	BR	Brasil	Tocantins	TO	Rio Sono	423
490	BR	Brasil	Maranhão	MA	Buriti Bravo	490
1165	BR	Brasil	Rio Grande do Norte	RN	Nísia Floresta	1165
1166	BR	Brasil	Rio Grande do Norte	RN	Nova Cruz	1166
1167	BR	Brasil	Rio Grande do Norte	RN	Olho-d´água do Borges	1167
1168	BR	Brasil	Rio Grande do Norte	RN	Ouro Branco	1168
1169	BR	Brasil	Rio Grande do Norte	RN	Paraná	1169
1255	BR	Brasil	Paraíba	PB	Arara	1255
1939	BR	Brasil	Bahia	BA	Correntina	1939
1940	BR	Brasil	Bahia	BA	Cotegipe	1940
1941	BR	Brasil	Bahia	BA	Cravolândia	1941
1942	BR	Brasil	Bahia	BA	Crisópolis	1942
1943	BR	Brasil	Bahia	BA	Cristópolis	1943
1944	BR	Brasil	Bahia	BA	Cruz Das Almas	1944
1945	BR	Brasil	Bahia	BA	Curaçá	1945
1946	BR	Brasil	Bahia	BA	Dário Meira	1946
1947	BR	Brasil	Bahia	BA	Dias D´ávila	1947
1948	BR	Brasil	Bahia	BA	Dom Basílio	1948
1949	BR	Brasil	Bahia	BA	Dom Macedo Costa	1949
1951	BR	Brasil	Bahia	BA	Encruzilhada	1951
1952	BR	Brasil	Bahia	BA	Entre Rios	1952
3868	BR	Brasil	São Paulo	SP	Taquarivaí	3868
3869	BR	Brasil	São Paulo	SP	Tarabai	3869
3898	BR	Brasil	São Paulo	SP	Valparaíso	3898
3899	BR	Brasil	São Paulo	SP	Vargem	3899
3900	BR	Brasil	São Paulo	SP	Vargem Grande do Sul	3900
3901	BR	Brasil	São Paulo	SP	Vargem Grande Paulista	3901
3902	BR	Brasil	São Paulo	SP	Várzea Paulista	3902
3903	BR	Brasil	São Paulo	SP	Vera Cruz	3903
3904	BR	Brasil	São Paulo	SP	Vinhedo	3904
3905	BR	Brasil	São Paulo	SP	Viradouro	3905
3906	BR	Brasil	São Paulo	SP	Vista Alegre do Alto	3906
3907	BR	Brasil	São Paulo	SP	Vitória Brasil	3907
3933	BR	Brasil	Paraná	PR	Araruna	3933
3934	BR	Brasil	Paraná	PR	Araucária	3934
3935	BR	Brasil	Paraná	PR	Ariranha do Ivaí	3935
3936	BR	Brasil	Paraná	PR	Assaí	3936
3937	BR	Brasil	Paraná	PR	Assis Chateaubriand	3937
3938	BR	Brasil	Paraná	PR	Astorga	3938
3939	BR	Brasil	Paraná	PR	Atalaia	3939
3940	BR	Brasil	Paraná	PR	Balsa Nova	3940
3941	BR	Brasil	Paraná	PR	Bandeirantes	3941
3942	BR	Brasil	Paraná	PR	Barbosa Ferraz	3942
3943	BR	Brasil	Paraná	PR	Barracão	3943
3944	BR	Brasil	Paraná	PR	Barra do Jacaré	3944
37	BR	Brasil	Rondônia	RO	Itapuã do Oeste	37
215	BR	Brasil	Pará	PA	Mãe do Rio	215
301	BR	Brasil	Amapá	AP	Ferreira Gomes	301
389	BR	Brasil	Tocantins	TO	Monte Santo do Tocantins	389
1329	BR	Brasil	Paraíba	PB	Ibiara	1329
1330	BR	Brasil	Paraíba	PB	Imaculada	1330
1331	BR	Brasil	Paraíba	PB	Ingá	1331
1332	BR	Brasil	Paraíba	PB	Itabaiana	1332
1333	BR	Brasil	Paraíba	PB	Itaporanga	1333
2200	BR	Brasil	Bahia	BA	Serra Dourada	2200
2201	BR	Brasil	Bahia	BA	Serra Preta	2201
2202	BR	Brasil	Bahia	BA	Serrinha	2202
2240	BR	Brasil	Bahia	BA	Vitória da Conquista	2240
2241	BR	Brasil	Bahia	BA	Wagner	2241
2242	BR	Brasil	Bahia	BA	Wanderley	2242
2243	BR	Brasil	Bahia	BA	Wenceslau Guimarães	2243
2244	BR	Brasil	Bahia	BA	Xique-xique	2244
2245	BR	Brasil	Minas Gerais	MG	Abadia Dos Dourados	2245
3947	BR	Brasil	Paraná	PR	Bituruna	3947
3948	BR	Brasil	Paraná	PR	Boa Esperança	3948
3949	BR	Brasil	Paraná	PR	Boa Esperança do Iguaçu	3949
3950	BR	Brasil	Paraná	PR	Boa Ventura de São Roque	3950
3951	BR	Brasil	Paraná	PR	Boa Vista da Aparecida	3951
3952	BR	Brasil	Paraná	PR	Bocaiúva do Sul	3952
3953	BR	Brasil	Paraná	PR	Bom Jesus do Sul	3953
3954	BR	Brasil	Paraná	PR	Bom Sucesso	3954
3955	BR	Brasil	Paraná	PR	Bom Sucesso do Sul	3955
3956	BR	Brasil	Paraná	PR	Borrazópolis	3956
3957	BR	Brasil	Paraná	PR	Braganey	3957
3958	BR	Brasil	Paraná	PR	Brasilândia do Sul	3958
4145	BR	Brasil	Paraná	PR	Nova Esperança do Sudoeste	4145
4146	BR	Brasil	Paraná	PR	Nova Fátima	4146
4147	BR	Brasil	Paraná	PR	Nova Laranjeiras	4147
4148	BR	Brasil	Paraná	PR	Nova Londrina	4148
4149	BR	Brasil	Paraná	PR	Nova Olímpia	4149
4150	BR	Brasil	Paraná	PR	Nova Santa Bárbara	4150
4151	BR	Brasil	Paraná	PR	Nova Santa Rosa	4151
4152	BR	Brasil	Paraná	PR	Nova Prata do Iguaçu	4152
4153	BR	Brasil	Paraná	PR	Nova Tebas	4153
4154	BR	Brasil	Paraná	PR	Novo Itacolomi	4154
4155	BR	Brasil	Paraná	PR	Ortigueira	4155
4156	BR	Brasil	Paraná	PR	Ourizona	4156
4157	BR	Brasil	Paraná	PR	Ouro Verde do Oeste	4157
4158	BR	Brasil	Paraná	PR	Paiçandu	4158
4159	BR	Brasil	Paraná	PR	Palmas	4159
4160	BR	Brasil	Paraná	PR	Palmeira	4160
4161	BR	Brasil	Paraná	PR	Palmital	4161
4162	BR	Brasil	Paraná	PR	Palotina	4162
4979	BR	Brasil	Rio Grande do Sul	RS	Santiago	4979
1652	BR	Brasil	Alagoas	AL	Anadia	1652
2393	BR	Brasil	Minas Gerais	MG	Carlos Chagas	2393
3959	BR	Brasil	Paraná	PR	Cafeara	3959
3960	BR	Brasil	Paraná	PR	Cafelândia	3960
3961	BR	Brasil	Paraná	PR	Cafezal do Sul	3961
3962	BR	Brasil	Paraná	PR	Califórnia	3962
3963	BR	Brasil	Paraná	PR	Cambará	3963
3965	BR	Brasil	Paraná	PR	Cambira	3965
3966	BR	Brasil	Paraná	PR	Campina da Lagoa	3966
3968	BR	Brasil	Paraná	PR	Campina Grande do Sul	3968
3970	BR	Brasil	Paraná	PR	Campo do Tenente	3970
3971	BR	Brasil	Paraná	PR	Campo Largo	3971
3974	BR	Brasil	Paraná	PR	Cândido de Abreu	3974
3975	BR	Brasil	Paraná	PR	Candói	3975
3976	BR	Brasil	Paraná	PR	Cantagalo	3976
4029	BR	Brasil	Paraná	PR	Flórida	4029
4030	BR	Brasil	Paraná	PR	Formosa do Oeste	4030
4031	BR	Brasil	Paraná	PR	Foz do Iguaçu	4031
4167	BR	Brasil	Paraná	PR	Paranavaí	4167
4168	BR	Brasil	Paraná	PR	Pato Bragado	4168
4169	BR	Brasil	Paraná	PR	Pato Branco	4169
4170	BR	Brasil	Paraná	PR	Paula Freitas	4170
4171	BR	Brasil	Paraná	PR	Paulo Frontin	4171
4172	BR	Brasil	Paraná	PR	Peabiru	4172
4173	BR	Brasil	Paraná	PR	Perobal	4173
4184	BR	Brasil	Paraná	PR	Pitangueiras	4184
4185	BR	Brasil	Paraná	PR	Planaltina do Paraná	4185
4186	BR	Brasil	Paraná	PR	Planalto	4186
4187	BR	Brasil	Paraná	PR	Ponta Grossa	4187
4188	BR	Brasil	Paraná	PR	Pontal do Paraná	4188
4189	BR	Brasil	Paraná	PR	Porecatu	4189
4190	BR	Brasil	Paraná	PR	Porto Amazonas	4190
4191	BR	Brasil	Paraná	PR	Porto Barreiro	4191
4195	BR	Brasil	Paraná	PR	Pranchita	4195
4196	BR	Brasil	Paraná	PR	Presidente Castelo Branco	4196
4197	BR	Brasil	Paraná	PR	Primeiro de Maio	4197
4198	BR	Brasil	Paraná	PR	Prudentópolis	4198
4199	BR	Brasil	Paraná	PR	Quarto Centenário	4199
4205	BR	Brasil	Paraná	PR	Quinta do Sol	4205
4206	BR	Brasil	Paraná	PR	Quitandinha	4206
4207	BR	Brasil	Paraná	PR	Ramilândia	4207
4208	BR	Brasil	Paraná	PR	Rancho Alegre	4208
4209	BR	Brasil	Paraná	PR	Rancho Alegre D´oeste	4209
4210	BR	Brasil	Paraná	PR	Realeza	4210
165	BR	Brasil	Pará	PA	Aveiro	165
352	BR	Brasil	Tocantins	TO	Couto de Magalhães	352
390	BR	Brasil	Tocantins	TO	Palmeiras do Tocantins	390
407	BR	Brasil	Tocantins	TO	Pequizeiro	407
1441	BR	Brasil	Paraíba	PB	Sapé	1441
1693	BR	Brasil	Alagoas	AL	Jundiá	1693
1706	BR	Brasil	Alagoas	AL	Messias	1706
1707	BR	Brasil	Alagoas	AL	Minador do Negrão	1707
1708	BR	Brasil	Alagoas	AL	Monteirópolis	1708
1709	BR	Brasil	Alagoas	AL	Murici	1709
2642	BR	Brasil	Minas Gerais	MG	Janaúba	2642
2680	BR	Brasil	Minas Gerais	MG	Lassance	2680
2681	BR	Brasil	Minas Gerais	MG	Lavras	2681
2786	BR	Brasil	Minas Gerais	MG	Padre Paraíso	2786
2787	BR	Brasil	Minas Gerais	MG	Paineiras	2787
2788	BR	Brasil	Minas Gerais	MG	Pains	2788
2789	BR	Brasil	Minas Gerais	MG	Pai Pedro	2789
2790	BR	Brasil	Minas Gerais	MG	Paiva	2790
2791	BR	Brasil	Minas Gerais	MG	Palma	2791
2792	BR	Brasil	Minas Gerais	MG	Palmópolis	2792
2805	BR	Brasil	Minas Gerais	MG	Patos de Minas	2805
2806	BR	Brasil	Minas Gerais	MG	Patrocínio	2806
2830	BR	Brasil	Minas Gerais	MG	Piedade de Caratinga	2830
2832	BR	Brasil	Minas Gerais	MG	Piedade do Rio Grande	2832
2838	BR	Brasil	Minas Gerais	MG	Pirajuba	2838
2839	BR	Brasil	Minas Gerais	MG	Piranga	2839
2840	BR	Brasil	Minas Gerais	MG	Piranguçu	2840
2849	BR	Brasil	Minas Gerais	MG	Poços de Caldas	2849
2863	BR	Brasil	Minas Gerais	MG	Pratinha	2863
2865	BR	Brasil	Minas Gerais	MG	Presidente Juscelino	2865
2866	BR	Brasil	Minas Gerais	MG	Presidente Kubitschek	2866
2867	BR	Brasil	Minas Gerais	MG	Presidente Olegário	2867
2868	BR	Brasil	Minas Gerais	MG	Alto Jequitibá	2868
2869	BR	Brasil	Minas Gerais	MG	Prudente de Morais	2869
2870	BR	Brasil	Minas Gerais	MG	Quartel Geral	2870
2871	BR	Brasil	Minas Gerais	MG	Queluzito	2871
2872	BR	Brasil	Minas Gerais	MG	Raposos	2872
3022	BR	Brasil	Minas Gerais	MG	Senhora do Porto	3022
3023	BR	Brasil	Minas Gerais	MG	Senhora Dos Remédios	3023
3024	BR	Brasil	Minas Gerais	MG	Sericita	3024
3025	BR	Brasil	Minas Gerais	MG	Seritinga	3025
3026	BR	Brasil	Minas Gerais	MG	Serra Azul de Minas	3026
3027	BR	Brasil	Minas Gerais	MG	Serra da Saudade	3027
3082	BR	Brasil	Minas Gerais	MG	Vazante	3082
3083	BR	Brasil	Minas Gerais	MG	Verdelândia	3083
3085	BR	Brasil	Minas Gerais	MG	Veríssimo	3085
88	BR	Brasil	Amazonas	AM	Borba	88
3086	BR	Brasil	Minas Gerais	MG	Vermelho Novo	3086
3087	BR	Brasil	Minas Gerais	MG	Vespasiano	3087
4966	BR	Brasil	Rio Grande do Sul	RS	Sananduva	4966
219	BR	Brasil	Pará	PA	Marapanim	219
266	BR	Brasil	Pará	PA	Santarém Novo	266
296	BR	Brasil	Amapá	AP	Serra do Navio	296
321	BR	Brasil	Tocantins	TO	Araguacema	321
322	BR	Brasil	Tocantins	TO	Araguaçu	322
1447	BR	Brasil	Paraíba	PB	Serraria	1447
1448	BR	Brasil	Paraíba	PB	Sertãozinho	1448
1449	BR	Brasil	Paraíba	PB	Sobrado	1449
1450	BR	Brasil	Paraíba	PB	Solânea	1450
1451	BR	Brasil	Paraíba	PB	Soledade	1451
1452	BR	Brasil	Paraíba	PB	Sossêgo	1452
1453	BR	Brasil	Paraíba	PB	Sousa	1453
1454	BR	Brasil	Paraíba	PB	Sumé	1454
1455	BR	Brasil	Paraíba	PB	Campo de Santana	1455
1456	BR	Brasil	Paraíba	PB	Taperoá	1456
1457	BR	Brasil	Paraíba	PB	Tavares	1457
1458	BR	Brasil	Paraíba	PB	Teixeira	1458
1459	BR	Brasil	Paraíba	PB	Tenório	1459
1460	BR	Brasil	Paraíba	PB	Triunfo	1460
1461	BR	Brasil	Paraíba	PB	Uiraúna	1461
1462	BR	Brasil	Paraíba	PB	Umbuzeiro	1462
1463	BR	Brasil	Paraíba	PB	Várzea	1463
1464	BR	Brasil	Paraíba	PB	Vieirópolis	1464
1465	BR	Brasil	Paraíba	PB	Zabelê	1465
1466	BR	Brasil	Pernambuco	PE	Abreu e Lima	1466
1467	BR	Brasil	Pernambuco	PE	Afogados da Ingazeira	1467
1468	BR	Brasil	Pernambuco	PE	Afrânio	1468
1469	BR	Brasil	Pernambuco	PE	Agrestina	1469
1470	BR	Brasil	Pernambuco	PE	Água Preta	1470
1471	BR	Brasil	Pernambuco	PE	Águas Belas	1471
1472	BR	Brasil	Pernambuco	PE	Alagoinha	1472
1473	BR	Brasil	Pernambuco	PE	Aliança	1473
1474	BR	Brasil	Pernambuco	PE	Altinho	1474
1475	BR	Brasil	Pernambuco	PE	Amaraji	1475
1476	BR	Brasil	Pernambuco	PE	Angelim	1476
1477	BR	Brasil	Pernambuco	PE	Araçoiaba	1477
1478	BR	Brasil	Pernambuco	PE	Araripina	1478
1479	BR	Brasil	Pernambuco	PE	Arcoverde	1479
1480	BR	Brasil	Pernambuco	PE	Barra de Guabiraba	1480
1481	BR	Brasil	Pernambuco	PE	Barreiros	1481
1482	BR	Brasil	Pernambuco	PE	Belém de Maria	1482
1483	BR	Brasil	Pernambuco	PE	Belém de São Francisco	1483
1484	BR	Brasil	Pernambuco	PE	Belo Jardim	1484
1485	BR	Brasil	Pernambuco	PE	Betânia	1485
2679	BR	Brasil	Minas Gerais	MG	Laranjal	2679
4395	BR	Brasil	Santa Catarina	SC	Ermo	4395
166	BR	Brasil	Pará	PA	Bagre	166
184	BR	Brasil	Pará	PA	Canaã Dos Carajás	184
235	BR	Brasil	Pará	PA	Oriximiná	235
254	BR	Brasil	Pará	PA	Rondon do Pará	254
310	BR	Brasil	Amapá	AP	Tartarugalzinho	310
323	BR	Brasil	Tocantins	TO	Araguaína	323
340	BR	Brasil	Tocantins	TO	Cachoeirinha	340
416	BR	Brasil	Tocantins	TO	Praia Norte	416
465	BR	Brasil	Maranhão	MA	Araguanã	465
468	BR	Brasil	Maranhão	MA	Arari	468
469	BR	Brasil	Maranhão	MA	Axixá	469
470	BR	Brasil	Maranhão	MA	Bacabal	470
471	BR	Brasil	Maranhão	MA	Bacabeira	471
472	BR	Brasil	Maranhão	MA	Bacuri	472
473	BR	Brasil	Maranhão	MA	Bacurituba	473
474	BR	Brasil	Maranhão	MA	Balsas	474
475	BR	Brasil	Maranhão	MA	Barão de Grajaú	475
476	BR	Brasil	Maranhão	MA	Barra do Corda	476
477	BR	Brasil	Maranhão	MA	Barreirinhas	477
478	BR	Brasil	Maranhão	MA	Belágua	478
479	BR	Brasil	Maranhão	MA	Bela Vista do Maranhão	479
480	BR	Brasil	Maranhão	MA	Benedito Leite	480
481	BR	Brasil	Maranhão	MA	Bequimão	481
482	BR	Brasil	Maranhão	MA	Bernardo do Mearim	482
483	BR	Brasil	Maranhão	MA	Boa Vista do Gurupi	483
484	BR	Brasil	Maranhão	MA	Bom Jardim	484
485	BR	Brasil	Maranhão	MA	Bom Jesus Das Selvas	485
486	BR	Brasil	Maranhão	MA	Bom Lugar	486
487	BR	Brasil	Maranhão	MA	Brejo	487
488	BR	Brasil	Maranhão	MA	Brejo de Areia	488
489	BR	Brasil	Maranhão	MA	Buriti	489
2831	BR	Brasil	Minas Gerais	MG	Piedade de Ponte Nova	2831
236	BR	Brasil	Pará	PA	Ourém	236
297	BR	Brasil	Amapá	AP	Amapá	297
381	BR	Brasil	Tocantins	TO	Lizarda	381
534	BR	Brasil	Maranhão	MA	Grajaú	534
535	BR	Brasil	Maranhão	MA	Guimarães	535
537	BR	Brasil	Maranhão	MA	Icatu	537
1893	BR	Brasil	Bahia	BA	Caetité	1893
1894	BR	Brasil	Bahia	BA	Cafarnaum	1894
1895	BR	Brasil	Bahia	BA	Cairu	1895
1896	BR	Brasil	Bahia	BA	Caldeirão Grande	1896
1897	BR	Brasil	Bahia	BA	Camacan	1897
1898	BR	Brasil	Bahia	BA	Camaçari	1898
2934	BR	Brasil	Minas Gerais	MG	Santa Rita de Caldas	2934
2935	BR	Brasil	Minas Gerais	MG	Santa Rita de Jacutinga	2935
2936	BR	Brasil	Minas Gerais	MG	Santa Rita de Minas	2936
2937	BR	Brasil	Minas Gerais	MG	Santa Rita de Ibitipoca	2937
2938	BR	Brasil	Minas Gerais	MG	Santa Rita do Itueto	2938
2939	BR	Brasil	Minas Gerais	MG	Santa Rita do Sapucaí	2939
2940	BR	Brasil	Minas Gerais	MG	Santa Rosa da Serra	2940
2941	BR	Brasil	Minas Gerais	MG	Santa Vitória	2941
2942	BR	Brasil	Minas Gerais	MG	Santo Antônio do Amparo	2942
2950	BR	Brasil	Minas Gerais	MG	Santo Hipólito	2950
3200	BR	Brasil	Rio de Janeiro	RJ	Duque de Caxias	3200
3201	BR	Brasil	Rio de Janeiro	RJ	Engenheiro Paulo de Frontin	3201
3338	BR	Brasil	São Paulo	SP	Bernardino de Campos	3338
3341	BR	Brasil	São Paulo	SP	Birigui	3341
3342	BR	Brasil	São Paulo	SP	Biritiba-mirim	3342
3343	BR	Brasil	São Paulo	SP	Boa Esperança do Sul	3343
3346	BR	Brasil	São Paulo	SP	Boituva	3346
3347	BR	Brasil	São Paulo	SP	Bom Jesus Dos Perdões	3347
3348	BR	Brasil	São Paulo	SP	Bom Sucesso de Itararé	3348
3349	BR	Brasil	São Paulo	SP	Borá	3349
3357	BR	Brasil	São Paulo	SP	Brodowski	3357
3358	BR	Brasil	São Paulo	SP	Brotas	3358
3359	BR	Brasil	São Paulo	SP	Buri	3359
3360	BR	Brasil	São Paulo	SP	Buritama	3360
3361	BR	Brasil	São Paulo	SP	Buritizal	3361
3362	BR	Brasil	São Paulo	SP	Cabrália Paulista	3362
3363	BR	Brasil	São Paulo	SP	Cabreúva	3363
3364	BR	Brasil	São Paulo	SP	Caçapava	3364
3365	BR	Brasil	São Paulo	SP	Cachoeira Paulista	3365
3366	BR	Brasil	São Paulo	SP	Caconde	3366
4302	BR	Brasil	Paraná	PR	Uraí	4302
5114	BR	Brasil	Mato Grosso do Sul	MS	Bandeirantes	5114
5115	BR	Brasil	Mato Grosso do Sul	MS	Bataguassu	5115
5145	BR	Brasil	Mato Grosso do Sul	MS	Ivinhema	5145
5146	BR	Brasil	Mato Grosso do Sul	MS	Japorã	5146
5147	BR	Brasil	Mato Grosso do Sul	MS	Jaraguari	5147
38	BR	Brasil	Rondônia	RO	Ministro Andreazza	38
402	BR	Brasil	Tocantins	TO	Paraíso do Tocantins	402
628	BR	Brasil	Maranhão	MA	São Francisco do Maranhão	628
629	BR	Brasil	Maranhão	MA	São João Batista	629
630	BR	Brasil	Maranhão	MA	São João do Carú	630
635	BR	Brasil	Maranhão	MA	São José Dos Basílios	635
637	BR	Brasil	Maranhão	MA	São Luís Gonzaga do Maranhão	637
638	BR	Brasil	Maranhão	MA	São Mateus do Maranhão	638
639	BR	Brasil	Maranhão	MA	São Pedro da Água Branca	639
640	BR	Brasil	Maranhão	MA	São Pedro Dos Crentes	640
641	BR	Brasil	Maranhão	MA	São Raimundo Das Mangabeiras	641
642	BR	Brasil	Maranhão	MA	São Raimundo do Doca Bezerra	642
643	BR	Brasil	Maranhão	MA	São Roberto	643
644	BR	Brasil	Maranhão	MA	São Vicente Ferrer	644
645	BR	Brasil	Maranhão	MA	Satubinha	645
646	BR	Brasil	Maranhão	MA	Senador Alexandre Costa	646
647	BR	Brasil	Maranhão	MA	Senador la Rocque	647
648	BR	Brasil	Maranhão	MA	Serrano do Maranhão	648
649	BR	Brasil	Maranhão	MA	Sítio Novo	649
650	BR	Brasil	Maranhão	MA	Sucupira do Norte	650
651	BR	Brasil	Maranhão	MA	Sucupira do Riachão	651
652	BR	Brasil	Maranhão	MA	Tasso Fragoso	652
653	BR	Brasil	Maranhão	MA	Timbiras	653
884	BR	Brasil	Piauí	PI	União	884
980	BR	Brasil	Ceará	CE	Itapiúna	980
981	BR	Brasil	Ceará	CE	Itarema	981
982	BR	Brasil	Ceará	CE	Itatira	982
983	BR	Brasil	Ceará	CE	Jaguaretama	983
984	BR	Brasil	Ceará	CE	Jaguaribara	984
985	BR	Brasil	Ceará	CE	Jaguaribe	985
986	BR	Brasil	Ceará	CE	Jaguaruana	986
987	BR	Brasil	Ceará	CE	Jardim	987
988	BR	Brasil	Ceará	CE	Jati	988
989	BR	Brasil	Ceará	CE	Jijoca de Jericoacoara	989
990	BR	Brasil	Ceará	CE	Juazeiro do Norte	990
991	BR	Brasil	Ceará	CE	Jucás	991
992	BR	Brasil	Ceará	CE	Lavras da Mangabeira	992
993	BR	Brasil	Ceará	CE	Limoeiro do Norte	993
994	BR	Brasil	Ceará	CE	Madalena	994
995	BR	Brasil	Ceará	CE	Maracanaú	995
996	BR	Brasil	Ceará	CE	Maranguape	996
997	BR	Brasil	Ceará	CE	Marco	997
998	BR	Brasil	Ceará	CE	Martinópole	998
999	BR	Brasil	Ceará	CE	Massapê	999
1000	BR	Brasil	Ceará	CE	Mauriti	1000
1001	BR	Brasil	Ceará	CE	Meruoca	1001
1002	BR	Brasil	Ceará	CE	Milagres	1002
1003	BR	Brasil	Ceará	CE	Milhã	1003
3412	BR	Brasil	São Paulo	SP	Cotia	3412
298	BR	Brasil	Amapá	AP	Pedra Branca do Amapari	298
1004	BR	Brasil	Ceará	CE	Miraíma	1004
2002	BR	Brasil	Bahia	BA	Itabela	2002
2003	BR	Brasil	Bahia	BA	Itaberaba	2003
3041	BR	Brasil	Minas Gerais	MG	Tabuleiro	3041
3042	BR	Brasil	Minas Gerais	MG	Taiobeiras	3042
3043	BR	Brasil	Minas Gerais	MG	Taparuba	3043
3044	BR	Brasil	Minas Gerais	MG	Tapira	3044
3414	BR	Brasil	São Paulo	SP	Cristais Paulista	3414
3415	BR	Brasil	São Paulo	SP	Cruzália	3415
3416	BR	Brasil	São Paulo	SP	Cruzeiro	3416
3417	BR	Brasil	São Paulo	SP	Cubatão	3417
3418	BR	Brasil	São Paulo	SP	Cunha	3418
3419	BR	Brasil	São Paulo	SP	Descalvado	3419
3420	BR	Brasil	São Paulo	SP	Diadema	3420
3421	BR	Brasil	São Paulo	SP	Dirce Reis	3421
3422	BR	Brasil	São Paulo	SP	Divinolândia	3422
3423	BR	Brasil	São Paulo	SP	Dobrada	3423
3424	BR	Brasil	São Paulo	SP	Dois Córregos	3424
3425	BR	Brasil	São Paulo	SP	Dolcinópolis	3425
3426	BR	Brasil	São Paulo	SP	Dourado	3426
3427	BR	Brasil	São Paulo	SP	Dracena	3427
3428	BR	Brasil	São Paulo	SP	Duartina	3428
3429	BR	Brasil	São Paulo	SP	Dumont	3429
3490	BR	Brasil	São Paulo	SP	Ibirá	3490
3512	BR	Brasil	São Paulo	SP	Ipuã	3512
3563	BR	Brasil	São Paulo	SP	Juquiá	3563
3564	BR	Brasil	São Paulo	SP	Juquitiba	3564
3565	BR	Brasil	São Paulo	SP	Lagoinha	3565
3566	BR	Brasil	São Paulo	SP	Laranjal Paulista	3566
3567	BR	Brasil	São Paulo	SP	Lavínia	3567
3568	BR	Brasil	São Paulo	SP	Lavrinhas	3568
3569	BR	Brasil	São Paulo	SP	Leme	3569
3570	BR	Brasil	São Paulo	SP	Lençóis Paulista	3570
3571	BR	Brasil	São Paulo	SP	Limeira	3571
3572	BR	Brasil	São Paulo	SP	Lindóia	3572
3573	BR	Brasil	São Paulo	SP	Lins	3573
3574	BR	Brasil	São Paulo	SP	Lorena	3574
3575	BR	Brasil	São Paulo	SP	Lourdes	3575
3576	BR	Brasil	São Paulo	SP	Louveira	3576
3577	BR	Brasil	São Paulo	SP	Lucélia	3577
3578	BR	Brasil	São Paulo	SP	Lucianópolis	3578
3580	BR	Brasil	São Paulo	SP	Luiziânia	3580
3581	BR	Brasil	São Paulo	SP	Lupércio	3581
3582	BR	Brasil	São Paulo	SP	Lutécia	3582
3583	BR	Brasil	São Paulo	SP	Macatuba	3583
3584	BR	Brasil	São Paulo	SP	Macaubal	3584
3585	BR	Brasil	São Paulo	SP	Macedônia	3585
81	BR	Brasil	Amazonas	AM	Autazes	81
261	BR	Brasil	Pará	PA	Santa Luzia do Pará	261
401	BR	Brasil	Tocantins	TO	Palmeirópolis	401
735	BR	Brasil	Piauí	PI	Curimatá	735
736	BR	Brasil	Piauí	PI	Currais	736
737	BR	Brasil	Piauí	PI	Curralinhos	737
738	BR	Brasil	Piauí	PI	Curral Novo do Piauí	738
739	BR	Brasil	Piauí	PI	Demerval Lobão	739
740	BR	Brasil	Piauí	PI	Dirceu Arcoverde	740
741	BR	Brasil	Piauí	PI	Dom Expedito Lopes	741
742	BR	Brasil	Piauí	PI	Domingos Mourão	742
743	BR	Brasil	Piauí	PI	Dom Inocêncio	743
744	BR	Brasil	Piauí	PI	Elesbão Veloso	744
745	BR	Brasil	Piauí	PI	Eliseu Martins	745
746	BR	Brasil	Piauí	PI	Esperantina	746
747	BR	Brasil	Piauí	PI	Fartura do Piauí	747
748	BR	Brasil	Piauí	PI	Flores do Piauí	748
749	BR	Brasil	Piauí	PI	Floresta do Piauí	749
750	BR	Brasil	Piauí	PI	Floriano	750
751	BR	Brasil	Piauí	PI	Francinópolis	751
752	BR	Brasil	Piauí	PI	Francisco Ayres	752
753	BR	Brasil	Piauí	PI	Francisco Macedo	753
754	BR	Brasil	Piauí	PI	Francisco Santos	754
755	BR	Brasil	Piauí	PI	Fronteiras	755
756	BR	Brasil	Piauí	PI	Geminiano	756
757	BR	Brasil	Piauí	PI	Gilbués	757
759	BR	Brasil	Piauí	PI	Guaribas	759
760	BR	Brasil	Piauí	PI	Hugo Napoleão	760
761	BR	Brasil	Piauí	PI	Ilha Grande	761
762	BR	Brasil	Piauí	PI	Inhuma	762
763	BR	Brasil	Piauí	PI	Ipiranga do Piauí	763
764	BR	Brasil	Piauí	PI	Isaías Coelho	764
765	BR	Brasil	Piauí	PI	Itainópolis	765
766	BR	Brasil	Piauí	PI	Itaueira	766
767	BR	Brasil	Piauí	PI	Jacobina do Piauí	767
768	BR	Brasil	Piauí	PI	Jaicós	768
769	BR	Brasil	Piauí	PI	Jardim do Mulato	769
770	BR	Brasil	Piauí	PI	Jatobá do Piauí	770
771	BR	Brasil	Piauí	PI	Jerumenha	771
772	BR	Brasil	Piauí	PI	João Costa	772
773	BR	Brasil	Piauí	PI	Joaquim Pires	773
774	BR	Brasil	Piauí	PI	Joca Marques	774
775	BR	Brasil	Piauí	PI	José de Freitas	775
776	BR	Brasil	Piauí	PI	Juazeiro do Piauí	776
3146	BR	Brasil	Espírito Santo	ES	Montanha	3146
4490	BR	Brasil	Santa Catarina	SC	Paial	4490
5116	BR	Brasil	Mato Grosso do Sul	MS	Batayporã	5116
5144	BR	Brasil	Mato Grosso do Sul	MS	Itaquiraí	5144
167	BR	Brasil	Pará	PA	Baião	167
227	BR	Brasil	Pará	PA	Muaná	227
239	BR	Brasil	Pará	PA	Palestina do Pará	239
240	BR	Brasil	Pará	PA	Paragominas	240
241	BR	Brasil	Pará	PA	Parauapebas	241
242	BR	Brasil	Pará	PA	Pau D´arco	242
243	BR	Brasil	Pará	PA	Peixe-boi	243
244	BR	Brasil	Pará	PA	Piçarra	244
255	BR	Brasil	Pará	PA	Rurópolis	255
256	BR	Brasil	Pará	PA	Salinópolis	256
267	BR	Brasil	Pará	PA	Santo Antônio do Tauá	267
268	BR	Brasil	Pará	PA	São Caetano de Odivelas	268
269	BR	Brasil	Pará	PA	São Domingos do Araguaia	269
270	BR	Brasil	Pará	PA	São Domingos do Capim	270
271	BR	Brasil	Pará	PA	São Félix do Xingu	271
279	BR	Brasil	Pará	PA	Sapucaia	279
280	BR	Brasil	Pará	PA	Senador José Porfírio	280
281	BR	Brasil	Pará	PA	Soure	281
302	BR	Brasil	Amapá	AP	Itaubal	302
303	BR	Brasil	Amapá	AP	Laranjal do Jari	303
305	BR	Brasil	Amapá	AP	Mazagão	305
306	BR	Brasil	Amapá	AP	Oiapoque	306
307	BR	Brasil	Amapá	AP	Porto Grande	307
327	BR	Brasil	Tocantins	TO	Arraias	327
332	BR	Brasil	Tocantins	TO	Bandeirantes do Tocantins	332
353	BR	Brasil	Tocantins	TO	Cristalândia	353
354	BR	Brasil	Tocantins	TO	Crixás do Tocantins	354
371	BR	Brasil	Tocantins	TO	Itacajá	371
372	BR	Brasil	Tocantins	TO	Itaguatins	372
374	BR	Brasil	Tocantins	TO	Itaporã do Tocantins	374
375	BR	Brasil	Tocantins	TO	Jaú do Tocantins	375
378	BR	Brasil	Tocantins	TO	Lagoa do Tocantins	378
383	BR	Brasil	Tocantins	TO	Marianópolis do Tocantins	383
384	BR	Brasil	Tocantins	TO	Mateiros	384
217	BR	Brasil	Pará	PA	Marabá	217
385	BR	Brasil	Tocantins	TO	Maurilândia do Tocantins	385
386	BR	Brasil	Tocantins	TO	Miracema do Tocantins	386
391	BR	Brasil	Tocantins	TO	Muricilândia	391
392	BR	Brasil	Tocantins	TO	Natividade	392
393	BR	Brasil	Tocantins	TO	Nazaré	393
403	BR	Brasil	Tocantins	TO	Paranã	403
408	BR	Brasil	Tocantins	TO	Colméia	408
409	BR	Brasil	Tocantins	TO	Pindorama do Tocantins	409
425	BR	Brasil	Tocantins	TO	Sandolândia	425
426	BR	Brasil	Tocantins	TO	Santa fé do Araguaia	426
464	BR	Brasil	Maranhão	MA	Apicum-açu	464
791	BR	Brasil	Piauí	PI	Marcos Parente	791
3579	BR	Brasil	São Paulo	SP	Luís Antônio	3579
108	BR	Brasil	Amazonas	AM	Jutaí	108
109	BR	Brasil	Amazonas	AM	Lábrea	109
110	BR	Brasil	Amazonas	AM	Manacapuru	110
111	BR	Brasil	Amazonas	AM	Manaquiri	111
112	BR	Brasil	Amazonas	AM	Manaus	112
113	BR	Brasil	Amazonas	AM	Manicoré	113
124	BR	Brasil	Amazonas	AM	Santa Isabel do Rio Negro	124
125	BR	Brasil	Amazonas	AM	Santo Antônio do Içá	125
126	BR	Brasil	Amazonas	AM	São Gabriel da Cachoeira	126
127	BR	Brasil	Amazonas	AM	São Paulo de Olivença	127
134	BR	Brasil	Amazonas	AM	Uarini	134
135	BR	Brasil	Amazonas	AM	Urucará	135
136	BR	Brasil	Amazonas	AM	Urucurituba	136
137	BR	Brasil	Roraima	RR	Amajari	137
138	BR	Brasil	Roraima	RR	Alto Alegre	138
139	BR	Brasil	Roraima	RR	Boa Vista	139
140	BR	Brasil	Roraima	RR	Bonfim	140
141	BR	Brasil	Roraima	RR	Cantá	141
142	BR	Brasil	Roraima	RR	Caracaraí	142
147	BR	Brasil	Roraima	RR	Pacaraima	147
148	BR	Brasil	Roraima	RR	Rorainópolis	148
149	BR	Brasil	Roraima	RR	São João da Baliza	149
150	BR	Brasil	Roraima	RR	São Luiz	150
168	BR	Brasil	Pará	PA	Bannach	168
172	BR	Brasil	Pará	PA	Benevides	172
173	BR	Brasil	Pará	PA	Bom Jesus do Tocantins	173
174	BR	Brasil	Pará	PA	Bonito	174
175	BR	Brasil	Pará	PA	Bragança	175
176	BR	Brasil	Pará	PA	Brasil Novo	176
177	BR	Brasil	Pará	PA	Brejo Grande do Araguaia	177
178	BR	Brasil	Pará	PA	Breu Branco	178
179	BR	Brasil	Pará	PA	Breves	179
185	BR	Brasil	Pará	PA	Capanema	185
186	BR	Brasil	Pará	PA	Capitão Poço	186
187	BR	Brasil	Pará	PA	Castanhal	187
188	BR	Brasil	Pará	PA	Chaves	188
193	BR	Brasil	Pará	PA	Curionópolis	193
194	BR	Brasil	Pará	PA	Curralinho	194
195	BR	Brasil	Pará	PA	Curuá	195
196	BR	Brasil	Pará	PA	Curuçá	196
197	BR	Brasil	Pará	PA	Dom Eliseu	197
198	BR	Brasil	Pará	PA	Eldorado Dos Carajás	198
199	BR	Brasil	Pará	PA	Faro	199
200	BR	Brasil	Pará	PA	Floresta do Araguaia	200
201	BR	Brasil	Pará	PA	Garrafão do Norte	201
202	BR	Brasil	Pará	PA	Goianésia do Pará	202
203	BR	Brasil	Pará	PA	Gurupá	203
204	BR	Brasil	Pará	PA	Igarapé-açu	204
205	BR	Brasil	Pará	PA	Igarapé-miri	205
228	BR	Brasil	Pará	PA	Nova Esperança do Piriá	228
229	BR	Brasil	Pará	PA	Nova Ipixuna	229
39	BR	Brasil	Rondônia	RO	Mirante da Serra	39
40	BR	Brasil	Rondônia	RO	Monte Negro	40
41	BR	Brasil	Rondônia	RO	Nova União	41
42	BR	Brasil	Rondônia	RO	Parecis	42
43	BR	Brasil	Rondônia	RO	Pimenteiras do Oeste	43
44	BR	Brasil	Rondônia	RO	Primavera de Rondônia	44
45	BR	Brasil	Rondônia	RO	São Felipe D´oeste	45
46	BR	Brasil	Rondônia	RO	São Francisco do Guaporé	46
47	BR	Brasil	Rondônia	RO	Seringueiras	47
48	BR	Brasil	Rondônia	RO	Teixeirópolis	48
49	BR	Brasil	Rondônia	RO	Theobroma	49
50	BR	Brasil	Rondônia	RO	Urupá	50
51	BR	Brasil	Rondônia	RO	Vale do Anari	51
52	BR	Brasil	Rondônia	RO	Vale do Paraíso	52
53	BR	Brasil	Acre	AC	Acrelândia	53
54	BR	Brasil	Acre	AC	Assis Brasil	54
55	BR	Brasil	Acre	AC	Brasiléia	55
56	BR	Brasil	Acre	AC	Bujari	56
57	BR	Brasil	Acre	AC	Capixaba	57
58	BR	Brasil	Acre	AC	Cruzeiro do Sul	58
59	BR	Brasil	Acre	AC	Epitaciolândia	59
60	BR	Brasil	Acre	AC	Feijó	60
61	BR	Brasil	Acre	AC	Jordão	61
62	BR	Brasil	Acre	AC	Mâncio Lima	62
63	BR	Brasil	Acre	AC	Manoel Urbano	63
64	BR	Brasil	Acre	AC	Marechal Thaumaturgo	64
65	BR	Brasil	Acre	AC	Plácido de Castro	65
66	BR	Brasil	Acre	AC	Porto Walter	66
67	BR	Brasil	Acre	AC	Rio Branco	67
68	BR	Brasil	Acre	AC	Rodrigues Alves	68
69	BR	Brasil	Acre	AC	Santa Rosa do Purus	69
70	BR	Brasil	Acre	AC	Senador Guiomard	70
75	BR	Brasil	Amazonas	AM	Alvarães	75
76	BR	Brasil	Amazonas	AM	Amaturá	76
82	BR	Brasil	Amazonas	AM	Barcelos	82
83	BR	Brasil	Amazonas	AM	Barreirinha	83
84	BR	Brasil	Amazonas	AM	Benjamin Constant	84
85	BR	Brasil	Amazonas	AM	Beruri	85
86	BR	Brasil	Amazonas	AM	Boa Vista do Ramos	86
87	BR	Brasil	Amazonas	AM	Boca do Acre	87
89	BR	Brasil	Amazonas	AM	Caapiranga	89
90	BR	Brasil	Amazonas	AM	Canutama	90
91	BR	Brasil	Amazonas	AM	Carauari	91
99	BR	Brasil	Amazonas	AM	Guajará	99
100	BR	Brasil	Amazonas	AM	Humaitá	100
101	BR	Brasil	Amazonas	AM	Ipixuna	101
102	BR	Brasil	Amazonas	AM	Iranduba	102
103	BR	Brasil	Amazonas	AM	Itacoatiara	103
104	BR	Brasil	Amazonas	AM	Itamarati	104
105	BR	Brasil	Amazonas	AM	Itapiranga	105
1	BR	Brasil	Rondônia	RO	Alta Floresta D´oeste	1
2	BR	Brasil	Rondônia	RO	Ariquemes	2
3	BR	Brasil	Rondônia	RO	Cabixi	3
4	BR	Brasil	Rondônia	RO	Cacoal	4
5	BR	Brasil	Rondônia	RO	Cerejeiras	5
6	BR	Brasil	Rondônia	RO	Colorado do Oeste	6
7	BR	Brasil	Rondônia	RO	Corumbiara	7
8	BR	Brasil	Rondônia	RO	Costa Marques	8
9	BR	Brasil	Rondônia	RO	Espigão D´oeste	9
10	BR	Brasil	Rondônia	RO	Guajará-mirim	10
11	BR	Brasil	Rondônia	RO	Jaru	11
12	BR	Brasil	Rondônia	RO	Ji-paraná	12
13	BR	Brasil	Rondônia	RO	Machadinho D´oeste	13
14	BR	Brasil	Rondônia	RO	Nova Brasilândia D´oeste	14
15	BR	Brasil	Rondônia	RO	Ouro Preto do Oeste	15
16	BR	Brasil	Rondônia	RO	Pimenta Bueno	16
17	BR	Brasil	Rondônia	RO	Porto Velho	17
18	BR	Brasil	Rondônia	RO	Presidente Médici	18
19	BR	Brasil	Rondônia	RO	Rio Crespo	19
20	BR	Brasil	Rondônia	RO	Rolim de Moura	20
21	BR	Brasil	Rondônia	RO	Santa Luzia D´oeste	21
22	BR	Brasil	Rondônia	RO	Vilhena	22
23	BR	Brasil	Rondônia	RO	São Miguel do Guaporé	23
24	BR	Brasil	Rondônia	RO	Nova Mamoré	24
25	BR	Brasil	Rondônia	RO	Alvorada D´oeste	25
26	BR	Brasil	Rondônia	RO	Alto Alegre Dos Parecis	26
27	BR	Brasil	Rondônia	RO	Alto Paraíso	27
28	BR	Brasil	Rondônia	RO	Buritis	28
29	BR	Brasil	Rondônia	RO	Novo Horizonte do Oeste	29
30	BR	Brasil	Rondônia	RO	Cacaulândia	30
31	BR	Brasil	Rondônia	RO	Campo Novo de Rondônia	31
32	BR	Brasil	Rondônia	RO	Candeias do Jamari	32
33	BR	Brasil	Rondônia	RO	Castanheiras	33
34	BR	Brasil	Rondônia	RO	Chupinguaia	34
132	BR	Brasil	Amazonas	AM	Tefé	132
180	BR	Brasil	Pará	PA	Bujaru	180
231	BR	Brasil	Pará	PA	Novo Progresso	231
312	BR	Brasil	Tocantins	TO	Abreulândia	312
380	BR	Brasil	Tocantins	TO	Lavandeira	380
418	BR	Brasil	Tocantins	TO	Pugmil	418
1079	BR	Brasil	Rio Grande do Norte	RN	Água Nova	1079
2621	BR	Brasil	Minas Gerais	MG	Itaobim	2621
5071	BR	Brasil	Rio Grande do Sul	RS	Tunas	5071
129	BR	Brasil	Amazonas	AM	Silves	129
160	BR	Brasil	Pará	PA	Anajás	160
250	BR	Brasil	Pará	PA	Primavera	250
304	BR	Brasil	Amapá	AP	Macapá	304
339	BR	Brasil	Tocantins	TO	Buriti do Tocantins	339
349	BR	Brasil	Tocantins	TO	Colinas do Tocantins	349
373	BR	Brasil	Tocantins	TO	Itapiratins	373
410	BR	Brasil	Tocantins	TO	Piraquê	410
495	BR	Brasil	Maranhão	MA	Cajari	495
496	BR	Brasil	Maranhão	MA	Campestre do Maranhão	496
497	BR	Brasil	Maranhão	MA	Cândido Mendes	497
498	BR	Brasil	Maranhão	MA	Cantanhede	498
499	BR	Brasil	Maranhão	MA	Capinzal do Norte	499
500	BR	Brasil	Maranhão	MA	Carolina	500
507	BR	Brasil	Maranhão	MA	Chapadinha	507
1096	BR	Brasil	Rio Grande do Norte	RN	Caiçara do Norte	1096
1097	BR	Brasil	Rio Grande do Norte	RN	Caiçara do Rio do Vento	1097
1098	BR	Brasil	Rio Grande do Norte	RN	Caicó	1098
1099	BR	Brasil	Rio Grande do Norte	RN	Campo Redondo	1099
1100	BR	Brasil	Rio Grande do Norte	RN	Canguaretama	1100
1101	BR	Brasil	Rio Grande do Norte	RN	Caraúbas	1101
1102	BR	Brasil	Rio Grande do Norte	RN	Carnaúba Dos Dantas	1102
1103	BR	Brasil	Rio Grande do Norte	RN	Carnaubais	1103
1104	BR	Brasil	Rio Grande do Norte	RN	Ceará-mirim	1104
1105	BR	Brasil	Rio Grande do Norte	RN	Cerro Corá	1105
1106	BR	Brasil	Rio Grande do Norte	RN	Coronel Ezequiel	1106
1108	BR	Brasil	Rio Grande do Norte	RN	Cruzeta	1108
1189	BR	Brasil	Rio Grande do Norte	RN	Pureza	1189
1190	BR	Brasil	Rio Grande do Norte	RN	Rafael Fernandes	1190
1191	BR	Brasil	Rio Grande do Norte	RN	Rafael Godeiro	1191
1192	BR	Brasil	Rio Grande do Norte	RN	Riacho da Cruz	1192
1193	BR	Brasil	Rio Grande do Norte	RN	Riacho de Santana	1193
1194	BR	Brasil	Rio Grande do Norte	RN	Riachuelo	1194
1195	BR	Brasil	Rio Grande do Norte	RN	Rodolfo Fernandes	1195
1196	BR	Brasil	Rio Grande do Norte	RN	Tibau	1196
1197	BR	Brasil	Rio Grande do Norte	RN	Ruy Barbosa	1197
1198	BR	Brasil	Rio Grande do Norte	RN	Santa Cruz	1198
1199	BR	Brasil	Rio Grande do Norte	RN	Santana do Matos	1199
1200	BR	Brasil	Rio Grande do Norte	RN	Santana do Seridó	1200
1205	BR	Brasil	Rio Grande do Norte	RN	São Francisco do Oeste	1205
1206	BR	Brasil	Rio Grande do Norte	RN	São Gonçalo do Amarante	1206
5159	BR	Brasil	Mato Grosso do Sul	MS	Nova Andradina	5159
5160	BR	Brasil	Mato Grosso do Sul	MS	Novo Horizonte do Sul	5160
5161	BR	Brasil	Mato Grosso do Sul	MS	Paraíso das Águas	5161
5381	BR	Brasil	Goiás	GO	Castelândia	5381
253	BR	Brasil	Pará	PA	Rio Maria	253
292	BR	Brasil	Pará	PA	Vigia	292
316	BR	Brasil	Tocantins	TO	Alvorada	316
366	BR	Brasil	Tocantins	TO	Goianorte	366
631	BR	Brasil	Maranhão	MA	São João do Paraíso	631
632	BR	Brasil	Maranhão	MA	São João do Soter	632
633	BR	Brasil	Maranhão	MA	São João Dos Patos	633
901	BR	Brasil	Ceará	CE	Antonina do Norte	901
1207	BR	Brasil	Rio Grande do Norte	RN	São João do Sabugi	1207
1208	BR	Brasil	Rio Grande do Norte	RN	São José de Mipibu	1208
1209	BR	Brasil	Rio Grande do Norte	RN	São José do Campestre	1209
1210	BR	Brasil	Rio Grande do Norte	RN	São José do Seridó	1210
1211	BR	Brasil	Rio Grande do Norte	RN	São Miguel	1211
1219	BR	Brasil	Rio Grande do Norte	RN	Senador Georgino Avelino	1219
1220	BR	Brasil	Rio Grande do Norte	RN	Serra de São Bento	1220
2217	BR	Brasil	Bahia	BA	Teofilândia	2217
2218	BR	Brasil	Bahia	BA	Teolândia	2218
2219	BR	Brasil	Bahia	BA	Terra Nova	2219
2222	BR	Brasil	Bahia	BA	Uauá	2222
2223	BR	Brasil	Bahia	BA	Ubaíra	2223
2224	BR	Brasil	Bahia	BA	Ubaitaba	2224
2225	BR	Brasil	Bahia	BA	Ubatã	2225
2226	BR	Brasil	Bahia	BA	Uibaí	2226
2227	BR	Brasil	Bahia	BA	Umburanas	2227
2228	BR	Brasil	Bahia	BA	Una	2228
2229	BR	Brasil	Bahia	BA	Urandi	2229
2230	BR	Brasil	Bahia	BA	Uruçuca	2230
2231	BR	Brasil	Bahia	BA	Utinga	2231
2232	BR	Brasil	Bahia	BA	Valença	2232
2234	BR	Brasil	Bahia	BA	Várzea da Roça	2234
2235	BR	Brasil	Bahia	BA	Várzea do Poço	2235
2236	BR	Brasil	Bahia	BA	Várzea Nova	2236
2237	BR	Brasil	Bahia	BA	Varzedo	2237
2238	BR	Brasil	Bahia	BA	Vera Cruz	2238
2239	BR	Brasil	Bahia	BA	Vereda	2239
2795	BR	Brasil	Minas Gerais	MG	Pará de Minas	2795
411	BR	Brasil	Tocantins	TO	Pium	411
524	BR	Brasil	Maranhão	MA	Fortuna	524
582	BR	Brasil	Maranhão	MA	Paraibano	582
604	BR	Brasil	Maranhão	MA	Presidente Vargas	604
622	BR	Brasil	Maranhão	MA	São Bento	622
728	BR	Brasil	Piauí	PI	Colônia do Gurguéia	728
729	BR	Brasil	Piauí	PI	Colônia do Piauí	729
730	BR	Brasil	Piauí	PI	Conceição do Canindé	730
731	BR	Brasil	Piauí	PI	Coronel José Dias	731
1047	BR	Brasil	Ceará	CE	Saboeiro	1047
1285	BR	Brasil	Paraíba	PB	Cachoeira Dos Índios	1285
1286	BR	Brasil	Paraíba	PB	Cacimba de Areia	1286
1287	BR	Brasil	Paraíba	PB	Cacimba de Dentro	1287
1288	BR	Brasil	Paraíba	PB	Cacimbas	1288
1295	BR	Brasil	Paraíba	PB	Capim	1295
1301	BR	Brasil	Paraíba	PB	Caturité	1301
1302	BR	Brasil	Paraíba	PB	Conceição	1302
1303	BR	Brasil	Paraíba	PB	Condado	1303
1304	BR	Brasil	Paraíba	PB	Conde	1304
1305	BR	Brasil	Paraíba	PB	Congo	1305
1306	BR	Brasil	Paraíba	PB	Coremas	1306
2271	BR	Brasil	Minas Gerais	MG	Amparo do Serra	2271
2285	BR	Brasil	Minas Gerais	MG	Araporã	2285
2286	BR	Brasil	Minas Gerais	MG	Arapuá	2286
2287	BR	Brasil	Minas Gerais	MG	Araújos	2287
2288	BR	Brasil	Minas Gerais	MG	Araxá	2288
2289	BR	Brasil	Minas Gerais	MG	Arceburgo	2289
2290	BR	Brasil	Minas Gerais	MG	Arcos	2290
2291	BR	Brasil	Minas Gerais	MG	Areado	2291
2292	BR	Brasil	Minas Gerais	MG	Argirita	2292
2293	BR	Brasil	Minas Gerais	MG	Aricanduva	2293
2294	BR	Brasil	Minas Gerais	MG	Arinos	2294
2295	BR	Brasil	Minas Gerais	MG	Astolfo Dutra	2295
2296	BR	Brasil	Minas Gerais	MG	Ataléia	2296
2297	BR	Brasil	Minas Gerais	MG	Augusto de Lima	2297
2298	BR	Brasil	Minas Gerais	MG	Baependi	2298
2299	BR	Brasil	Minas Gerais	MG	Baldim	2299
2300	BR	Brasil	Minas Gerais	MG	Bambuí	2300
2301	BR	Brasil	Minas Gerais	MG	Bandeira	2301
2302	BR	Brasil	Minas Gerais	MG	Bandeira do Sul	2302
2303	BR	Brasil	Minas Gerais	MG	Barão de Cocais	2303
2304	BR	Brasil	Minas Gerais	MG	Barão de Monte Alto	2304
3084	BR	Brasil	Minas Gerais	MG	Veredinha	3084
438	BR	Brasil	Tocantins	TO	Silvanópolis	438
659	BR	Brasil	Maranhão	MA	Turilândia	659
703	BR	Brasil	Piauí	PI	Brejo do Piauí	703
821	BR	Brasil	Piauí	PI	Pau D´arco do Piauí	821
822	BR	Brasil	Piauí	PI	Paulistana	822
823	BR	Brasil	Piauí	PI	Pavussu	823
1371	BR	Brasil	Paraíba	PB	Nova Olinda	1371
1372	BR	Brasil	Paraíba	PB	Nova Palmeira	1372
1373	BR	Brasil	Paraíba	PB	Olho D´água	1373
1374	BR	Brasil	Paraíba	PB	Olivedos	1374
1375	BR	Brasil	Paraíba	PB	Ouro Velho	1375
1376	BR	Brasil	Paraíba	PB	Parari	1376
2323	BR	Brasil	Minas Gerais	MG	Bom Despacho	2323
2324	BR	Brasil	Minas Gerais	MG	Bom Jardim de Minas	2324
2325	BR	Brasil	Minas Gerais	MG	Bom Jesus da Penha	2325
2326	BR	Brasil	Minas Gerais	MG	Bom Jesus do Amparo	2326
2327	BR	Brasil	Minas Gerais	MG	Bom Jesus do Galho	2327
2328	BR	Brasil	Minas Gerais	MG	Bom Repouso	2328
2329	BR	Brasil	Minas Gerais	MG	Bom Sucesso	2329
2330	BR	Brasil	Minas Gerais	MG	Bonfim	2330
2331	BR	Brasil	Minas Gerais	MG	Bonfinópolis de Minas	2331
2332	BR	Brasil	Minas Gerais	MG	Bonito de Minas	2332
2334	BR	Brasil	Minas Gerais	MG	Botelhos	2334
3312	BR	Brasil	São Paulo	SP	Arujá	3312
3313	BR	Brasil	São Paulo	SP	Aspásia	3313
3314	BR	Brasil	São Paulo	SP	Assis	3314
3315	BR	Brasil	São Paulo	SP	Atibaia	3315
3316	BR	Brasil	São Paulo	SP	Auriflama	3316
3317	BR	Brasil	São Paulo	SP	Avaí	3317
3318	BR	Brasil	São Paulo	SP	Avanhandava	3318
3319	BR	Brasil	São Paulo	SP	Avaré	3319
3320	BR	Brasil	São Paulo	SP	Bady Bassitt	3320
3321	BR	Brasil	São Paulo	SP	Balbinos	3321
3322	BR	Brasil	São Paulo	SP	Bálsamo	3322
3324	BR	Brasil	São Paulo	SP	Barão de Antonina	3324
3325	BR	Brasil	São Paulo	SP	Barbosa	3325
3326	BR	Brasil	São Paulo	SP	Bariri	3326
3327	BR	Brasil	São Paulo	SP	Barra Bonita	3327
3328	BR	Brasil	São Paulo	SP	Barra do Chapéu	3328
3329	BR	Brasil	São Paulo	SP	Barra do Turvo	3329
3331	BR	Brasil	São Paulo	SP	Barrinha	3331
3332	BR	Brasil	São Paulo	SP	Barueri	3332
3333	BR	Brasil	São Paulo	SP	Bastos	3333
3334	BR	Brasil	São Paulo	SP	Batatais	3334
3335	BR	Brasil	São Paulo	SP	Bauru	3335
3336	BR	Brasil	São Paulo	SP	Bebedouro	3336
3337	BR	Brasil	São Paulo	SP	Bento de Abreu	3337
3340	BR	Brasil	São Paulo	SP	Bilac	3340
545	BR	Brasil	Maranhão	MA	Jenipapo Dos Vieiras	545
609	BR	Brasil	Maranhão	MA	Rosário	609
615	BR	Brasil	Maranhão	MA	Santa Luzia do Paruá	615
668	BR	Brasil	Piauí	PI	Acauã	668
758	BR	Brasil	Piauí	PI	Guadalupe	758
919	BR	Brasil	Ceará	CE	Beberibe	919
920	BR	Brasil	Ceará	CE	Bela Cruz	920
921	BR	Brasil	Ceará	CE	Boa Viagem	921
922	BR	Brasil	Ceará	CE	Brejo Santo	922
923	BR	Brasil	Ceará	CE	Camocim	923
924	BR	Brasil	Ceará	CE	Campos Sales	924
925	BR	Brasil	Ceará	CE	Canindé	925
926	BR	Brasil	Ceará	CE	Capistrano	926
927	BR	Brasil	Ceará	CE	Caridade	927
928	BR	Brasil	Ceará	CE	Cariré	928
929	BR	Brasil	Ceará	CE	Caririaçu	929
930	BR	Brasil	Ceará	CE	Cariús	930
931	BR	Brasil	Ceará	CE	Carnaubal	931
932	BR	Brasil	Ceará	CE	Cascavel	932
933	BR	Brasil	Ceará	CE	Catarina	933
934	BR	Brasil	Ceará	CE	Catunda	934
935	BR	Brasil	Ceará	CE	Caucaia	935
936	BR	Brasil	Ceará	CE	Cedro	936
937	BR	Brasil	Ceará	CE	Chaval	937
938	BR	Brasil	Ceará	CE	Choró	938
939	BR	Brasil	Ceará	CE	Chorozinho	939
940	BR	Brasil	Ceará	CE	Coreaú	940
941	BR	Brasil	Ceará	CE	Crateús	941
942	BR	Brasil	Ceará	CE	Crato	942
943	BR	Brasil	Ceará	CE	Croatá	943
944	BR	Brasil	Ceará	CE	Cruz	944
945	BR	Brasil	Ceará	CE	Deputado Irapuan Pinheiro	945
946	BR	Brasil	Ceará	CE	Ererê	946
947	BR	Brasil	Ceará	CE	Eusébio	947
948	BR	Brasil	Ceará	CE	Farias Brito	948
949	BR	Brasil	Ceará	CE	Forquilha	949
950	BR	Brasil	Ceará	CE	Fortaleza	950
3344	BR	Brasil	São Paulo	SP	Bocaina	3344
3345	BR	Brasil	São Paulo	SP	Bofete	3345
439	BR	Brasil	Tocantins	TO	Sítio Novo do Tocantins	439
440	BR	Brasil	Tocantins	TO	Sucupira	440
441	BR	Brasil	Tocantins	TO	Taguatinga	441
442	BR	Brasil	Tocantins	TO	Taipas do Tocantins	442
443	BR	Brasil	Tocantins	TO	Talismã	443
444	BR	Brasil	Tocantins	TO	Palmas	444
445	BR	Brasil	Tocantins	TO	Tocantínia	445
446	BR	Brasil	Tocantins	TO	Tocantinópolis	446
447	BR	Brasil	Tocantins	TO	Tupirama	447
448	BR	Brasil	Tocantins	TO	Tupiratins	448
959	BR	Brasil	Ceará	CE	Guaraciaba do Norte	959
960	BR	Brasil	Ceará	CE	Guaramiranga	960
961	BR	Brasil	Ceará	CE	Hidrolândia	961
962	BR	Brasil	Ceará	CE	Horizonte	962
963	BR	Brasil	Ceará	CE	Ibaretama	963
964	BR	Brasil	Ceará	CE	Ibiapina	964
965	BR	Brasil	Ceará	CE	Ibicuitinga	965
966	BR	Brasil	Ceará	CE	Icapuí	966
967	BR	Brasil	Ceará	CE	Icó	967
968	BR	Brasil	Ceará	CE	Iguatu	968
969	BR	Brasil	Ceará	CE	Independência	969
1497	BR	Brasil	Pernambuco	PE	Cabrobó	1497
1498	BR	Brasil	Pernambuco	PE	Cachoeirinha	1498
1499	BR	Brasil	Pernambuco	PE	Caetés	1499
1500	BR	Brasil	Pernambuco	PE	Calçado	1500
1501	BR	Brasil	Pernambuco	PE	Calumbi	1501
1502	BR	Brasil	Pernambuco	PE	Camaragibe	1502
1503	BR	Brasil	Pernambuco	PE	Camocim de São Félix	1503
1504	BR	Brasil	Pernambuco	PE	Camutanga	1504
1505	BR	Brasil	Pernambuco	PE	Canhotinho	1505
1506	BR	Brasil	Pernambuco	PE	Capoeiras	1506
1507	BR	Brasil	Pernambuco	PE	Carnaíba	1507
1508	BR	Brasil	Pernambuco	PE	Carnaubeira da Penha	1508
1509	BR	Brasil	Pernambuco	PE	Carpina	1509
1510	BR	Brasil	Pernambuco	PE	Caruaru	1510
1511	BR	Brasil	Pernambuco	PE	Casinhas	1511
1512	BR	Brasil	Pernambuco	PE	Catende	1512
1513	BR	Brasil	Pernambuco	PE	Cedro	1513
1514	BR	Brasil	Pernambuco	PE	Chã de Alegria	1514
1515	BR	Brasil	Pernambuco	PE	Chã Grande	1515
1516	BR	Brasil	Pernambuco	PE	Condado	1516
1517	BR	Brasil	Pernambuco	PE	Correntes	1517
4297	BR	Brasil	Paraná	PR	Turvo	4297
1963	BR	Brasil	Bahia	BA	Gandu	1963
526	BR	Brasil	Maranhão	MA	Gonçalves Dias	526
527	BR	Brasil	Maranhão	MA	Governador Archer	527
528	BR	Brasil	Maranhão	MA	Governador Edison Lobão	528
529	BR	Brasil	Maranhão	MA	Governador Eugênio Barros	529
530	BR	Brasil	Maranhão	MA	Governador Luiz Rocha	530
531	BR	Brasil	Maranhão	MA	Governador Newton Bello	531
1039	BR	Brasil	Ceará	CE	Quiterianópolis	1039
1040	BR	Brasil	Ceará	CE	Quixadá	1040
1041	BR	Brasil	Ceará	CE	Quixelô	1041
1042	BR	Brasil	Ceará	CE	Quixeramobim	1042
1043	BR	Brasil	Ceará	CE	Quixeré	1043
1044	BR	Brasil	Ceará	CE	Redenção	1044
1045	BR	Brasil	Ceará	CE	Reriutaba	1045
1538	BR	Brasil	Pernambuco	PE	Ibimirim	1538
1539	BR	Brasil	Pernambuco	PE	Ibirajuba	1539
1540	BR	Brasil	Pernambuco	PE	Igarassu	1540
1541	BR	Brasil	Pernambuco	PE	Iguaraci	1541
1542	BR	Brasil	Pernambuco	PE	Inajá	1542
1543	BR	Brasil	Pernambuco	PE	Ingazeira	1543
1544	BR	Brasil	Pernambuco	PE	Ipojuca	1544
1545	BR	Brasil	Pernambuco	PE	Ipubi	1545
1546	BR	Brasil	Pernambuco	PE	Itacuruba	1546
1547	BR	Brasil	Pernambuco	PE	Itaíba	1547
1548	BR	Brasil	Pernambuco	PE	Ilha de Itamaracá	1548
1549	BR	Brasil	Pernambuco	PE	Itambé	1549
1550	BR	Brasil	Pernambuco	PE	Itapetim	1550
1551	BR	Brasil	Pernambuco	PE	Itapissuma	1551
2453	BR	Brasil	Minas Gerais	MG	Cordislândia	2453
2454	BR	Brasil	Minas Gerais	MG	Corinto	2454
2455	BR	Brasil	Minas Gerais	MG	Coroaci	2455
2456	BR	Brasil	Minas Gerais	MG	Coromandel	2456
2457	BR	Brasil	Minas Gerais	MG	Coronel Fabriciano	2457
2458	BR	Brasil	Minas Gerais	MG	Coronel Murta	2458
2459	BR	Brasil	Minas Gerais	MG	Coronel Pacheco	2459
2460	BR	Brasil	Minas Gerais	MG	Coronel Xavier Chaves	2460
2461	BR	Brasil	Minas Gerais	MG	Córrego Danta	2461
2467	BR	Brasil	Minas Gerais	MG	Cristais	2467
2468	BR	Brasil	Minas Gerais	MG	Cristália	2468
2469	BR	Brasil	Minas Gerais	MG	Cristiano Otoni	2469
2470	BR	Brasil	Minas Gerais	MG	Cristina	2470
2471	BR	Brasil	Minas Gerais	MG	Crucilândia	2471
2472	BR	Brasil	Minas Gerais	MG	Cruzeiro da Fortaleza	2472
2473	BR	Brasil	Minas Gerais	MG	Cruzília	2473
2474	BR	Brasil	Minas Gerais	MG	Cuparaque	2474
2476	BR	Brasil	Minas Gerais	MG	Curvelo	2476
2477	BR	Brasil	Minas Gerais	MG	Datas	2477
3441	BR	Brasil	São Paulo	SP	Estrela D´oeste	3441
617	BR	Brasil	Maranhão	MA	Santa Rita	617
618	BR	Brasil	Maranhão	MA	Santana do Maranhão	618
619	BR	Brasil	Maranhão	MA	Santo Amaro do Maranhão	619
636	BR	Brasil	Maranhão	MA	São Luís	636
1117	BR	Brasil	Rio Grande do Norte	RN	Fernando Pedroza	1117
1118	BR	Brasil	Rio Grande do Norte	RN	Florânia	1118
1119	BR	Brasil	Rio Grande do Norte	RN	Francisco Dantas	1119
1120	BR	Brasil	Rio Grande do Norte	RN	Frutuoso Gomes	1120
1609	BR	Brasil	Pernambuco	PE	Santa Filomena	1609
1610	BR	Brasil	Pernambuco	PE	Santa Maria da Boa Vista	1610
1611	BR	Brasil	Pernambuco	PE	Santa Maria do Cambucá	1611
1612	BR	Brasil	Pernambuco	PE	Santa Terezinha	1612
1613	BR	Brasil	Pernambuco	PE	São Benedito do Sul	1613
1614	BR	Brasil	Pernambuco	PE	São Bento do Una	1614
1615	BR	Brasil	Pernambuco	PE	São Caitano	1615
1616	BR	Brasil	Pernambuco	PE	São João	1616
2478	BR	Brasil	Minas Gerais	MG	Delfim Moreira	2478
2479	BR	Brasil	Minas Gerais	MG	Delfinópolis	2479
2480	BR	Brasil	Minas Gerais	MG	Delta	2480
2481	BR	Brasil	Minas Gerais	MG	Descoberto	2481
2482	BR	Brasil	Minas Gerais	MG	Desterro de Entre Rios	2482
2483	BR	Brasil	Minas Gerais	MG	Desterro do Melo	2483
2484	BR	Brasil	Minas Gerais	MG	Diamantina	2484
2485	BR	Brasil	Minas Gerais	MG	Diogo de Vasconcelos	2485
2486	BR	Brasil	Minas Gerais	MG	Dionísio	2486
2487	BR	Brasil	Minas Gerais	MG	Divinésia	2487
2488	BR	Brasil	Minas Gerais	MG	Divino	2488
2489	BR	Brasil	Minas Gerais	MG	Divino Das Laranjeiras	2489
2491	BR	Brasil	Minas Gerais	MG	Divinópolis	2491
2492	BR	Brasil	Minas Gerais	MG	Divisa Alegre	2492
2493	BR	Brasil	Minas Gerais	MG	Divisa Nova	2493
2494	BR	Brasil	Minas Gerais	MG	Divisópolis	2494
3982	BR	Brasil	Paraná	PR	Castro	3982
4916	BR	Brasil	Rio Grande do Sul	RS	Pejuçara	4916
715	BR	Brasil	Piauí	PI	Canavieira	715
716	BR	Brasil	Piauí	PI	Canto do Buriti	716
717	BR	Brasil	Piauí	PI	Capitão de Campos	717
718	BR	Brasil	Piauí	PI	Capitão Gervásio Oliveira	718
720	BR	Brasil	Piauí	PI	Caraúbas do Piauí	720
1201	BR	Brasil	Rio Grande do Norte	RN	Santo Antônio	1201
1202	BR	Brasil	Rio Grande do Norte	RN	São Bento do Norte	1202
1203	BR	Brasil	Rio Grande do Norte	RN	São Bento do Trairí	1203
1204	BR	Brasil	Rio Grande do Norte	RN	São Fernando	1204
1694	BR	Brasil	Alagoas	AL	Junqueiro	1694
1695	BR	Brasil	Alagoas	AL	Lagoa da Canoa	1695
1696	BR	Brasil	Alagoas	AL	Limoeiro de Anadia	1696
1697	BR	Brasil	Alagoas	AL	Maceió	1697
1698	BR	Brasil	Alagoas	AL	Major Isidoro	1698
1699	BR	Brasil	Alagoas	AL	Maragogi	1699
1700	BR	Brasil	Alagoas	AL	Maravilha	1700
1701	BR	Brasil	Alagoas	AL	Marechal Deodoro	1701
1702	BR	Brasil	Alagoas	AL	Maribondo	1702
1703	BR	Brasil	Alagoas	AL	Mar Vermelho	1703
1704	BR	Brasil	Alagoas	AL	Mata Grande	1704
2531	BR	Brasil	Minas Gerais	MG	Fernandes Tourinho	2531
2532	BR	Brasil	Minas Gerais	MG	Ferros	2532
2533	BR	Brasil	Minas Gerais	MG	Fervedouro	2533
2534	BR	Brasil	Minas Gerais	MG	Florestal	2534
2535	BR	Brasil	Minas Gerais	MG	Formiga	2535
2540	BR	Brasil	Minas Gerais	MG	Francisco Dumont	2540
2541	BR	Brasil	Minas Gerais	MG	Francisco sá	2541
2542	BR	Brasil	Minas Gerais	MG	Franciscópolis	2542
2543	BR	Brasil	Minas Gerais	MG	Frei Gaspar	2543
2544	BR	Brasil	Minas Gerais	MG	Frei Inocêncio	2544
2545	BR	Brasil	Minas Gerais	MG	Frei Lagonegro	2545
2546	BR	Brasil	Minas Gerais	MG	Fronteira	2546
2547	BR	Brasil	Minas Gerais	MG	Fronteira Dos Vales	2547
2548	BR	Brasil	Minas Gerais	MG	Fruta de Leite	2548
2549	BR	Brasil	Minas Gerais	MG	Frutal	2549
2550	BR	Brasil	Minas Gerais	MG	Funilândia	2550
2551	BR	Brasil	Minas Gerais	MG	Galiléia	2551
2552	BR	Brasil	Minas Gerais	MG	Gameleiras	2552
2556	BR	Brasil	Minas Gerais	MG	Gonçalves	2556
2557	BR	Brasil	Minas Gerais	MG	Gonzaga	2557
3487	BR	Brasil	São Paulo	SP	Iacri	3487
4383	BR	Brasil	Santa Catarina	SC	Coronel Martins	4383
815	BR	Brasil	Piauí	PI	Palmeirais	815
816	BR	Brasil	Piauí	PI	Paquetá	816
817	BR	Brasil	Piauí	PI	Parnaguá	817
818	BR	Brasil	Piauí	PI	Parnaíba	818
827	BR	Brasil	Piauí	PI	Picos	827
1289	BR	Brasil	Paraíba	PB	Caiçara	1289
1290	BR	Brasil	Paraíba	PB	Cajazeiras	1290
1291	BR	Brasil	Paraíba	PB	Cajazeirinhas	1291
1292	BR	Brasil	Paraíba	PB	Caldas Brandão	1292
1293	BR	Brasil	Paraíba	PB	Camalaú	1293
1775	BR	Brasil	Sergipe	SE	General Maynard	1775
1776	BR	Brasil	Sergipe	SE	Gracho Cardoso	1776
1777	BR	Brasil	Sergipe	SE	Ilha Das Flores	1777
1778	BR	Brasil	Sergipe	SE	Indiaroba	1778
1779	BR	Brasil	Sergipe	SE	Itabaiana	1779
1780	BR	Brasil	Sergipe	SE	Itabaianinha	1780
1781	BR	Brasil	Sergipe	SE	Itabi	1781
1782	BR	Brasil	Sergipe	SE	Itaporanga D´ajuda	1782
1783	BR	Brasil	Sergipe	SE	Japaratuba	1783
1784	BR	Brasil	Sergipe	SE	Japoatã	1784
2576	BR	Brasil	Minas Gerais	MG	Iapu	2576
2577	BR	Brasil	Minas Gerais	MG	Ibertioga	2577
2578	BR	Brasil	Minas Gerais	MG	Ibiá	2578
2579	BR	Brasil	Minas Gerais	MG	Ibiaí	2579
2580	BR	Brasil	Minas Gerais	MG	Ibiracatu	2580
2581	BR	Brasil	Minas Gerais	MG	Ibiraci	2581
2582	BR	Brasil	Minas Gerais	MG	Ibirité	2582
2583	BR	Brasil	Minas Gerais	MG	Ibitiúra de Minas	2583
2584	BR	Brasil	Minas Gerais	MG	Ibituruna	2584
2585	BR	Brasil	Minas Gerais	MG	Icaraí de Minas	2585
2586	BR	Brasil	Minas Gerais	MG	Igarapé	2586
2587	BR	Brasil	Minas Gerais	MG	Igaratinga	2587
2588	BR	Brasil	Minas Gerais	MG	Iguatama	2588
2589	BR	Brasil	Minas Gerais	MG	Ijaci	2589
2590	BR	Brasil	Minas Gerais	MG	Ilicínea	2590
2591	BR	Brasil	Minas Gerais	MG	Imbé de Minas	2591
2592	BR	Brasil	Minas Gerais	MG	Inconfidentes	2592
2593	BR	Brasil	Minas Gerais	MG	Indaiabira	2593
2594	BR	Brasil	Minas Gerais	MG	Indianópolis	2594
916	BR	Brasil	Ceará	CE	Barro	916
917	BR	Brasil	Ceará	CE	Barroquinha	917
1388	BR	Brasil	Paraíba	PB	Pirpirituba	1388
1394	BR	Brasil	Paraíba	PB	Prata	1394
1861	BR	Brasil	Bahia	BA	Barra	1861
1862	BR	Brasil	Bahia	BA	Barra da Estiva	1862
1863	BR	Brasil	Bahia	BA	Barra do Choça	1863
1864	BR	Brasil	Bahia	BA	Barra do Mendes	1864
2625	BR	Brasil	Minas Gerais	MG	Itatiaiuçu	2625
2626	BR	Brasil	Minas Gerais	MG	Itaú de Minas	2626
2627	BR	Brasil	Minas Gerais	MG	Itaúna	2627
2628	BR	Brasil	Minas Gerais	MG	Itaverava	2628
2629	BR	Brasil	Minas Gerais	MG	Itinga	2629
2630	BR	Brasil	Minas Gerais	MG	Itueta	2630
2631	BR	Brasil	Minas Gerais	MG	Ituiutaba	2631
2634	BR	Brasil	Minas Gerais	MG	Itutinga	2634
3587	BR	Brasil	São Paulo	SP	Mairinque	3587
3588	BR	Brasil	São Paulo	SP	Mairiporã	3588
3590	BR	Brasil	São Paulo	SP	Marabá Paulista	3590
3591	BR	Brasil	São Paulo	SP	Maracaí	3591
3596	BR	Brasil	São Paulo	SP	Martinópolis	3596
3597	BR	Brasil	São Paulo	SP	Matão	3597
3598	BR	Brasil	São Paulo	SP	Mauá	3598
3599	BR	Brasil	São Paulo	SP	Mendonça	3599
3600	BR	Brasil	São Paulo	SP	Meridiano	3600
3601	BR	Brasil	São Paulo	SP	Mesópolis	3601
3602	BR	Brasil	São Paulo	SP	Miguelópolis	3602
3603	BR	Brasil	São Paulo	SP	Mineiros do Tietê	3603
3604	BR	Brasil	São Paulo	SP	Miracatu	3604
3605	BR	Brasil	São Paulo	SP	Mira Estrela	3605
3609	BR	Brasil	São Paulo	SP	Mirassolândia	3609
3622	BR	Brasil	São Paulo	SP	Monteiro Lobato	3622
3623	BR	Brasil	São Paulo	SP	Monte Mor	3623
3624	BR	Brasil	São Paulo	SP	Morro Agudo	3624
3625	BR	Brasil	São Paulo	SP	Morungaba	3625
3626	BR	Brasil	São Paulo	SP	Motuca	3626
3627	BR	Brasil	São Paulo	SP	Murutinga do Sul	3627
3629	BR	Brasil	São Paulo	SP	Narandiba	3629
3630	BR	Brasil	São Paulo	SP	Natividade da Serra	3630
3631	BR	Brasil	São Paulo	SP	Nazaré Paulista	3631
3632	BR	Brasil	São Paulo	SP	Neves Paulista	3632
4596	BR	Brasil	Santa Catarina	SC	Vargem	4596
1030	BR	Brasil	Ceará	CE	Pentecoste	1030
1031	BR	Brasil	Ceará	CE	Pereiro	1031
1032	BR	Brasil	Ceará	CE	Pindoretama	1032
1489	BR	Brasil	Pernambuco	PE	Bom Jardim	1489
1490	BR	Brasil	Pernambuco	PE	Bonito	1490
1491	BR	Brasil	Pernambuco	PE	Brejão	1491
1965	BR	Brasil	Bahia	BA	Gentio do Ouro	1965
1966	BR	Brasil	Bahia	BA	Glória	1966
1967	BR	Brasil	Bahia	BA	Gongogi	1967
1968	BR	Brasil	Bahia	BA	Governador Mangabeira	1968
1969	BR	Brasil	Bahia	BA	Guajeru	1969
1970	BR	Brasil	Bahia	BA	Guanambi	1970
1971	BR	Brasil	Bahia	BA	Guaratinga	1971
2723	BR	Brasil	Minas Gerais	MG	Medina	2723
2724	BR	Brasil	Minas Gerais	MG	Mendes Pimentel	2724
2725	BR	Brasil	Minas Gerais	MG	Mercês	2725
2726	BR	Brasil	Minas Gerais	MG	Mesquita	2726
2727	BR	Brasil	Minas Gerais	MG	Minas Novas	2727
2728	BR	Brasil	Minas Gerais	MG	Minduri	2728
2729	BR	Brasil	Minas Gerais	MG	Mirabela	2729
2730	BR	Brasil	Minas Gerais	MG	Miradouro	2730
2742	BR	Brasil	Minas Gerais	MG	Monte Formoso	2742
2743	BR	Brasil	Minas Gerais	MG	Monte Santo de Minas	2743
2744	BR	Brasil	Minas Gerais	MG	Montes Claros	2744
2745	BR	Brasil	Minas Gerais	MG	Monte Sião	2745
3653	BR	Brasil	São Paulo	SP	Orindiúva	3653
3654	BR	Brasil	São Paulo	SP	Orlândia	3654
3655	BR	Brasil	São Paulo	SP	Osasco	3655
3656	BR	Brasil	São Paulo	SP	Oscar Bressane	3656
3657	BR	Brasil	São Paulo	SP	Osvaldo Cruz	3657
3658	BR	Brasil	São Paulo	SP	Ourinhos	3658
3659	BR	Brasil	São Paulo	SP	Ouroeste	3659
3660	BR	Brasil	São Paulo	SP	Ouro Verde	3660
3661	BR	Brasil	São Paulo	SP	Pacaembu	3661
3662	BR	Brasil	São Paulo	SP	Palestina	3662
3663	BR	Brasil	São Paulo	SP	Palmares Paulista	3663
3664	BR	Brasil	São Paulo	SP	Palmeira D´oeste	3664
3665	BR	Brasil	São Paulo	SP	Palmital	3665
3666	BR	Brasil	São Paulo	SP	Panorama	3666
3667	BR	Brasil	São Paulo	SP	Paraguaçu Paulista	3667
3668	BR	Brasil	São Paulo	SP	Paraibuna	3668
3669	BR	Brasil	São Paulo	SP	Paraíso	3669
3670	BR	Brasil	São Paulo	SP	Paranapanema	3670
3671	BR	Brasil	São Paulo	SP	Paranapuã	3671
3672	BR	Brasil	São Paulo	SP	Parapuã	3672
3673	BR	Brasil	São Paulo	SP	Pardinho	3673
3674	BR	Brasil	São Paulo	SP	Pariquera-açu	3674
3675	BR	Brasil	São Paulo	SP	Parisi	3675
3676	BR	Brasil	São Paulo	SP	Patrocínio Paulista	3676
1127	BR	Brasil	Rio Grande do Norte	RN	Ipanguaçu	1127
1128	BR	Brasil	Rio Grande do Norte	RN	Ipueira	1128
1129	BR	Brasil	Rio Grande do Norte	RN	Itajá	1129
1130	BR	Brasil	Rio Grande do Norte	RN	Itaú	1130
1131	BR	Brasil	Rio Grande do Norte	RN	Jaçanã	1131
1587	BR	Brasil	Pernambuco	PE	Paulista	1587
1588	BR	Brasil	Pernambuco	PE	Pedra	1588
1589	BR	Brasil	Pernambuco	PE	Pesqueira	1589
1590	BR	Brasil	Pernambuco	PE	Petrolândia	1590
1591	BR	Brasil	Pernambuco	PE	Petrolina	1591
1592	BR	Brasil	Pernambuco	PE	Poção	1592
2069	BR	Brasil	Bahia	BA	Maiquinique	2069
2070	BR	Brasil	Bahia	BA	Mairi	2070
2071	BR	Brasil	Bahia	BA	Malhada	2071
2072	BR	Brasil	Bahia	BA	Malhada de Pedras	2072
2073	BR	Brasil	Bahia	BA	Manoel Vitorino	2073
2074	BR	Brasil	Bahia	BA	Mansidão	2074
2075	BR	Brasil	Bahia	BA	Maracás	2075
2076	BR	Brasil	Bahia	BA	Maragogipe	2076
2077	BR	Brasil	Bahia	BA	Maraú	2077
2078	BR	Brasil	Bahia	BA	Marcionílio Souza	2078
2079	BR	Brasil	Bahia	BA	Mascote	2079
2080	BR	Brasil	Bahia	BA	Mata de São João	2080
2807	BR	Brasil	Minas Gerais	MG	Patrocínio do Muriaé	2807
2808	BR	Brasil	Minas Gerais	MG	Paula Cândido	2808
2810	BR	Brasil	Minas Gerais	MG	Pavão	2810
2811	BR	Brasil	Minas Gerais	MG	Peçanha	2811
2812	BR	Brasil	Minas Gerais	MG	Pedra Azul	2812
2813	BR	Brasil	Minas Gerais	MG	Pedra Bonita	2813
2814	BR	Brasil	Minas Gerais	MG	Pedra do Anta	2814
2815	BR	Brasil	Minas Gerais	MG	Pedra do Indaiá	2815
2816	BR	Brasil	Minas Gerais	MG	Pedra Dourada	2816
2817	BR	Brasil	Minas Gerais	MG	Pedralva	2817
2818	BR	Brasil	Minas Gerais	MG	Pedras de Maria da Cruz	2818
2819	BR	Brasil	Minas Gerais	MG	Pedrinópolis	2819
2820	BR	Brasil	Minas Gerais	MG	Pedro Leopoldo	2820
2821	BR	Brasil	Minas Gerais	MG	Pedro Teixeira	2821
2822	BR	Brasil	Minas Gerais	MG	Pequeri	2822
2823	BR	Brasil	Minas Gerais	MG	Pequi	2823
2824	BR	Brasil	Minas Gerais	MG	Perdigão	2824
2825	BR	Brasil	Minas Gerais	MG	Perdizes	2825
2826	BR	Brasil	Minas Gerais	MG	Perdões	2826
2827	BR	Brasil	Minas Gerais	MG	Periquito	2827
2828	BR	Brasil	Minas Gerais	MG	Pescador	2828
2829	BR	Brasil	Minas Gerais	MG	Piau	2829
5005	BR	Brasil	Rio Grande do Sul	RS	São Leopoldo	5005
1212	BR	Brasil	Rio Grande do Norte	RN	São Miguel do Gostoso	1212
1213	BR	Brasil	Rio Grande do Norte	RN	São Paulo do Potengi	1213
1214	BR	Brasil	Rio Grande do Norte	RN	São Pedro	1214
1215	BR	Brasil	Rio Grande do Norte	RN	São Rafael	1215
1216	BR	Brasil	Rio Grande do Norte	RN	São Tomé	1216
1964	BR	Brasil	Bahia	BA	Gavião	1964
1217	BR	Brasil	Rio Grande do Norte	RN	São Vicente	1217
1218	BR	Brasil	Rio Grande do Norte	RN	Senador Elói de Souza	1218
1676	BR	Brasil	Alagoas	AL	Delmiro Gouveia	1676
1677	BR	Brasil	Alagoas	AL	Dois Riachos	1677
1678	BR	Brasil	Alagoas	AL	Estrela de Alagoas	1678
1679	BR	Brasil	Alagoas	AL	Feira Grande	1679
1680	BR	Brasil	Alagoas	AL	Feliz Deserto	1680
1681	BR	Brasil	Alagoas	AL	Flexeiras	1681
1682	BR	Brasil	Alagoas	AL	Girau do Ponciano	1682
1683	BR	Brasil	Alagoas	AL	Ibateguara	1683
2146	BR	Brasil	Bahia	BA	Quixabeira	2146
2147	BR	Brasil	Bahia	BA	Rafael Jambeiro	2147
2148	BR	Brasil	Bahia	BA	Remanso	2148
2149	BR	Brasil	Bahia	BA	Retirolândia	2149
2150	BR	Brasil	Bahia	BA	Riachão Das Neves	2150
2151	BR	Brasil	Bahia	BA	Riachão do Jacuípe	2151
2152	BR	Brasil	Bahia	BA	Riacho de Santana	2152
2153	BR	Brasil	Bahia	BA	Ribeira do Amparo	2153
2154	BR	Brasil	Bahia	BA	Ribeira do Pombal	2154
2155	BR	Brasil	Bahia	BA	Ribeirão do Largo	2155
2156	BR	Brasil	Bahia	BA	Rio de Contas	2156
2157	BR	Brasil	Bahia	BA	Rio do Antônio	2157
2158	BR	Brasil	Bahia	BA	Rio do Pires	2158
2159	BR	Brasil	Bahia	BA	Rio Real	2159
2160	BR	Brasil	Bahia	BA	Rodelas	2160
2161	BR	Brasil	Bahia	BA	Ruy Barbosa	2161
4102	BR	Brasil	Paraná	PR	Lobato	4102
5059	BR	Brasil	Rio Grande do Sul	RS	Tramandaí	5059
5060	BR	Brasil	Rio Grande do Sul	RS	Travesseiro	5060
5061	BR	Brasil	Rio Grande do Sul	RS	Três Arroios	5061
5117	BR	Brasil	Mato Grosso do Sul	MS	Bela Vista	5117
5118	BR	Brasil	Mato Grosso do Sul	MS	Bodoquena	5118
5119	BR	Brasil	Mato Grosso do Sul	MS	Bonito	5119
5120	BR	Brasil	Mato Grosso do Sul	MS	Brasilândia	5120
5121	BR	Brasil	Mato Grosso do Sul	MS	Caarapó	5121
5122	BR	Brasil	Mato Grosso do Sul	MS	Camapuã	5122
5123	BR	Brasil	Mato Grosso do Sul	MS	Campo Grande	5123
5124	BR	Brasil	Mato Grosso do Sul	MS	Caracol	5124
5139	BR	Brasil	Mato Grosso do Sul	MS	Glória de Dourados	5139
5140	BR	Brasil	Mato Grosso do Sul	MS	Guia Lopes da Laguna	5140
5142	BR	Brasil	Mato Grosso do Sul	MS	Inocência	5142
5143	BR	Brasil	Mato Grosso do Sul	MS	Itaporã	5143
1294	BR	Brasil	Paraíba	PB	Campina Grande	1294
1296	BR	Brasil	Paraíba	PB	Caraúbas	1296
1297	BR	Brasil	Paraíba	PB	Carrapateira	1297
1298	BR	Brasil	Paraíba	PB	Casserengue	1298
1299	BR	Brasil	Paraíba	PB	Catingueira	1299
1300	BR	Brasil	Paraíba	PB	Catolé do Rocha	1300
1755	BR	Brasil	Sergipe	SE	Aracaju	1755
1756	BR	Brasil	Sergipe	SE	Arauá	1756
1757	BR	Brasil	Sergipe	SE	Areia Branca	1757
1758	BR	Brasil	Sergipe	SE	Barra Dos Coqueiros	1758
1759	BR	Brasil	Sergipe	SE	Boquim	1759
1760	BR	Brasil	Sergipe	SE	Brejo Grande	1760
1761	BR	Brasil	Sergipe	SE	Campo do Brito	1761
2203	BR	Brasil	Bahia	BA	Serrolândia	2203
2204	BR	Brasil	Bahia	BA	Simões Filho	2204
2205	BR	Brasil	Bahia	BA	Sítio do Mato	2205
2206	BR	Brasil	Bahia	BA	Sítio do Quinto	2206
2207	BR	Brasil	Bahia	BA	Sobradinho	2207
2208	BR	Brasil	Bahia	BA	Souto Soares	2208
2209	BR	Brasil	Bahia	BA	Tabocas do Brejo Velho	2209
2210	BR	Brasil	Bahia	BA	Tanhaçu	2210
2211	BR	Brasil	Bahia	BA	Tanque Novo	2211
2212	BR	Brasil	Bahia	BA	Tanquinho	2212
2213	BR	Brasil	Bahia	BA	Taperoá	2213
2214	BR	Brasil	Bahia	BA	Tapiramutá	2214
2215	BR	Brasil	Bahia	BA	Teixeira de Freitas	2215
2216	BR	Brasil	Bahia	BA	Teodoro Sampaio	2216
2891	BR	Brasil	Minas Gerais	MG	Rio Pardo de Minas	2891
2892	BR	Brasil	Minas Gerais	MG	Rio Piracicaba	2892
2893	BR	Brasil	Minas Gerais	MG	Rio Pomba	2893
2894	BR	Brasil	Minas Gerais	MG	Rio Preto	2894
2895	BR	Brasil	Minas Gerais	MG	Rio Vermelho	2895
2896	BR	Brasil	Minas Gerais	MG	Ritápolis	2896
2897	BR	Brasil	Minas Gerais	MG	Rochedo de Minas	2897
2898	BR	Brasil	Minas Gerais	MG	Rodeiro	2898
2899	BR	Brasil	Minas Gerais	MG	Romaria	2899
2900	BR	Brasil	Minas Gerais	MG	Rosário da Limeira	2900
2901	BR	Brasil	Minas Gerais	MG	Rubelita	2901
2902	BR	Brasil	Minas Gerais	MG	Rubim	2902
2903	BR	Brasil	Minas Gerais	MG	Sabará	2903
2904	BR	Brasil	Minas Gerais	MG	Sabinópolis	2904
2905	BR	Brasil	Minas Gerais	MG	Sacramento	2905
2906	BR	Brasil	Minas Gerais	MG	Salinas	2906
2907	BR	Brasil	Minas Gerais	MG	Salto da Divisa	2907
2908	BR	Brasil	Minas Gerais	MG	Santa Bárbara	2908
2909	BR	Brasil	Minas Gerais	MG	Santa Bárbara do Leste	2909
2910	BR	Brasil	Minas Gerais	MG	Santa Bárbara do Monte Verde	2910
2911	BR	Brasil	Minas Gerais	MG	Santa Bárbara do Tugúrio	2911
2912	BR	Brasil	Minas Gerais	MG	Santa Cruz de Minas	2912
1395	BR	Brasil	Paraíba	PB	Princesa Isabel	1395
1396	BR	Brasil	Paraíba	PB	Puxinanã	1396
1397	BR	Brasil	Paraíba	PB	Queimadas	1397
1398	BR	Brasil	Paraíba	PB	Quixabá	1398
1847	BR	Brasil	Bahia	BA	Antônio Cardoso	1847
1848	BR	Brasil	Bahia	BA	Antônio Gonçalves	1848
1849	BR	Brasil	Bahia	BA	Aporá	1849
1850	BR	Brasil	Bahia	BA	Apuarema	1850
2272	BR	Brasil	Minas Gerais	MG	Andradas	2272
2273	BR	Brasil	Minas Gerais	MG	Cachoeira de Pajeú	2273
2279	BR	Brasil	Minas Gerais	MG	Araçaí	2279
2280	BR	Brasil	Minas Gerais	MG	Aracitaba	2280
2281	BR	Brasil	Minas Gerais	MG	Araçuaí	2281
2282	BR	Brasil	Minas Gerais	MG	Araguari	2282
2283	BR	Brasil	Minas Gerais	MG	Arantina	2283
2284	BR	Brasil	Minas Gerais	MG	Araponga	2284
2913	BR	Brasil	Minas Gerais	MG	Santa Cruz de Salinas	2913
2914	BR	Brasil	Minas Gerais	MG	Santa Cruz do Escalvado	2914
2915	BR	Brasil	Minas Gerais	MG	Santa Efigênia de Minas	2915
2922	BR	Brasil	Minas Gerais	MG	Santa Maria do Salto	2922
2923	BR	Brasil	Minas Gerais	MG	Santa Maria do Suaçuí	2923
2924	BR	Brasil	Minas Gerais	MG	Santana da Vargem	2924
2925	BR	Brasil	Minas Gerais	MG	Santana de Cataguases	2925
2926	BR	Brasil	Minas Gerais	MG	Santana de Pirapama	2926
2927	BR	Brasil	Minas Gerais	MG	Santana do Deserto	2927
2928	BR	Brasil	Minas Gerais	MG	Santana do Garambéu	2928
2929	BR	Brasil	Minas Gerais	MG	Santana do Jacaré	2929
2930	BR	Brasil	Minas Gerais	MG	Santana do Manhuaçu	2930
2931	BR	Brasil	Minas Gerais	MG	Santana do Paraíso	2931
3760	BR	Brasil	São Paulo	SP	Rio Claro	3760
3761	BR	Brasil	São Paulo	SP	Rio Das Pedras	3761
3762	BR	Brasil	São Paulo	SP	Rio Grande da Serra	3762
3763	BR	Brasil	São Paulo	SP	Riolândia	3763
3764	BR	Brasil	São Paulo	SP	Rosana	3764
3765	BR	Brasil	São Paulo	SP	Roseira	3765
3766	BR	Brasil	São Paulo	SP	Rubiácea	3766
3767	BR	Brasil	São Paulo	SP	Rubinéia	3767
3768	BR	Brasil	São Paulo	SP	Sabino	3768
3769	BR	Brasil	São Paulo	SP	Sagres	3769
4131	BR	Brasil	Paraná	PR	Medianeira	4131
1493	BR	Brasil	Pernambuco	PE	Brejo da Madre de Deus	1493
1950	BR	Brasil	Bahia	BA	Elísio Medrado	1950
2355	BR	Brasil	Minas Gerais	MG	Cajuri	2355
2356	BR	Brasil	Minas Gerais	MG	Caldas	2356
2971	BR	Brasil	Minas Gerais	MG	São João da Mata	2971
2972	BR	Brasil	Minas Gerais	MG	São João da Ponte	2972
2973	BR	Brasil	Minas Gerais	MG	São João Das Missões	2973
3815	BR	Brasil	São Paulo	SP	São Francisco	3815
3816	BR	Brasil	São Paulo	SP	São João da Boa Vista	3816
3817	BR	Brasil	São Paulo	SP	São João Das Duas Pontes	3817
3818	BR	Brasil	São Paulo	SP	São João de Iracema	3818
3819	BR	Brasil	São Paulo	SP	São João do Pau D´alho	3819
3820	BR	Brasil	São Paulo	SP	São Joaquim da Barra	3820
3821	BR	Brasil	São Paulo	SP	São José da Bela Vista	3821
3822	BR	Brasil	São Paulo	SP	São José do Barreiro	3822
3823	BR	Brasil	São Paulo	SP	São José do Rio Pardo	3823
3836	BR	Brasil	São Paulo	SP	São Simão	3836
3837	BR	Brasil	São Paulo	SP	São Vicente	3837
3838	BR	Brasil	São Paulo	SP	Sarapuí	3838
3840	BR	Brasil	São Paulo	SP	Sebastianópolis do Sul	3840
3841	BR	Brasil	São Paulo	SP	Serra Azul	3841
3842	BR	Brasil	São Paulo	SP	Serrana	3842
3843	BR	Brasil	São Paulo	SP	Serra Negra	3843
3845	BR	Brasil	São Paulo	SP	Sete Barras	3845
3846	BR	Brasil	São Paulo	SP	Severínia	3846
3847	BR	Brasil	São Paulo	SP	Silveiras	3847
3851	BR	Brasil	São Paulo	SP	Sumaré	3851
3852	BR	Brasil	São Paulo	SP	Suzano	3852
3853	BR	Brasil	São Paulo	SP	Suzanápolis	3853
3854	BR	Brasil	São Paulo	SP	Tabapuã	3854
3855	BR	Brasil	São Paulo	SP	Tabatinga	3855
3856	BR	Brasil	São Paulo	SP	Taboão da Serra	3856
5149	BR	Brasil	Mato Grosso do Sul	MS	Jateí	5149
5150	BR	Brasil	Mato Grosso do Sul	MS	Juti	5150
5154	BR	Brasil	Mato Grosso do Sul	MS	Miranda	5154
5155	BR	Brasil	Mato Grosso do Sul	MS	Mundo Novo	5155
5156	BR	Brasil	Mato Grosso do Sul	MS	Naviraí	5156
5157	BR	Brasil	Mato Grosso do Sul	MS	Nioaque	5157
5158	BR	Brasil	Mato Grosso do Sul	MS	Nova Alvorada do Sul	5158
1601	BR	Brasil	Pernambuco	PE	Sairé	1601
1602	BR	Brasil	Pernambuco	PE	Salgadinho	1602
1658	BR	Brasil	Alagoas	AL	Belém	1658
2066	BR	Brasil	Bahia	BA	Macururé	2066
2067	BR	Brasil	Bahia	BA	Madre de Deus	2067
2068	BR	Brasil	Bahia	BA	Maetinga	2068
2180	BR	Brasil	Bahia	BA	São Domingos	2180
2181	BR	Brasil	Bahia	BA	São Félix	2181
2182	BR	Brasil	Bahia	BA	São Félix do Coribe	2182
2183	BR	Brasil	Bahia	BA	São Felipe	2183
2197	BR	Brasil	Bahia	BA	Senhor do Bonfim	2197
2198	BR	Brasil	Bahia	BA	Serra do Ramalho	2198
2199	BR	Brasil	Bahia	BA	Sento sé	2199
2246	BR	Brasil	Minas Gerais	MG	Abaeté	2246
2247	BR	Brasil	Minas Gerais	MG	Abre Campo	2247
2248	BR	Brasil	Minas Gerais	MG	Acaiaca	2248
2249	BR	Brasil	Minas Gerais	MG	Açucena	2249
2250	BR	Brasil	Minas Gerais	MG	Água Boa	2250
2310	BR	Brasil	Minas Gerais	MG	Belo Horizonte	2310
2311	BR	Brasil	Minas Gerais	MG	Belo Oriente	2311
2312	BR	Brasil	Minas Gerais	MG	Belo Vale	2312
2313	BR	Brasil	Minas Gerais	MG	Berilo	2313
2314	BR	Brasil	Minas Gerais	MG	Bertópolis	2314
2315	BR	Brasil	Minas Gerais	MG	Berizal	2315
2316	BR	Brasil	Minas Gerais	MG	Betim	2316
2317	BR	Brasil	Minas Gerais	MG	Bias Fortes	2317
2318	BR	Brasil	Minas Gerais	MG	Bicas	2318
2319	BR	Brasil	Minas Gerais	MG	Biquinhas	2319
2320	BR	Brasil	Minas Gerais	MG	Boa Esperança	2320
2321	BR	Brasil	Minas Gerais	MG	Bocaina de Minas	2321
2049	BR	Brasil	Bahia	BA	Jussiape	2049
2322	BR	Brasil	Minas Gerais	MG	Bocaiúva	2322
2333	BR	Brasil	Minas Gerais	MG	Borda da Mata	2333
2335	BR	Brasil	Minas Gerais	MG	Botumirim	2335
2336	BR	Brasil	Minas Gerais	MG	Brasilândia de Minas	2336
2337	BR	Brasil	Minas Gerais	MG	Brasília de Minas	2337
2339	BR	Brasil	Minas Gerais	MG	Braúnas	2339
2340	BR	Brasil	Minas Gerais	MG	Brasópolis	2340
2341	BR	Brasil	Minas Gerais	MG	Brumadinho	2341
2342	BR	Brasil	Minas Gerais	MG	Bueno Brandão	2342
2343	BR	Brasil	Minas Gerais	MG	Buenópolis	2343
2344	BR	Brasil	Minas Gerais	MG	Bugre	2344
2346	BR	Brasil	Minas Gerais	MG	Buritizeiro	2346
2347	BR	Brasil	Minas Gerais	MG	Cabeceira Grande	2347
2348	BR	Brasil	Minas Gerais	MG	Cabo Verde	2348
2349	BR	Brasil	Minas Gerais	MG	Cachoeira da Prata	2349
2351	BR	Brasil	Minas Gerais	MG	Cachoeira Dourada	2351
4137	BR	Brasil	Paraná	PR	Morretes	4137
1705	BR	Brasil	Alagoas	AL	Matriz de Camaragibe	1705
2169	BR	Brasil	Bahia	BA	Santaluz	2169
2172	BR	Brasil	Bahia	BA	Santana	2172
2366	BR	Brasil	Minas Gerais	MG	Campo Belo	2366
2367	BR	Brasil	Minas Gerais	MG	Campo do Meio	2367
2368	BR	Brasil	Minas Gerais	MG	Campo Florido	2368
2369	BR	Brasil	Minas Gerais	MG	Campos Altos	2369
2370	BR	Brasil	Minas Gerais	MG	Campos Gerais	2370
2387	BR	Brasil	Minas Gerais	MG	Caranaíba	2387
2389	BR	Brasil	Minas Gerais	MG	Carangola	2389
2390	BR	Brasil	Minas Gerais	MG	Caratinga	2390
2391	BR	Brasil	Minas Gerais	MG	Carbonita	2391
2392	BR	Brasil	Minas Gerais	MG	Careaçu	2392
2394	BR	Brasil	Minas Gerais	MG	Carmésia	2394
2395	BR	Brasil	Minas Gerais	MG	Carmo da Cachoeira	2395
2396	BR	Brasil	Minas Gerais	MG	Carmo da Mata	2396
2397	BR	Brasil	Minas Gerais	MG	Carmo de Minas	2397
2398	BR	Brasil	Minas Gerais	MG	Carmo do Cajuru	2398
2399	BR	Brasil	Minas Gerais	MG	Carmo do Paranaíba	2399
2400	BR	Brasil	Minas Gerais	MG	Carmo do Rio Claro	2400
2401	BR	Brasil	Minas Gerais	MG	Carmópolis de Minas	2401
2402	BR	Brasil	Minas Gerais	MG	Carneirinho	2402
2403	BR	Brasil	Minas Gerais	MG	Carrancas	2403
3908	BR	Brasil	São Paulo	SP	Votorantim	3908
3909	BR	Brasil	São Paulo	SP	Votuporanga	3909
3910	BR	Brasil	São Paulo	SP	Zacarias	3910
3911	BR	Brasil	São Paulo	SP	Chavantes	3911
3912	BR	Brasil	São Paulo	SP	Estiva Gerbi	3912
3913	BR	Brasil	Paraná	PR	Abatiá	3913
3914	BR	Brasil	Paraná	PR	Adrianópolis	3914
3915	BR	Brasil	Paraná	PR	Agudos do Sul	3915
3916	BR	Brasil	Paraná	PR	Almirante Tamandaré	3916
3917	BR	Brasil	Paraná	PR	Altamira do Paraná	3917
3918	BR	Brasil	Paraná	PR	Altônia	3918
3919	BR	Brasil	Paraná	PR	Alto Paraná	3919
3920	BR	Brasil	Paraná	PR	Alto Piquiri	3920
3921	BR	Brasil	Paraná	PR	Alvorada do Sul	3921
3922	BR	Brasil	Paraná	PR	Amaporã	3922
3923	BR	Brasil	Paraná	PR	Ampére	3923
3925	BR	Brasil	Paraná	PR	Andirá	3925
3926	BR	Brasil	Paraná	PR	Ângulo	3926
3927	BR	Brasil	Paraná	PR	Antonina	3927
3928	BR	Brasil	Paraná	PR	Antônio Olinto	3928
3929	BR	Brasil	Paraná	PR	Apucarana	3929
3930	BR	Brasil	Paraná	PR	Arapongas	3930
3931	BR	Brasil	Paraná	PR	Arapoti	3931
3932	BR	Brasil	Paraná	PR	Arapuã	3932
1811	BR	Brasil	Sergipe	SE	Ribeirópolis	1811
1812	BR	Brasil	Sergipe	SE	Rosário do Catete	1812
1813	BR	Brasil	Sergipe	SE	Salgado	1813
1814	BR	Brasil	Sergipe	SE	Santa Luzia do Itanhy	1814
1815	BR	Brasil	Sergipe	SE	Santana do São Francisco	1815
2274	BR	Brasil	Minas Gerais	MG	Andrelândia	2274
2275	BR	Brasil	Minas Gerais	MG	Angelândia	2275
2276	BR	Brasil	Minas Gerais	MG	Antônio Carlos	2276
2277	BR	Brasil	Minas Gerais	MG	Antônio Dias	2277
2278	BR	Brasil	Minas Gerais	MG	Antônio Prado de Minas	2278
2654	BR	Brasil	Minas Gerais	MG	Joanésia	2654
2655	BR	Brasil	Minas Gerais	MG	João Monlevade	2655
2656	BR	Brasil	Minas Gerais	MG	João Pinheiro	2656
2657	BR	Brasil	Minas Gerais	MG	Joaquim Felício	2657
2658	BR	Brasil	Minas Gerais	MG	Jordânia	2658
2659	BR	Brasil	Minas Gerais	MG	José Gonçalves de Minas	2659
2660	BR	Brasil	Minas Gerais	MG	José Raydan	2660
2661	BR	Brasil	Minas Gerais	MG	Josenópolis	2661
2662	BR	Brasil	Minas Gerais	MG	Nova União	2662
2663	BR	Brasil	Minas Gerais	MG	Juatuba	2663
2682	BR	Brasil	Minas Gerais	MG	Leandro Ferreira	2682
2683	BR	Brasil	Minas Gerais	MG	Leme do Prado	2683
2684	BR	Brasil	Minas Gerais	MG	Leopoldina	2684
2685	BR	Brasil	Minas Gerais	MG	Liberdade	2685
2686	BR	Brasil	Minas Gerais	MG	Lima Duarte	2686
2687	BR	Brasil	Minas Gerais	MG	Limeira do Oeste	2687
2688	BR	Brasil	Minas Gerais	MG	Lontra	2688
2773	BR	Brasil	Minas Gerais	MG	Olaria	2773
2774	BR	Brasil	Minas Gerais	MG	Olhos-d´água	2774
2775	BR	Brasil	Minas Gerais	MG	Olímpio Noronha	2775
2776	BR	Brasil	Minas Gerais	MG	Oliveira	2776
2777	BR	Brasil	Minas Gerais	MG	Oliveira Fortes	2777
2778	BR	Brasil	Minas Gerais	MG	Onça de Pitangui	2778
2779	BR	Brasil	Minas Gerais	MG	Oratórios	2779
2780	BR	Brasil	Minas Gerais	MG	Orizânia	2780
2781	BR	Brasil	Minas Gerais	MG	Ouro Branco	2781
2782	BR	Brasil	Minas Gerais	MG	Ouro Fino	2782
2783	BR	Brasil	Minas Gerais	MG	Ouro Preto	2783
2784	BR	Brasil	Minas Gerais	MG	Ouro Verde de Minas	2784
2785	BR	Brasil	Minas Gerais	MG	Padre Carvalho	2785
1912	BR	Brasil	Bahia	BA	Capim Grosso	1912
1913	BR	Brasil	Bahia	BA	Caraíbas	1913
1914	BR	Brasil	Bahia	BA	Caravelas	1914
1915	BR	Brasil	Bahia	BA	Cardeal da Silva	1915
1916	BR	Brasil	Bahia	BA	Carinhanha	1916
1917	BR	Brasil	Bahia	BA	Casa Nova	1917
2359	BR	Brasil	Minas Gerais	MG	Cambuí	2359
2360	BR	Brasil	Minas Gerais	MG	Cambuquira	2360
2361	BR	Brasil	Minas Gerais	MG	Campanário	2361
2362	BR	Brasil	Minas Gerais	MG	Campanha	2362
2363	BR	Brasil	Minas Gerais	MG	Campestre	2363
2374	BR	Brasil	Minas Gerais	MG	Candeias	2374
2731	BR	Brasil	Minas Gerais	MG	Miraí	2731
2732	BR	Brasil	Minas Gerais	MG	Miravânia	2732
2733	BR	Brasil	Minas Gerais	MG	Moeda	2733
2734	BR	Brasil	Minas Gerais	MG	Moema	2734
2735	BR	Brasil	Minas Gerais	MG	Monjolos	2735
2736	BR	Brasil	Minas Gerais	MG	Monsenhor Paulo	2736
2737	BR	Brasil	Minas Gerais	MG	Montalvânia	2737
2738	BR	Brasil	Minas Gerais	MG	Monte Alegre de Minas	2738
2739	BR	Brasil	Minas Gerais	MG	Monte Azul	2739
2740	BR	Brasil	Minas Gerais	MG	Monte Belo	2740
2741	BR	Brasil	Minas Gerais	MG	Monte Carmelo	2741
2841	BR	Brasil	Minas Gerais	MG	Piranguinho	2841
2842	BR	Brasil	Minas Gerais	MG	Pirapetinga	2842
2843	BR	Brasil	Minas Gerais	MG	Pirapora	2843
2844	BR	Brasil	Minas Gerais	MG	Piraúba	2844
2845	BR	Brasil	Minas Gerais	MG	Pitangui	2845
2846	BR	Brasil	Minas Gerais	MG	Piumhi	2846
2847	BR	Brasil	Minas Gerais	MG	Planura	2847
2848	BR	Brasil	Minas Gerais	MG	Poço Fundo	2848
2850	BR	Brasil	Minas Gerais	MG	Pocrane	2850
2851	BR	Brasil	Minas Gerais	MG	Pompéu	2851
2852	BR	Brasil	Minas Gerais	MG	Ponte Nova	2852
2853	BR	Brasil	Minas Gerais	MG	Ponto Chique	2853
2854	BR	Brasil	Minas Gerais	MG	Ponto Dos Volantes	2854
2855	BR	Brasil	Minas Gerais	MG	Porteirinha	2855
2856	BR	Brasil	Minas Gerais	MG	Porto Firme	2856
2857	BR	Brasil	Minas Gerais	MG	Poté	2857
2858	BR	Brasil	Minas Gerais	MG	Pouso Alegre	2858
2859	BR	Brasil	Minas Gerais	MG	Pouso Alto	2859
2860	BR	Brasil	Minas Gerais	MG	Prados	2860
2861	BR	Brasil	Minas Gerais	MG	Prata	2861
2862	BR	Brasil	Minas Gerais	MG	Pratápolis	2862
2864	BR	Brasil	Minas Gerais	MG	Presidente Bernardes	2864
2014	BR	Brasil	Bahia	BA	Itamari	2014
2015	BR	Brasil	Bahia	BA	Itambé	2015
2016	BR	Brasil	Bahia	BA	Itanagra	2016
2017	BR	Brasil	Bahia	BA	Itanhém	2017
2018	BR	Brasil	Bahia	BA	Itaparica	2018
2447	BR	Brasil	Minas Gerais	MG	Conselheiro Pena	2447
2448	BR	Brasil	Minas Gerais	MG	Consolação	2448
2449	BR	Brasil	Minas Gerais	MG	Contagem	2449
2450	BR	Brasil	Minas Gerais	MG	Coqueiral	2450
2796	BR	Brasil	Minas Gerais	MG	Paraguaçu	2796
2797	BR	Brasil	Minas Gerais	MG	Paraisópolis	2797
2798	BR	Brasil	Minas Gerais	MG	Paraopeba	2798
2799	BR	Brasil	Minas Gerais	MG	Passabém	2799
2800	BR	Brasil	Minas Gerais	MG	Passa Quatro	2800
2801	BR	Brasil	Minas Gerais	MG	Passa Tempo	2801
2802	BR	Brasil	Minas Gerais	MG	Passa-vinte	2802
2803	BR	Brasil	Minas Gerais	MG	Passos	2803
2804	BR	Brasil	Minas Gerais	MG	Patis	2804
2873	BR	Brasil	Minas Gerais	MG	Raul Soares	2873
2874	BR	Brasil	Minas Gerais	MG	Recreio	2874
2875	BR	Brasil	Minas Gerais	MG	Reduto	2875
2884	BR	Brasil	Minas Gerais	MG	Rio Casca	2884
2885	BR	Brasil	Minas Gerais	MG	Rio Doce	2885
2886	BR	Brasil	Minas Gerais	MG	Rio do Prado	2886
2887	BR	Brasil	Minas Gerais	MG	Rio Espera	2887
2888	BR	Brasil	Minas Gerais	MG	Rio Manso	2888
2889	BR	Brasil	Minas Gerais	MG	Rio Novo	2889
2890	BR	Brasil	Minas Gerais	MG	Rio Paranaíba	2890
3381	BR	Brasil	São Paulo	SP	Canas	3381
3382	BR	Brasil	São Paulo	SP	Cândido Mota	3382
3383	BR	Brasil	São Paulo	SP	Cândido Rodrigues	3383
3384	BR	Brasil	São Paulo	SP	Canitar	3384
3385	BR	Brasil	São Paulo	SP	Capão Bonito	3385
3386	BR	Brasil	São Paulo	SP	Capela do Alto	3386
3387	BR	Brasil	São Paulo	SP	Capivari	3387
3388	BR	Brasil	São Paulo	SP	Caraguatatuba	3388
3389	BR	Brasil	São Paulo	SP	Carapicuíba	3389
3390	BR	Brasil	São Paulo	SP	Cardoso	3390
3391	BR	Brasil	São Paulo	SP	Casa Branca	3391
3392	BR	Brasil	São Paulo	SP	Cássia Dos Coqueiros	3392
3393	BR	Brasil	São Paulo	SP	Castilho	3393
3394	BR	Brasil	São Paulo	SP	Catanduva	3394
3395	BR	Brasil	São Paulo	SP	Catiguá	3395
3396	BR	Brasil	São Paulo	SP	Cedral	3396
3397	BR	Brasil	São Paulo	SP	Cerqueira César	3397
3967	BR	Brasil	Paraná	PR	Campina do Simão	3967
3969	BR	Brasil	Paraná	PR	Campo Bonito	3969
2117	BR	Brasil	Bahia	BA	Paramirim	2117
2118	BR	Brasil	Bahia	BA	Paratinga	2118
2119	BR	Brasil	Bahia	BA	Paripiranga	2119
2120	BR	Brasil	Bahia	BA	Pau Brasil	2120
2536	BR	Brasil	Minas Gerais	MG	Formoso	2536
2537	BR	Brasil	Minas Gerais	MG	Fortaleza de Minas	2537
2538	BR	Brasil	Minas Gerais	MG	Fortuna de Minas	2538
2539	BR	Brasil	Minas Gerais	MG	Francisco Badaró	2539
2876	BR	Brasil	Minas Gerais	MG	Resende Costa	2876
2877	BR	Brasil	Minas Gerais	MG	Resplendor	2877
2878	BR	Brasil	Minas Gerais	MG	Ressaquinha	2878
2879	BR	Brasil	Minas Gerais	MG	Riachinho	2879
2880	BR	Brasil	Minas Gerais	MG	Riacho Dos Machados	2880
2881	BR	Brasil	Minas Gerais	MG	Ribeirão Das Neves	2881
2882	BR	Brasil	Minas Gerais	MG	Ribeirão Vermelho	2882
2883	BR	Brasil	Minas Gerais	MG	Rio Acima	2883
2932	BR	Brasil	Minas Gerais	MG	Santana do Riacho	2932
2933	BR	Brasil	Minas Gerais	MG	Santana Dos Montes	2933
2943	BR	Brasil	Minas Gerais	MG	Santo Antônio do Aventureiro	2943
2944	BR	Brasil	Minas Gerais	MG	Santo Antônio do Grama	2944
2945	BR	Brasil	Minas Gerais	MG	Santo Antônio do Itambé	2945
2946	BR	Brasil	Minas Gerais	MG	Santo Antônio do Jacinto	2946
2947	BR	Brasil	Minas Gerais	MG	Santo Antônio do Monte	2947
2948	BR	Brasil	Minas Gerais	MG	Santo Antônio do Retiro	2948
2949	BR	Brasil	Minas Gerais	MG	Santo Antônio do Rio Abaixo	2949
2951	BR	Brasil	Minas Gerais	MG	Santos Dumont	2951
2952	BR	Brasil	Minas Gerais	MG	São Bento Abade	2952
3210	BR	Brasil	Rio de Janeiro	RJ	Japeri	3210
3430	BR	Brasil	São Paulo	SP	Echaporã	3430
3431	BR	Brasil	São Paulo	SP	Eldorado	3431
3432	BR	Brasil	São Paulo	SP	Elias Fausto	3432
3433	BR	Brasil	São Paulo	SP	Elisiário	3433
3434	BR	Brasil	São Paulo	SP	Embaúba	3434
3435	BR	Brasil	São Paulo	SP	Embu	3435
3436	BR	Brasil	São Paulo	SP	Embu-guaçu	3436
3437	BR	Brasil	São Paulo	SP	Emilianópolis	3437
3438	BR	Brasil	São Paulo	SP	Engenheiro Coelho	3438
3439	BR	Brasil	São Paulo	SP	Espírito Santo do Pinhal	3439
3453	BR	Brasil	São Paulo	SP	Franca	3453
3454	BR	Brasil	São Paulo	SP	Francisco Morato	3454
3455	BR	Brasil	São Paulo	SP	Franco da Rocha	3455
3456	BR	Brasil	São Paulo	SP	Gabriel Monteiro	3456
3457	BR	Brasil	São Paulo	SP	Gália	3457
3458	BR	Brasil	São Paulo	SP	Garça	3458
3459	BR	Brasil	São Paulo	SP	Gastão Vidigal	3459
3460	BR	Brasil	São Paulo	SP	Gavião Peixoto	3460
2220	BR	Brasil	Bahia	BA	Tremedal	2220
2221	BR	Brasil	Bahia	BA	Tucano	2221
2632	BR	Brasil	Minas Gerais	MG	Itumirim	2632
2633	BR	Brasil	Minas Gerais	MG	Iturama	2633
2953	BR	Brasil	Minas Gerais	MG	São Brás do Suaçuí	2953
2954	BR	Brasil	Minas Gerais	MG	São Domingos Das Dores	2954
2955	BR	Brasil	Minas Gerais	MG	São Domingos do Prata	2955
2956	BR	Brasil	Minas Gerais	MG	São Félix de Minas	2956
2957	BR	Brasil	Minas Gerais	MG	São Francisco	2957
2958	BR	Brasil	Minas Gerais	MG	São Francisco de Paula	2958
2959	BR	Brasil	Minas Gerais	MG	São Francisco de Sales	2959
2960	BR	Brasil	Minas Gerais	MG	São Francisco do Glória	2960
2961	BR	Brasil	Minas Gerais	MG	São Geraldo	2961
2962	BR	Brasil	Minas Gerais	MG	São Geraldo da Piedade	2962
2963	BR	Brasil	Minas Gerais	MG	São Geraldo do Baixio	2963
2964	BR	Brasil	Minas Gerais	MG	São Gonçalo do Abaeté	2964
2965	BR	Brasil	Minas Gerais	MG	São Gonçalo do Pará	2965
2966	BR	Brasil	Minas Gerais	MG	São Gonçalo do Rio Abaixo	2966
2967	BR	Brasil	Minas Gerais	MG	São Gonçalo do Sapucaí	2967
2968	BR	Brasil	Minas Gerais	MG	São Gotardo	2968
2970	BR	Brasil	Minas Gerais	MG	São João da Lagoa	2970
3006	BR	Brasil	Minas Gerais	MG	São Sebastião do Rio Verde	3006
3009	BR	Brasil	Minas Gerais	MG	São Thomé Das Letras	3009
3010	BR	Brasil	Minas Gerais	MG	São Vicente de Minas	3010
3011	BR	Brasil	Minas Gerais	MG	Sapucaí-mirim	3011
3014	BR	Brasil	Minas Gerais	MG	Setubinha	3014
3015	BR	Brasil	Minas Gerais	MG	Sem-peixe	3015
3016	BR	Brasil	Minas Gerais	MG	Senador Amaral	3016
3017	BR	Brasil	Minas Gerais	MG	Senador Cortes	3017
3018	BR	Brasil	Minas Gerais	MG	Senador Firmino	3018
3019	BR	Brasil	Minas Gerais	MG	Senador José Bento	3019
3020	BR	Brasil	Minas Gerais	MG	Senador Modestino Gonçalves	3020
3021	BR	Brasil	Minas Gerais	MG	Senhora de Oliveira	3021
4814	BR	Brasil	Rio Grande do Sul	RS	Ipê	4814
3028	BR	Brasil	Minas Gerais	MG	Serra Dos Aimorés	3028
3029	BR	Brasil	Minas Gerais	MG	Serra do Salitre	3029
3030	BR	Brasil	Minas Gerais	MG	Serrania	3030
3031	BR	Brasil	Minas Gerais	MG	Serranópolis de Minas	3031
3032	BR	Brasil	Minas Gerais	MG	Serranos	3032
3033	BR	Brasil	Minas Gerais	MG	Serro	3033
3034	BR	Brasil	Minas Gerais	MG	Sete Lagoas	3034
3035	BR	Brasil	Minas Gerais	MG	Silveirânia	3035
3036	BR	Brasil	Minas Gerais	MG	Silvianópolis	3036
3037	BR	Brasil	Minas Gerais	MG	Simão Pereira	3037
3038	BR	Brasil	Minas Gerais	MG	Simonésia	3038
3039	BR	Brasil	Minas Gerais	MG	Sobrália	3039
3040	BR	Brasil	Minas Gerais	MG	Soledade de Minas	3040
3045	BR	Brasil	Minas Gerais	MG	Tapiraí	3045
3046	BR	Brasil	Minas Gerais	MG	Taquaraçu de Minas	3046
3047	BR	Brasil	Minas Gerais	MG	Tarumirim	3047
3048	BR	Brasil	Minas Gerais	MG	Teixeiras	3048
3049	BR	Brasil	Minas Gerais	MG	Teófilo Otoni	3049
3050	BR	Brasil	Minas Gerais	MG	Timóteo	3050
3051	BR	Brasil	Minas Gerais	MG	Tiradentes	3051
3052	BR	Brasil	Minas Gerais	MG	Tiros	3052
3053	BR	Brasil	Minas Gerais	MG	Tocantins	3053
3054	BR	Brasil	Minas Gerais	MG	Tocos do Moji	3054
3055	BR	Brasil	Minas Gerais	MG	Toledo	3055
3056	BR	Brasil	Minas Gerais	MG	Tombos	3056
3057	BR	Brasil	Minas Gerais	MG	Três Corações	3057
3058	BR	Brasil	Minas Gerais	MG	Três Marias	3058
3059	BR	Brasil	Minas Gerais	MG	Três Pontas	3059
3060	BR	Brasil	Minas Gerais	MG	Tumiritinga	3060
4009	BR	Brasil	Paraná	PR	Diamante do Sul	4009
4010	BR	Brasil	Paraná	PR	Diamante D´oeste	4010
4011	BR	Brasil	Paraná	PR	Dois Vizinhos	4011
4012	BR	Brasil	Paraná	PR	Douradina	4012
4013	BR	Brasil	Paraná	PR	Doutor Camargo	4013
4014	BR	Brasil	Paraná	PR	Enéas Marques	4014
4019	BR	Brasil	Paraná	PR	Farol	4019
1891	BR	Brasil	Bahia	BA	Caém	1891
1892	BR	Brasil	Bahia	BA	Caetanos	1892
1899	BR	Brasil	Bahia	BA	Camamu	1899
1900	BR	Brasil	Bahia	BA	Campo Alegre de Lourdes	1900
1901	BR	Brasil	Bahia	BA	Campo Formoso	1901
1902	BR	Brasil	Bahia	BA	Canápolis	1902
1903	BR	Brasil	Bahia	BA	Canarana	1903
1904	BR	Brasil	Bahia	BA	Canavieiras	1904
1905	BR	Brasil	Bahia	BA	Candeal	1905
1906	BR	Brasil	Bahia	BA	Candeias	1906
1907	BR	Brasil	Bahia	BA	Candiba	1907
1908	BR	Brasil	Bahia	BA	Cândido Sales	1908
1909	BR	Brasil	Bahia	BA	Cansanção	1909
1910	BR	Brasil	Bahia	BA	Canudos	1910
1911	BR	Brasil	Bahia	BA	Capela do Alto Alegre	1911
1953	BR	Brasil	Bahia	BA	Esplanada	1953
1954	BR	Brasil	Bahia	BA	Euclides da Cunha	1954
1955	BR	Brasil	Bahia	BA	Eunápolis	1955
1956	BR	Brasil	Bahia	BA	Fátima	1956
2428	BR	Brasil	Minas Gerais	MG	Coimbra	2428
2429	BR	Brasil	Minas Gerais	MG	Coluna	2429
2430	BR	Brasil	Minas Gerais	MG	Comendador Gomes	2430
2431	BR	Brasil	Minas Gerais	MG	Comercinho	2431
2432	BR	Brasil	Minas Gerais	MG	Conceição da Aparecida	2432
2833	BR	Brasil	Minas Gerais	MG	Piedade Dos Gerais	2833
2834	BR	Brasil	Minas Gerais	MG	Pimenta	2834
2835	BR	Brasil	Minas Gerais	MG	Pingo-d´água	2835
2836	BR	Brasil	Minas Gerais	MG	Pintópolis	2836
2837	BR	Brasil	Minas Gerais	MG	Piracema	2837
3061	BR	Brasil	Minas Gerais	MG	Tupaciguara	3061
3063	BR	Brasil	Minas Gerais	MG	Turvolândia	3063
3064	BR	Brasil	Minas Gerais	MG	Ubá	3064
3065	BR	Brasil	Minas Gerais	MG	Ubaí	3065
3066	BR	Brasil	Minas Gerais	MG	Ubaporanga	3066
3067	BR	Brasil	Minas Gerais	MG	Uberaba	3067
3068	BR	Brasil	Minas Gerais	MG	Uberlândia	3068
3069	BR	Brasil	Minas Gerais	MG	Umburatiba	3069
3071	BR	Brasil	Minas Gerais	MG	União de Minas	3071
3073	BR	Brasil	Minas Gerais	MG	Urucânia	3073
3074	BR	Brasil	Minas Gerais	MG	Urucuia	3074
3075	BR	Brasil	Minas Gerais	MG	Vargem Alegre	3075
3076	BR	Brasil	Minas Gerais	MG	Vargem Bonita	3076
1992	BR	Brasil	Bahia	BA	Inhambupe	1992
1993	BR	Brasil	Bahia	BA	Ipecaetá	1993
1995	BR	Brasil	Bahia	BA	Ipirá	1995
1996	BR	Brasil	Bahia	BA	Ipupiara	1996
1997	BR	Brasil	Bahia	BA	Irajuba	1997
1998	BR	Brasil	Bahia	BA	Iramaia	1998
1999	BR	Brasil	Bahia	BA	Iraquara	1999
2000	BR	Brasil	Bahia	BA	Irará	2000
2004	BR	Brasil	Bahia	BA	Itabuna	2004
2005	BR	Brasil	Bahia	BA	Itacaré	2005
2006	BR	Brasil	Bahia	BA	Itaeté	2006
2007	BR	Brasil	Bahia	BA	Itagi	2007
2517	BR	Brasil	Minas Gerais	MG	Espírito Santo do Dourado	2517
2518	BR	Brasil	Minas Gerais	MG	Estiva	2518
2519	BR	Brasil	Minas Gerais	MG	Estrela Dalva	2519
2520	BR	Brasil	Minas Gerais	MG	Estrela do Indaiá	2520
2521	BR	Brasil	Minas Gerais	MG	Estrela do Sul	2521
2916	BR	Brasil	Minas Gerais	MG	Santa fé de Minas	2916
2917	BR	Brasil	Minas Gerais	MG	Santa Helena de Minas	2917
2919	BR	Brasil	Minas Gerais	MG	Santa Luzia	2919
2920	BR	Brasil	Minas Gerais	MG	Santa Margarida	2920
2921	BR	Brasil	Minas Gerais	MG	Santa Maria de Itabira	2921
3099	BR	Brasil	Espírito Santo	ES	Águia Branca	3099
3100	BR	Brasil	Espírito Santo	ES	Água Doce do Norte	3100
3101	BR	Brasil	Espírito Santo	ES	Alegre	3101
3102	BR	Brasil	Espírito Santo	ES	Alfredo Chaves	3102
3103	BR	Brasil	Espírito Santo	ES	Alto Rio Novo	3103
3104	BR	Brasil	Espírito Santo	ES	Anchieta	3104
3105	BR	Brasil	Espírito Santo	ES	Apiacá	3105
3106	BR	Brasil	Espírito Santo	ES	Aracruz	3106
3107	BR	Brasil	Espírito Santo	ES	Atilio Vivacqua	3107
3108	BR	Brasil	Espírito Santo	ES	Baixo Guandu	3108
3109	BR	Brasil	Espírito Santo	ES	Barra de São Francisco	3109
3111	BR	Brasil	Espírito Santo	ES	Bom Jesus do Norte	3111
3112	BR	Brasil	Espírito Santo	ES	Brejetuba	3112
3113	BR	Brasil	Espírito Santo	ES	Cachoeiro de Itapemirim	3113
3114	BR	Brasil	Espírito Santo	ES	Cariacica	3114
3115	BR	Brasil	Espírito Santo	ES	Castelo	3115
3116	BR	Brasil	Espírito Santo	ES	Colatina	3116
3117	BR	Brasil	Espírito Santo	ES	Conceição da Barra	3117
3118	BR	Brasil	Espírito Santo	ES	Conceição do Castelo	3118
3119	BR	Brasil	Espírito Santo	ES	Divino de São Lourenço	3119
3120	BR	Brasil	Espírito Santo	ES	Domingos Martins	3120
4976	BR	Brasil	Rio Grande do Sul	RS	Santa Rosa	4976
2008	BR	Brasil	Bahia	BA	Itagibá	2008
2009	BR	Brasil	Bahia	BA	Itagimirim	2009
2010	BR	Brasil	Bahia	BA	Itaguaçu da Bahia	2010
2011	BR	Brasil	Bahia	BA	Itaju do Colônia	2011
2012	BR	Brasil	Bahia	BA	Itajuípe	2012
2013	BR	Brasil	Bahia	BA	Itamaraju	2013
2019	BR	Brasil	Bahia	BA	Itapé	2019
2020	BR	Brasil	Bahia	BA	Itapebi	2020
2021	BR	Brasil	Bahia	BA	Itapetinga	2021
2611	BR	Brasil	Minas Gerais	MG	Itaipé	2611
2612	BR	Brasil	Minas Gerais	MG	Itajubá	2612
2614	BR	Brasil	Minas Gerais	MG	Itamarati de Minas	2614
2615	BR	Brasil	Minas Gerais	MG	Itambacuri	2615
2616	BR	Brasil	Minas Gerais	MG	Itambé do Mato Dentro	2616
2992	BR	Brasil	Minas Gerais	MG	São Lourenço	2992
2993	BR	Brasil	Minas Gerais	MG	São Miguel do Anta	2993
2994	BR	Brasil	Minas Gerais	MG	São Pedro da União	2994
2995	BR	Brasil	Minas Gerais	MG	São Pedro Dos Ferros	2995
2997	BR	Brasil	Minas Gerais	MG	São Romão	2997
3130	BR	Brasil	Espírito Santo	ES	Iconha	3130
3131	BR	Brasil	Espírito Santo	ES	Irupi	3131
3132	BR	Brasil	Espírito Santo	ES	Itaguaçu	3132
3133	BR	Brasil	Espírito Santo	ES	Itapemirim	3133
3134	BR	Brasil	Espírito Santo	ES	Itarana	3134
3135	BR	Brasil	Espírito Santo	ES	Iúna	3135
3136	BR	Brasil	Espírito Santo	ES	Jaguaré	3136
3137	BR	Brasil	Espírito Santo	ES	Jerônimo Monteiro	3137
3138	BR	Brasil	Espírito Santo	ES	João Neiva	3138
3139	BR	Brasil	Espírito Santo	ES	Laranja da Terra	3139
3140	BR	Brasil	Espírito Santo	ES	Linhares	3140
3141	BR	Brasil	Espírito Santo	ES	Mantenópolis	3141
3142	BR	Brasil	Espírito Santo	ES	Marataízes	3142
3143	BR	Brasil	Espírito Santo	ES	Marechal Floriano	3143
3144	BR	Brasil	Espírito Santo	ES	Marilândia	3144
3145	BR	Brasil	Espírito Santo	ES	Mimoso do Sul	3145
3147	BR	Brasil	Espírito Santo	ES	Mucurici	3147
3148	BR	Brasil	Espírito Santo	ES	Muniz Freire	3148
3149	BR	Brasil	Espírito Santo	ES	Muqui	3149
3150	BR	Brasil	Espírito Santo	ES	Nova Venécia	3150
3151	BR	Brasil	Espírito Santo	ES	Pancas	3151
3152	BR	Brasil	Espírito Santo	ES	Pedro Canário	3152
3153	BR	Brasil	Espírito Santo	ES	Pinheiros	3153
3154	BR	Brasil	Espírito Santo	ES	Piúma	3154
3155	BR	Brasil	Espírito Santo	ES	Ponto Belo	3155
4077	BR	Brasil	Paraná	PR	Ivatuba	4077
2022	BR	Brasil	Bahia	BA	Itapicuru	2022
2023	BR	Brasil	Bahia	BA	Itapitanga	2023
2024	BR	Brasil	Bahia	BA	Itaquara	2024
2025	BR	Brasil	Bahia	BA	Itarantim	2025
2087	BR	Brasil	Bahia	BA	Monte Santo	2087
2088	BR	Brasil	Bahia	BA	Morpará	2088
2089	BR	Brasil	Bahia	BA	Morro do Chapéu	2089
2090	BR	Brasil	Bahia	BA	Mortugaba	2090
2091	BR	Brasil	Bahia	BA	Mucugê	2091
2092	BR	Brasil	Bahia	BA	Mucuri	2092
2093	BR	Brasil	Bahia	BA	Mulungu do Morro	2093
2094	BR	Brasil	Bahia	BA	Mundo Novo	2094
2095	BR	Brasil	Bahia	BA	Muniz Ferreira	2095
2096	BR	Brasil	Bahia	BA	Muquém de São Francisco	2096
2097	BR	Brasil	Bahia	BA	Muritiba	2097
2098	BR	Brasil	Bahia	BA	Mutuípe	2098
2099	BR	Brasil	Bahia	BA	Nazaré	2099
2100	BR	Brasil	Bahia	BA	Nilo Peçanha	2100
2101	BR	Brasil	Bahia	BA	Nordestina	2101
2102	BR	Brasil	Bahia	BA	Nova Canaã	2102
2103	BR	Brasil	Bahia	BA	Nova Fátima	2103
2104	BR	Brasil	Bahia	BA	Nova Ibiá	2104
2105	BR	Brasil	Bahia	BA	Nova Itarana	2105
2106	BR	Brasil	Bahia	BA	Nova Redenção	2106
2107	BR	Brasil	Bahia	BA	Nova Soure	2107
2703	BR	Brasil	Minas Gerais	MG	Mar de Espanha	2703
2704	BR	Brasil	Minas Gerais	MG	Maria da fé	2704
2705	BR	Brasil	Minas Gerais	MG	Mariana	2705
2706	BR	Brasil	Minas Gerais	MG	Marilac	2706
2707	BR	Brasil	Minas Gerais	MG	Mário Campos	2707
3077	BR	Brasil	Minas Gerais	MG	Vargem Grande do Rio Pardo	3077
3079	BR	Brasil	Minas Gerais	MG	Varjão de Minas	3079
3080	BR	Brasil	Minas Gerais	MG	Várzea da Palma	3080
3081	BR	Brasil	Minas Gerais	MG	Varzelândia	3081
3165	BR	Brasil	Espírito Santo	ES	São Mateus	3165
3166	BR	Brasil	Espírito Santo	ES	São Roque do Canaã	3166
3168	BR	Brasil	Espírito Santo	ES	Sooretama	3168
3169	BR	Brasil	Espírito Santo	ES	Vargem Alta	3169
3170	BR	Brasil	Espírito Santo	ES	Venda Nova do Imigrante	3170
4095	BR	Brasil	Paraná	PR	Lapa	4095
4309	BR	Brasil	Paraná	PR	Virmond	4309
2109	BR	Brasil	Bahia	BA	Novo Horizonte	2109
3062	BR	Brasil	Minas Gerais	MG	Turmalina	3062
3072	BR	Brasil	Minas Gerais	MG	Uruana de Minas	3072
3078	BR	Brasil	Minas Gerais	MG	Varginha	3078
3183	BR	Brasil	Rio de Janeiro	RJ	Barra Mansa	3183
3184	BR	Brasil	Rio de Janeiro	RJ	Belford Roxo	3184
3185	BR	Brasil	Rio de Janeiro	RJ	Bom Jardim	3185
3186	BR	Brasil	Rio de Janeiro	RJ	Bom Jesus do Itabapoana	3186
3187	BR	Brasil	Rio de Janeiro	RJ	Cabo Frio	3187
3188	BR	Brasil	Rio de Janeiro	RJ	Cachoeiras de Macacu	3188
3189	BR	Brasil	Rio de Janeiro	RJ	Cambuci	3189
3190	BR	Brasil	Rio de Janeiro	RJ	Carapebus	3190
3191	BR	Brasil	Rio de Janeiro	RJ	Comendador Levy Gasparian	3191
3202	BR	Brasil	Rio de Janeiro	RJ	Guapimirim	3202
3203	BR	Brasil	Rio de Janeiro	RJ	Iguaba Grande	3203
3204	BR	Brasil	Rio de Janeiro	RJ	Itaboraí	3204
3205	BR	Brasil	Rio de Janeiro	RJ	Itaguaí	3205
3206	BR	Brasil	Rio de Janeiro	RJ	Italva	3206
3207	BR	Brasil	Rio de Janeiro	RJ	Itaocara	3207
3208	BR	Brasil	Rio de Janeiro	RJ	Itaperuna	3208
3209	BR	Brasil	Rio de Janeiro	RJ	Itatiaia	3209
3211	BR	Brasil	Rio de Janeiro	RJ	Laje do Muriaé	3211
3212	BR	Brasil	Rio de Janeiro	RJ	Macaé	3212
3213	BR	Brasil	Rio de Janeiro	RJ	Macuco	3213
3214	BR	Brasil	Rio de Janeiro	RJ	Magé	3214
3215	BR	Brasil	Rio de Janeiro	RJ	Mangaratiba	3215
3216	BR	Brasil	Rio de Janeiro	RJ	Maricá	3216
3217	BR	Brasil	Rio de Janeiro	RJ	Mendes	3217
3218	BR	Brasil	Rio de Janeiro	RJ	Mesquita	3218
3219	BR	Brasil	Rio de Janeiro	RJ	Miguel Pereira	3219
3220	BR	Brasil	Rio de Janeiro	RJ	Miracema	3220
3221	BR	Brasil	Rio de Janeiro	RJ	Natividade	3221
3222	BR	Brasil	Rio de Janeiro	RJ	Nilópolis	3222
3223	BR	Brasil	Rio de Janeiro	RJ	Niterói	3223
3224	BR	Brasil	Rio de Janeiro	RJ	Nova Friburgo	3224
3225	BR	Brasil	Rio de Janeiro	RJ	Nova Iguaçu	3225
3226	BR	Brasil	Rio de Janeiro	RJ	Paracambi	3226
3227	BR	Brasil	Rio de Janeiro	RJ	Paraíba do Sul	3227
3228	BR	Brasil	Rio de Janeiro	RJ	Parati	3228
3229	BR	Brasil	Rio de Janeiro	RJ	Paty do Alferes	3229
3230	BR	Brasil	Rio de Janeiro	RJ	Petrópolis	3230
3231	BR	Brasil	Rio de Janeiro	RJ	Pinheiral	3231
3232	BR	Brasil	Rio de Janeiro	RJ	Piraí	3232
3233	BR	Brasil	Rio de Janeiro	RJ	Porciúncula	3233
3234	BR	Brasil	Rio de Janeiro	RJ	Porto Real	3234
3235	BR	Brasil	Rio de Janeiro	RJ	Quatis	3235
3236	BR	Brasil	Rio de Janeiro	RJ	Queimados	3236
2110	BR	Brasil	Bahia	BA	Novo Triunfo	2110
3157	BR	Brasil	Espírito Santo	ES	Rio Bananal	3157
3239	BR	Brasil	Rio de Janeiro	RJ	Rio Bonito	3239
3243	BR	Brasil	Rio de Janeiro	RJ	Rio de Janeiro	3243
3244	BR	Brasil	Rio de Janeiro	RJ	Santa Maria Madalena	3244
3245	BR	Brasil	Rio de Janeiro	RJ	Santo Antônio de Pádua	3245
3246	BR	Brasil	Rio de Janeiro	RJ	São Francisco de Itabapoana	3246
3247	BR	Brasil	Rio de Janeiro	RJ	São Fidélis	3247
3248	BR	Brasil	Rio de Janeiro	RJ	São Gonçalo	3248
3249	BR	Brasil	Rio de Janeiro	RJ	São João da Barra	3249
3250	BR	Brasil	Rio de Janeiro	RJ	São João de Meriti	3250
3251	BR	Brasil	Rio de Janeiro	RJ	São José de Ubá	3251
3252	BR	Brasil	Rio de Janeiro	RJ	São José do Vale do Rio Preto	3252
3253	BR	Brasil	Rio de Janeiro	RJ	São Pedro da Aldeia	3253
3254	BR	Brasil	Rio de Janeiro	RJ	São Sebastião do Alto	3254
3255	BR	Brasil	Rio de Janeiro	RJ	Sapucaia	3255
3256	BR	Brasil	Rio de Janeiro	RJ	Saquarema	3256
3257	BR	Brasil	Rio de Janeiro	RJ	Seropédica	3257
3258	BR	Brasil	Rio de Janeiro	RJ	Silva Jardim	3258
3259	BR	Brasil	Rio de Janeiro	RJ	Sumidouro	3259
3260	BR	Brasil	Rio de Janeiro	RJ	Tanguá	3260
3261	BR	Brasil	Rio de Janeiro	RJ	Teresópolis	3261
3262	BR	Brasil	Rio de Janeiro	RJ	Trajano de Morais	3262
3263	BR	Brasil	Rio de Janeiro	RJ	Três Rios	3263
3264	BR	Brasil	Rio de Janeiro	RJ	Valença	3264
3265	BR	Brasil	Rio de Janeiro	RJ	Varre-sai	3265
3266	BR	Brasil	Rio de Janeiro	RJ	Vassouras	3266
3267	BR	Brasil	Rio de Janeiro	RJ	Volta Redonda	3267
3268	BR	Brasil	São Paulo	SP	Adamantina	3268
3269	BR	Brasil	São Paulo	SP	Adolfo	3269
3270	BR	Brasil	São Paulo	SP	Aguaí	3270
3271	BR	Brasil	São Paulo	SP	Águas da Prata	3271
3272	BR	Brasil	São Paulo	SP	Águas de Lindóia	3272
3273	BR	Brasil	São Paulo	SP	Águas de Santa Bárbara	3273
3274	BR	Brasil	São Paulo	SP	Águas de São Pedro	3274
3275	BR	Brasil	São Paulo	SP	Agudos	3275
3276	BR	Brasil	São Paulo	SP	Alambari	3276
3277	BR	Brasil	São Paulo	SP	Alfredo Marcondes	3277
3278	BR	Brasil	São Paulo	SP	Altair	3278
3279	BR	Brasil	São Paulo	SP	Altinópolis	3279
3280	BR	Brasil	São Paulo	SP	Alto Alegre	3280
3281	BR	Brasil	São Paulo	SP	Alumínio	3281
3282	BR	Brasil	São Paulo	SP	Álvares Florence	3282
3283	BR	Brasil	São Paulo	SP	Álvares Machado	3283
3284	BR	Brasil	São Paulo	SP	Álvaro de Carvalho	3284
3285	BR	Brasil	São Paulo	SP	Alvinlândia	3285
911	BR	Brasil	Ceará	CE	Aurora	911
1178	BR	Brasil	Rio Grande do Norte	RN	Pau Dos Ferros	1178
1239	BR	Brasil	Rio Grande do Norte	RN	Venha-ver	1239
1240	BR	Brasil	Rio Grande do Norte	RN	Vera Cruz	1240
1241	BR	Brasil	Rio Grande do Norte	RN	Viçosa	1241
1242	BR	Brasil	Rio Grande do Norte	RN	Vila Flor	1242
1580	BR	Brasil	Pernambuco	PE	Palmares	1580
1581	BR	Brasil	Pernambuco	PE	Palmeirina	1581
1582	BR	Brasil	Pernambuco	PE	Panelas	1582
1583	BR	Brasil	Pernambuco	PE	Paranatama	1583
1584	BR	Brasil	Pernambuco	PE	Parnamirim	1584
2123	BR	Brasil	Bahia	BA	Pedrão	2123
2167	BR	Brasil	Bahia	BA	Santa Cruz da Vitória	2167
2170	BR	Brasil	Bahia	BA	Santa Luzia	2170
2171	BR	Brasil	Bahia	BA	Santa Maria da Vitória	2171
2173	BR	Brasil	Bahia	BA	Santanópolis	2173
2174	BR	Brasil	Bahia	BA	Santa Rita de Cássia	2174
2175	BR	Brasil	Bahia	BA	Santa Teresinha	2175
2176	BR	Brasil	Bahia	BA	Santo Amaro	2176
2177	BR	Brasil	Bahia	BA	Santo Antônio de Jesus	2177
2178	BR	Brasil	Bahia	BA	Santo Estêvão	2178
2179	BR	Brasil	Bahia	BA	São Desidério	2179
3287	BR	Brasil	São Paulo	SP	Américo Brasiliense	3287
3288	BR	Brasil	São Paulo	SP	Américo de Campos	3288
3289	BR	Brasil	São Paulo	SP	Amparo	3289
3290	BR	Brasil	São Paulo	SP	Analândia	3290
3291	BR	Brasil	São Paulo	SP	Andradina	3291
3292	BR	Brasil	São Paulo	SP	Angatuba	3292
3293	BR	Brasil	São Paulo	SP	Anhembi	3293
3294	BR	Brasil	São Paulo	SP	Anhumas	3294
3295	BR	Brasil	São Paulo	SP	Aparecida	3295
3296	BR	Brasil	São Paulo	SP	Aparecida D´oeste	3296
3297	BR	Brasil	São Paulo	SP	Apiaí	3297
3298	BR	Brasil	São Paulo	SP	Araçariguama	3298
3299	BR	Brasil	São Paulo	SP	Araçatuba	3299
3300	BR	Brasil	São Paulo	SP	Araçoiaba da Serra	3300
3301	BR	Brasil	São Paulo	SP	Aramina	3301
3302	BR	Brasil	São Paulo	SP	Arandu	3302
3303	BR	Brasil	São Paulo	SP	Arapeí	3303
3304	BR	Brasil	São Paulo	SP	Araraquara	3304
3305	BR	Brasil	São Paulo	SP	Araras	3305
3306	BR	Brasil	São Paulo	SP	Arco-íris	3306
3307	BR	Brasil	São Paulo	SP	Arealva	3307
3308	BR	Brasil	São Paulo	SP	Areias	3308
4404	BR	Brasil	Santa Catarina	SC	Galvão	4404
5012	BR	Brasil	Rio Grande do Sul	RS	São Nicolau	5012
1804	BR	Brasil	Sergipe	SE	Pirambu	1804
1805	BR	Brasil	Sergipe	SE	Poço Redondo	1805
1806	BR	Brasil	Sergipe	SE	Poço Verde	1806
1807	BR	Brasil	Sergipe	SE	Porto da Folha	1807
1808	BR	Brasil	Sergipe	SE	Propriá	1808
1809	BR	Brasil	Sergipe	SE	Riachão do Dantas	1809
1810	BR	Brasil	Sergipe	SE	Riachuelo	1810
1816	BR	Brasil	Sergipe	SE	Santa Rosa de Lima	1816
1827	BR	Brasil	Sergipe	SE	Umbaúba	1827
1828	BR	Brasil	Bahia	BA	Abaíra	1828
1829	BR	Brasil	Bahia	BA	Abaré	1829
1830	BR	Brasil	Bahia	BA	Acajutiba	1830
1831	BR	Brasil	Bahia	BA	Adustina	1831
1832	BR	Brasil	Bahia	BA	Água Fria	1832
1833	BR	Brasil	Bahia	BA	Érico Cardoso	1833
1834	BR	Brasil	Bahia	BA	Aiquara	1834
1835	BR	Brasil	Bahia	BA	Alagoinhas	1835
1836	BR	Brasil	Bahia	BA	Alcobaça	1836
1837	BR	Brasil	Bahia	BA	Almadina	1837
1838	BR	Brasil	Bahia	BA	Amargosa	1838
1839	BR	Brasil	Bahia	BA	Amélia Rodrigues	1839
1840	BR	Brasil	Bahia	BA	América Dourada	1840
1841	BR	Brasil	Bahia	BA	Anagé	1841
1842	BR	Brasil	Bahia	BA	Andaraí	1842
1843	BR	Brasil	Bahia	BA	Andorinha	1843
1844	BR	Brasil	Bahia	BA	Angical	1844
2372	BR	Brasil	Minas Gerais	MG	Canápolis	2372
2373	BR	Brasil	Minas Gerais	MG	Cana Verde	2373
2375	BR	Brasil	Minas Gerais	MG	Cantagalo	2375
2376	BR	Brasil	Minas Gerais	MG	Caparaó	2376
2377	BR	Brasil	Minas Gerais	MG	Capela Nova	2377
2378	BR	Brasil	Minas Gerais	MG	Capelinha	2378
2379	BR	Brasil	Minas Gerais	MG	Capetinga	2379
2380	BR	Brasil	Minas Gerais	MG	Capim Branco	2380
2382	BR	Brasil	Minas Gerais	MG	Capitão Andrade	2382
2383	BR	Brasil	Minas Gerais	MG	Capitão Enéas	2383
2384	BR	Brasil	Minas Gerais	MG	Capitólio	2384
2385	BR	Brasil	Minas Gerais	MG	Caputira	2385
2386	BR	Brasil	Minas Gerais	MG	Caraí	2386
2388	BR	Brasil	Minas Gerais	MG	Carandaí	2388
4129	BR	Brasil	Paraná	PR	Mato Rico	4129
1845	BR	Brasil	Bahia	BA	Anguera	1845
1846	BR	Brasil	Bahia	BA	Antas	1846
1851	BR	Brasil	Bahia	BA	Aracatu	1851
1852	BR	Brasil	Bahia	BA	Araças	1852
1853	BR	Brasil	Bahia	BA	Araci	1853
1854	BR	Brasil	Bahia	BA	Aramari	1854
1855	BR	Brasil	Bahia	BA	Arataca	1855
1856	BR	Brasil	Bahia	BA	Aratuípe	1856
1857	BR	Brasil	Bahia	BA	Aurelino Leal	1857
2498	BR	Brasil	Minas Gerais	MG	Dom Silvério	2498
2503	BR	Brasil	Minas Gerais	MG	Dores do Indaiá	2503
2504	BR	Brasil	Minas Gerais	MG	Dores do Turvo	2504
2505	BR	Brasil	Minas Gerais	MG	Doresópolis	2505
2506	BR	Brasil	Minas Gerais	MG	Douradoquara	2506
2508	BR	Brasil	Minas Gerais	MG	Elói Mendes	2508
2509	BR	Brasil	Minas Gerais	MG	Engenheiro Caldas	2509
3374	BR	Brasil	São Paulo	SP	Cajuru	3374
3376	BR	Brasil	São Paulo	SP	Campinas	3376
3377	BR	Brasil	São Paulo	SP	Campo Limpo Paulista	3377
3378	BR	Brasil	São Paulo	SP	Campos do Jordão	3378
3379	BR	Brasil	São Paulo	SP	Campos Novos Paulista	3379
3380	BR	Brasil	São Paulo	SP	Cananéia	3380
3398	BR	Brasil	São Paulo	SP	Cerquilho	3398
3399	BR	Brasil	São Paulo	SP	Cesário Lange	3399
3400	BR	Brasil	São Paulo	SP	Charqueada	3400
3401	BR	Brasil	São Paulo	SP	Clementina	3401
3402	BR	Brasil	São Paulo	SP	Colina	3402
3403	BR	Brasil	São Paulo	SP	Colômbia	3403
3404	BR	Brasil	São Paulo	SP	Conchal	3404
3405	BR	Brasil	São Paulo	SP	Conchas	3405
3406	BR	Brasil	São Paulo	SP	Cordeirópolis	3406
4818	BR	Brasil	Rio Grande do Sul	RS	Itacurubi	4818
1957	BR	Brasil	Bahia	BA	Feira da Mata	1957
1958	BR	Brasil	Bahia	BA	Feira de Santana	1958
1959	BR	Brasil	Bahia	BA	Filadélfia	1959
1960	BR	Brasil	Bahia	BA	Firmino Alves	1960
1961	BR	Brasil	Bahia	BA	Floresta Azul	1961
1962	BR	Brasil	Bahia	BA	Formosa do Rio Preto	1962
1972	BR	Brasil	Bahia	BA	Heliópolis	1972
1973	BR	Brasil	Bahia	BA	Iaçu	1973
1974	BR	Brasil	Bahia	BA	Ibiassucê	1974
1975	BR	Brasil	Bahia	BA	Ibicaraí	1975
1976	BR	Brasil	Bahia	BA	Ibicoara	1976
1977	BR	Brasil	Bahia	BA	Ibicuí	1977
1978	BR	Brasil	Bahia	BA	Ibipeba	1978
1979	BR	Brasil	Bahia	BA	Ibipitanga	1979
1980	BR	Brasil	Bahia	BA	Ibiquera	1980
1981	BR	Brasil	Bahia	BA	Ibirapitanga	1981
1982	BR	Brasil	Bahia	BA	Ibirapuã	1982
1983	BR	Brasil	Bahia	BA	Ibirataia	1983
1984	BR	Brasil	Bahia	BA	Ibitiara	1984
1985	BR	Brasil	Bahia	BA	Ibititá	1985
1986	BR	Brasil	Bahia	BA	Ibotirama	1986
1987	BR	Brasil	Bahia	BA	Ichu	1987
1988	BR	Brasil	Bahia	BA	Igaporã	1988
1989	BR	Brasil	Bahia	BA	Igrapiúna	1989
1990	BR	Brasil	Bahia	BA	Iguaí	1990
1991	BR	Brasil	Bahia	BA	Ilhéus	1991
1994	BR	Brasil	Bahia	BA	Ipiaú	1994
2689	BR	Brasil	Minas Gerais	MG	Luisburgo	2689
2690	BR	Brasil	Minas Gerais	MG	Luislândia	2690
2691	BR	Brasil	Minas Gerais	MG	Luminárias	2691
2692	BR	Brasil	Minas Gerais	MG	Luz	2692
2693	BR	Brasil	Minas Gerais	MG	Machacalis	2693
2694	BR	Brasil	Minas Gerais	MG	Machado	2694
2695	BR	Brasil	Minas Gerais	MG	Madre de Deus de Minas	2695
2696	BR	Brasil	Minas Gerais	MG	Malacacheta	2696
2697	BR	Brasil	Minas Gerais	MG	Mamonas	2697
2698	BR	Brasil	Minas Gerais	MG	Manga	2698
2699	BR	Brasil	Minas Gerais	MG	Manhuaçu	2699
2700	BR	Brasil	Minas Gerais	MG	Manhumirim	2700
2701	BR	Brasil	Minas Gerais	MG	Mantena	2701
2702	BR	Brasil	Minas Gerais	MG	Maravilhas	2702
2708	BR	Brasil	Minas Gerais	MG	Maripá de Minas	2708
2709	BR	Brasil	Minas Gerais	MG	Marliéria	2709
2710	BR	Brasil	Minas Gerais	MG	Marmelópolis	2710
2711	BR	Brasil	Minas Gerais	MG	Martinho Campos	2711
2712	BR	Brasil	Minas Gerais	MG	Martins Soares	2712
4994	BR	Brasil	Rio Grande do Sul	RS	São João da Urtiga	4994
2026	BR	Brasil	Bahia	BA	Itatim	2026
2027	BR	Brasil	Bahia	BA	Itiruçu	2027
2028	BR	Brasil	Bahia	BA	Itiúba	2028
2029	BR	Brasil	Bahia	BA	Itororó	2029
2030	BR	Brasil	Bahia	BA	Ituaçu	2030
2031	BR	Brasil	Bahia	BA	Ituberá	2031
2032	BR	Brasil	Bahia	BA	Iuiú	2032
2033	BR	Brasil	Bahia	BA	Jaborandi	2033
2034	BR	Brasil	Bahia	BA	Jacaraci	2034
2035	BR	Brasil	Bahia	BA	Jacobina	2035
2036	BR	Brasil	Bahia	BA	Jaguaquara	2036
2037	BR	Brasil	Bahia	BA	Jaguarari	2037
2038	BR	Brasil	Bahia	BA	Jaguaripe	2038
2039	BR	Brasil	Bahia	BA	Jandaíra	2039
2040	BR	Brasil	Bahia	BA	Jequié	2040
2041	BR	Brasil	Bahia	BA	Jeremoabo	2041
2042	BR	Brasil	Bahia	BA	Jiquiriçá	2042
2043	BR	Brasil	Bahia	BA	Jitaúna	2043
2044	BR	Brasil	Bahia	BA	João Dourado	2044
2046	BR	Brasil	Bahia	BA	Jucuruçu	2046
2047	BR	Brasil	Bahia	BA	Jussara	2047
2048	BR	Brasil	Bahia	BA	Jussari	2048
2713	BR	Brasil	Minas Gerais	MG	Mata Verde	2713
2714	BR	Brasil	Minas Gerais	MG	Materlândia	2714
2756	BR	Brasil	Minas Gerais	MG	Naque	2756
2757	BR	Brasil	Minas Gerais	MG	Natalândia	2757
2758	BR	Brasil	Minas Gerais	MG	Natércia	2758
2759	BR	Brasil	Minas Gerais	MG	Nazareno	2759
2760	BR	Brasil	Minas Gerais	MG	Nepomuceno	2760
2761	BR	Brasil	Minas Gerais	MG	Ninheira	2761
2762	BR	Brasil	Minas Gerais	MG	Nova Belém	2762
2763	BR	Brasil	Minas Gerais	MG	Nova Era	2763
2764	BR	Brasil	Minas Gerais	MG	Nova Lima	2764
2765	BR	Brasil	Minas Gerais	MG	Nova Módica	2765
2766	BR	Brasil	Minas Gerais	MG	Nova Ponte	2766
2767	BR	Brasil	Minas Gerais	MG	Nova Porteirinha	2767
2768	BR	Brasil	Minas Gerais	MG	Nova Resende	2768
2769	BR	Brasil	Minas Gerais	MG	Nova Serrana	2769
2770	BR	Brasil	Minas Gerais	MG	Novo Cruzeiro	2770
2771	BR	Brasil	Minas Gerais	MG	Novo Oriente de Minas	2771
2772	BR	Brasil	Minas Gerais	MG	Novorizonte	2772
4425	BR	Brasil	Santa Catarina	SC	Indaial	4425
4550	BR	Brasil	Santa Catarina	SC	São Bonifácio	4550
5151	BR	Brasil	Mato Grosso do Sul	MS	Ladário	5151
5152	BR	Brasil	Mato Grosso do Sul	MS	Laguna Carapã	5152
5153	BR	Brasil	Mato Grosso do Sul	MS	Maracaju	5153
912	BR	Brasil	Ceará	CE	Baixio	912
913	BR	Brasil	Ceará	CE	Banabuiú	913
914	BR	Brasil	Ceará	CE	Barbalha	914
915	BR	Brasil	Ceará	CE	Barreira	915
918	BR	Brasil	Ceará	CE	Baturité	918
951	BR	Brasil	Ceará	CE	Fortim	951
952	BR	Brasil	Ceará	CE	Frecheirinha	952
953	BR	Brasil	Ceará	CE	General Sampaio	953
954	BR	Brasil	Ceará	CE	Graça	954
955	BR	Brasil	Ceará	CE	Granja	955
956	BR	Brasil	Ceará	CE	Granjeiro	956
957	BR	Brasil	Ceará	CE	Groaíras	957
958	BR	Brasil	Ceará	CE	Guaiúba	958
970	BR	Brasil	Ceará	CE	Ipaporanga	970
971	BR	Brasil	Ceará	CE	Ipaumirim	971
972	BR	Brasil	Ceará	CE	Ipu	972
973	BR	Brasil	Ceará	CE	Ipueiras	973
974	BR	Brasil	Ceará	CE	Iracema	974
975	BR	Brasil	Ceará	CE	Irauçuba	975
976	BR	Brasil	Ceará	CE	Itaiçaba	976
2050	BR	Brasil	Bahia	BA	Lafaiete Coutinho	2050
2051	BR	Brasil	Bahia	BA	Lagoa Real	2051
2052	BR	Brasil	Bahia	BA	Laje	2052
2053	BR	Brasil	Bahia	BA	Lajedão	2053
2054	BR	Brasil	Bahia	BA	Lajedinho	2054
2055	BR	Brasil	Bahia	BA	Lajedo do Tabocal	2055
2056	BR	Brasil	Bahia	BA	Lamarão	2056
2057	BR	Brasil	Bahia	BA	Lapão	2057
2058	BR	Brasil	Bahia	BA	Lauro de Freitas	2058
2059	BR	Brasil	Bahia	BA	Lençóis	2059
2060	BR	Brasil	Bahia	BA	Licínio de Almeida	2060
2061	BR	Brasil	Bahia	BA	Livramento de Nossa Senhora	2061
2062	BR	Brasil	Bahia	BA	Luís Eduardo Magalhães	2062
2063	BR	Brasil	Bahia	BA	Macajuba	2063
2064	BR	Brasil	Bahia	BA	Macarani	2064
2065	BR	Brasil	Bahia	BA	Macaúbas	2065
2081	BR	Brasil	Bahia	BA	Matina	2081
2082	BR	Brasil	Bahia	BA	Medeiros Neto	2082
2083	BR	Brasil	Bahia	BA	Miguel Calmon	2083
2084	BR	Brasil	Bahia	BA	Milagres	2084
2085	BR	Brasil	Bahia	BA	Mirangaba	2085
2086	BR	Brasil	Bahia	BA	Mirante	2086
977	BR	Brasil	Ceará	CE	Itaitinga	977
978	BR	Brasil	Ceará	CE	Itapagé	978
1008	BR	Brasil	Ceará	CE	Morada Nova	1008
1009	BR	Brasil	Ceará	CE	Moraújo	1009
1010	BR	Brasil	Ceará	CE	Morrinhos	1010
1011	BR	Brasil	Ceará	CE	Mucambo	1011
1012	BR	Brasil	Ceará	CE	Mulungu	1012
1013	BR	Brasil	Ceará	CE	Nova Olinda	1013
1014	BR	Brasil	Ceará	CE	Nova Russas	1014
1015	BR	Brasil	Ceará	CE	Novo Oriente	1015
1016	BR	Brasil	Ceará	CE	Ocara	1016
1017	BR	Brasil	Ceará	CE	Orós	1017
1018	BR	Brasil	Ceará	CE	Pacajus	1018
1019	BR	Brasil	Ceará	CE	Pacatuba	1019
1020	BR	Brasil	Ceará	CE	Pacoti	1020
1021	BR	Brasil	Ceará	CE	Pacujá	1021
1022	BR	Brasil	Ceará	CE	Palhano	1022
1023	BR	Brasil	Ceará	CE	Palmácia	1023
1024	BR	Brasil	Ceará	CE	Paracuru	1024
1025	BR	Brasil	Ceará	CE	Paraipaba	1025
1026	BR	Brasil	Ceará	CE	Parambu	1026
1027	BR	Brasil	Ceará	CE	Paramoti	1027
1028	BR	Brasil	Ceará	CE	Pedra Branca	1028
1029	BR	Brasil	Ceará	CE	Penaforte	1029
1033	BR	Brasil	Ceará	CE	Piquet Carneiro	1033
1034	BR	Brasil	Ceará	CE	Pires Ferreira	1034
1035	BR	Brasil	Ceará	CE	Poranga	1035
1036	BR	Brasil	Ceará	CE	Porteiras	1036
1037	BR	Brasil	Ceará	CE	Potengi	1037
1038	BR	Brasil	Ceará	CE	Potiretama	1038
1064	BR	Brasil	Ceará	CE	Tejuçuoca	1064
1065	BR	Brasil	Ceará	CE	Tianguá	1065
1066	BR	Brasil	Ceará	CE	Trairi	1066
1067	BR	Brasil	Ceará	CE	Tururu	1067
1068	BR	Brasil	Ceará	CE	Ubajara	1068
1069	BR	Brasil	Ceará	CE	Umari	1069
2108	BR	Brasil	Bahia	BA	Nova Viçosa	2108
4588	BR	Brasil	Santa Catarina	SC	Tubarão	4588
1075	BR	Brasil	Ceará	CE	Viçosa do Ceará	1075
1076	BR	Brasil	Rio Grande do Norte	RN	Acari	1076
1077	BR	Brasil	Rio Grande do Norte	RN	Açu	1077
1080	BR	Brasil	Rio Grande do Norte	RN	Alexandria	1080
1081	BR	Brasil	Rio Grande do Norte	RN	Almino Afonso	1081
1082	BR	Brasil	Rio Grande do Norte	RN	Alto do Rodrigues	1082
1084	BR	Brasil	Rio Grande do Norte	RN	Antônio Martins	1084
1085	BR	Brasil	Rio Grande do Norte	RN	Apodi	1085
1086	BR	Brasil	Rio Grande do Norte	RN	Areia Branca	1086
1154	BR	Brasil	Rio Grande do Norte	RN	Macau	1154
1155	BR	Brasil	Rio Grande do Norte	RN	Major Sales	1155
1156	BR	Brasil	Rio Grande do Norte	RN	Marcelino Vieira	1156
1157	BR	Brasil	Rio Grande do Norte	RN	Martins	1157
1158	BR	Brasil	Rio Grande do Norte	RN	Maxaranguape	1158
1159	BR	Brasil	Rio Grande do Norte	RN	Messias Targino	1159
1160	BR	Brasil	Rio Grande do Norte	RN	Montanhas	1160
1161	BR	Brasil	Rio Grande do Norte	RN	Monte Alegre	1161
1162	BR	Brasil	Rio Grande do Norte	RN	Monte Das Gameleiras	1162
1163	BR	Brasil	Rio Grande do Norte	RN	Mossoró	1163
1164	BR	Brasil	Rio Grande do Norte	RN	Natal	1164
1170	BR	Brasil	Rio Grande do Norte	RN	Paraú	1170
1171	BR	Brasil	Rio Grande do Norte	RN	Parazinho	1171
1172	BR	Brasil	Rio Grande do Norte	RN	Parelhas	1172
1173	BR	Brasil	Rio Grande do Norte	RN	Rio do Fogo	1173
1174	BR	Brasil	Rio Grande do Norte	RN	Passa e Fica	1174
1175	BR	Brasil	Rio Grande do Norte	RN	Passagem	1175
1176	BR	Brasil	Rio Grande do Norte	RN	Patu	1176
1177	BR	Brasil	Rio Grande do Norte	RN	Santa Maria	1177
1238	BR	Brasil	Rio Grande do Norte	RN	Várzea	1238
4298	BR	Brasil	Paraná	PR	Ubiratã	4298
5091	BR	Brasil	Rio Grande do Sul	RS	Viamão	5091
5092	BR	Brasil	Rio Grande do Sul	RS	Vicente Dutra	5092
5093	BR	Brasil	Rio Grande do Sul	RS	Victor Graeff	5093
5094	BR	Brasil	Rio Grande do Sul	RS	Vila Flores	5094
5095	BR	Brasil	Rio Grande do Sul	RS	Vila Lângaro	5095
5096	BR	Brasil	Rio Grande do Sul	RS	Vila Maria	5096
5097	BR	Brasil	Rio Grande do Sul	RS	Vila Nova do Sul	5097
5102	BR	Brasil	Rio Grande do Sul	RS	Westfalia	5102
5106	BR	Brasil	Mato Grosso do Sul	MS	Amambaí	5106
5107	BR	Brasil	Mato Grosso do Sul	MS	Anastácio	5107
5108	BR	Brasil	Mato Grosso do Sul	MS	Anaurilândia	5108
5109	BR	Brasil	Mato Grosso do Sul	MS	Angélica	5109
5110	BR	Brasil	Mato Grosso do Sul	MS	Antônio João	5110
1243	BR	Brasil	Paraíba	PB	Água Branca	1243
1244	BR	Brasil	Paraíba	PB	Aguiar	1244
1245	BR	Brasil	Paraíba	PB	Alagoa Grande	1245
1246	BR	Brasil	Paraíba	PB	Alagoa Nova	1246
1247	BR	Brasil	Paraíba	PB	Alagoinha	1247
1248	BR	Brasil	Paraíba	PB	Alcantil	1248
1249	BR	Brasil	Paraíba	PB	Algodão de Jandaíra	1249
1283	BR	Brasil	Paraíba	PB	Cabaceiras	1283
1284	BR	Brasil	Paraíba	PB	Cabedelo	1284
1307	BR	Brasil	Paraíba	PB	Coxixola	1307
1308	BR	Brasil	Paraíba	PB	Cruz do Espírito Santo	1308
1309	BR	Brasil	Paraíba	PB	Cubati	1309
1310	BR	Brasil	Paraíba	PB	Cuité	1310
1311	BR	Brasil	Paraíba	PB	Cuitegi	1311
1312	BR	Brasil	Paraíba	PB	Cuité de Mamanguape	1312
1313	BR	Brasil	Paraíba	PB	Curral de Cima	1313
1314	BR	Brasil	Paraíba	PB	Curral Velho	1314
1315	BR	Brasil	Paraíba	PB	Damião	1315
1316	BR	Brasil	Paraíba	PB	Desterro	1316
1317	BR	Brasil	Paraíba	PB	Vista Serrana	1317
1318	BR	Brasil	Paraíba	PB	Diamante	1318
1319	BR	Brasil	Paraíba	PB	Dona Inês	1319
1320	BR	Brasil	Paraíba	PB	Duas Estradas	1320
1321	BR	Brasil	Paraíba	PB	Emas	1321
1322	BR	Brasil	Paraíba	PB	Esperança	1322
1323	BR	Brasil	Paraíba	PB	Fagundes	1323
1324	BR	Brasil	Paraíba	PB	Frei Martinho	1324
1325	BR	Brasil	Paraíba	PB	Gado Bravo	1325
1326	BR	Brasil	Paraíba	PB	Guarabira	1326
1327	BR	Brasil	Paraíba	PB	Gurinhém	1327
1365	BR	Brasil	Paraíba	PB	Monte Horebe	1365
1366	BR	Brasil	Paraíba	PB	Monteiro	1366
1367	BR	Brasil	Paraíba	PB	Mulungu	1367
1368	BR	Brasil	Paraíba	PB	Natuba	1368
2381	BR	Brasil	Minas Gerais	MG	Capinópolis	2381
3013	BR	Brasil	Minas Gerais	MG	Sarzedo	3013
4605	BR	Brasil	Santa Catarina	SC	Zortéa	4605
1369	BR	Brasil	Paraíba	PB	Nazarezinho	1369
1370	BR	Brasil	Paraíba	PB	Nova Floresta	1370
1378	BR	Brasil	Paraíba	PB	Patos	1378
1379	BR	Brasil	Paraíba	PB	Paulista	1379
1417	BR	Brasil	Paraíba	PB	Santa Rita	1417
1418	BR	Brasil	Paraíba	PB	Santa Teresinha	1418
1419	BR	Brasil	Paraíba	PB	Santo André	1419
1420	BR	Brasil	Paraíba	PB	São Bento	1420
1421	BR	Brasil	Paraíba	PB	São Bentinho	1421
1422	BR	Brasil	Paraíba	PB	São Domingos do Cariri	1422
1423	BR	Brasil	Paraíba	PB	São Domingos de Pombal	1423
1424	BR	Brasil	Paraíba	PB	São Francisco	1424
1425	BR	Brasil	Paraíba	PB	São João do Cariri	1425
1426	BR	Brasil	Paraíba	PB	São João do Tigre	1426
1427	BR	Brasil	Paraíba	PB	São José da Lagoa Tapada	1427
1433	BR	Brasil	Paraíba	PB	São José do Bonfim	1433
1434	BR	Brasil	Paraíba	PB	São José do Brejo do Cruz	1434
1435	BR	Brasil	Paraíba	PB	São José do Sabugi	1435
1436	BR	Brasil	Paraíba	PB	São José Dos Cordeiros	1436
1437	BR	Brasil	Paraíba	PB	São Mamede	1437
1438	BR	Brasil	Paraíba	PB	São Miguel de Taipu	1438
1439	BR	Brasil	Paraíba	PB	São Sebastião de Lagoa de Roça	1439
2413	BR	Brasil	Minas Gerais	MG	Catuji	2413
2414	BR	Brasil	Minas Gerais	MG	Catuti	2414
2415	BR	Brasil	Minas Gerais	MG	Caxambu	2415
2416	BR	Brasil	Minas Gerais	MG	Cedro do Abaeté	2416
2417	BR	Brasil	Minas Gerais	MG	Central de Minas	2417
2418	BR	Brasil	Minas Gerais	MG	Centralina	2418
2419	BR	Brasil	Minas Gerais	MG	Chácara	2419
2420	BR	Brasil	Minas Gerais	MG	Chalé	2420
2421	BR	Brasil	Minas Gerais	MG	Chapada do Norte	2421
2422	BR	Brasil	Minas Gerais	MG	Chapada Gaúcha	2422
2423	BR	Brasil	Minas Gerais	MG	Chiador	2423
2424	BR	Brasil	Minas Gerais	MG	Cipotânea	2424
2425	BR	Brasil	Minas Gerais	MG	Claraval	2425
2426	BR	Brasil	Minas Gerais	MG	Claro Dos Poções	2426
2427	BR	Brasil	Minas Gerais	MG	Cláudio	2427
1440	BR	Brasil	Paraíba	PB	São Sebastião do Umbuzeiro	1440
1442	BR	Brasil	Paraíba	PB	Seridó	1442
1443	BR	Brasil	Paraíba	PB	Serra Branca	1443
1444	BR	Brasil	Paraíba	PB	Serra da Raiz	1444
1445	BR	Brasil	Paraíba	PB	Serra Grande	1445
1446	BR	Brasil	Paraíba	PB	Serra Redonda	1446
1486	BR	Brasil	Pernambuco	PE	Bezerros	1486
1487	BR	Brasil	Pernambuco	PE	Bodocó	1487
1488	BR	Brasil	Pernambuco	PE	Bom Conselho	1488
1492	BR	Brasil	Pernambuco	PE	Brejinho	1492
1494	BR	Brasil	Pernambuco	PE	Buenos Aires	1494
1495	BR	Brasil	Pernambuco	PE	Buíque	1495
1496	BR	Brasil	Pernambuco	PE	Cabo de Santo Agostinho	1496
1518	BR	Brasil	Pernambuco	PE	Cortês	1518
1519	BR	Brasil	Pernambuco	PE	Cumaru	1519
1520	BR	Brasil	Pernambuco	PE	Cupira	1520
1521	BR	Brasil	Pernambuco	PE	Custódia	1521
1522	BR	Brasil	Pernambuco	PE	Dormentes	1522
1523	BR	Brasil	Pernambuco	PE	Escada	1523
1524	BR	Brasil	Pernambuco	PE	Exu	1524
1525	BR	Brasil	Pernambuco	PE	Feira Nova	1525
1526	BR	Brasil	Pernambuco	PE	Fernando de Noronha	1526
1527	BR	Brasil	Pernambuco	PE	Ferreiros	1527
1528	BR	Brasil	Pernambuco	PE	Flores	1528
1529	BR	Brasil	Pernambuco	PE	Floresta	1529
1530	BR	Brasil	Pernambuco	PE	Frei Miguelinho	1530
1531	BR	Brasil	Pernambuco	PE	Gameleira	1531
1532	BR	Brasil	Pernambuco	PE	Garanhuns	1532
1533	BR	Brasil	Pernambuco	PE	Glória do Goitá	1533
1534	BR	Brasil	Pernambuco	PE	Goiana	1534
1535	BR	Brasil	Pernambuco	PE	Granito	1535
2499	BR	Brasil	Minas Gerais	MG	Dom Viçoso	2499
2500	BR	Brasil	Minas Gerais	MG	Dona Eusébia	2500
2501	BR	Brasil	Minas Gerais	MG	Dores de Campos	2501
2502	BR	Brasil	Minas Gerais	MG	Dores de Guanhães	2502
2507	BR	Brasil	Minas Gerais	MG	Durandé	2507
3070	BR	Brasil	Minas Gerais	MG	Unaí	3070
5141	BR	Brasil	Mato Grosso do Sul	MS	Iguatemi	5141
1536	BR	Brasil	Pernambuco	PE	Gravatá	1536
1537	BR	Brasil	Pernambuco	PE	Iati	1537
1552	BR	Brasil	Pernambuco	PE	Itaquitinga	1552
1553	BR	Brasil	Pernambuco	PE	Jaboatão Dos Guararapes	1553
1554	BR	Brasil	Pernambuco	PE	Jaqueira	1554
1555	BR	Brasil	Pernambuco	PE	Jataúba	1555
1556	BR	Brasil	Pernambuco	PE	Jatobá	1556
1557	BR	Brasil	Pernambuco	PE	João Alfredo	1557
1558	BR	Brasil	Pernambuco	PE	Joaquim Nabuco	1558
1559	BR	Brasil	Pernambuco	PE	Jucati	1559
1560	BR	Brasil	Pernambuco	PE	Jupi	1560
1561	BR	Brasil	Pernambuco	PE	Jurema	1561
1562	BR	Brasil	Pernambuco	PE	Lagoa do Carro	1562
1563	BR	Brasil	Pernambuco	PE	Lagoa do Itaenga	1563
1564	BR	Brasil	Pernambuco	PE	Lagoa do Ouro	1564
1565	BR	Brasil	Pernambuco	PE	Lagoa Dos Gatos	1565
1566	BR	Brasil	Pernambuco	PE	Lagoa Grande	1566
1567	BR	Brasil	Pernambuco	PE	Lajedo	1567
1568	BR	Brasil	Pernambuco	PE	Limoeiro	1568
1569	BR	Brasil	Pernambuco	PE	Macaparana	1569
1570	BR	Brasil	Pernambuco	PE	Machados	1570
1571	BR	Brasil	Pernambuco	PE	Manari	1571
1572	BR	Brasil	Pernambuco	PE	Maraial	1572
1573	BR	Brasil	Pernambuco	PE	Mirandiba	1573
1574	BR	Brasil	Pernambuco	PE	Moreno	1574
1575	BR	Brasil	Pernambuco	PE	Nazaré da Mata	1575
1576	BR	Brasil	Pernambuco	PE	Olinda	1576
1577	BR	Brasil	Pernambuco	PE	Orobó	1577
1578	BR	Brasil	Pernambuco	PE	Orocó	1578
1579	BR	Brasil	Pernambuco	PE	Ouricuri	1579
2564	BR	Brasil	Minas Gerais	MG	Guaraciaba	2564
2565	BR	Brasil	Minas Gerais	MG	Guaraciama	2565
2566	BR	Brasil	Minas Gerais	MG	Guaranésia	2566
2567	BR	Brasil	Minas Gerais	MG	Guarani	2567
2568	BR	Brasil	Minas Gerais	MG	Guarará	2568
2569	BR	Brasil	Minas Gerais	MG	Guarda-mor	2569
2570	BR	Brasil	Minas Gerais	MG	Guaxupé	2570
2571	BR	Brasil	Minas Gerais	MG	Guidoval	2571
2572	BR	Brasil	Minas Gerais	MG	Guimarânia	2572
2573	BR	Brasil	Minas Gerais	MG	Guiricema	2573
2574	BR	Brasil	Minas Gerais	MG	Gurinhatã	2574
2575	BR	Brasil	Minas Gerais	MG	Heliodora	2575
1599	BR	Brasil	Pernambuco	PE	Ribeirão	1599
1600	BR	Brasil	Pernambuco	PE	Rio Formoso	1600
1603	BR	Brasil	Pernambuco	PE	Salgueiro	1603
1604	BR	Brasil	Pernambuco	PE	Saloá	1604
1605	BR	Brasil	Pernambuco	PE	Sanharó	1605
1606	BR	Brasil	Pernambuco	PE	Santa Cruz	1606
1607	BR	Brasil	Pernambuco	PE	Santa Cruz da Baixa Verde	1607
1608	BR	Brasil	Pernambuco	PE	Santa Cruz do Capibaribe	1608
1633	BR	Brasil	Pernambuco	PE	Tamandaré	1633
1634	BR	Brasil	Pernambuco	PE	Taquaritinga do Norte	1634
1635	BR	Brasil	Pernambuco	PE	Terezinha	1635
1636	BR	Brasil	Pernambuco	PE	Terra Nova	1636
1637	BR	Brasil	Pernambuco	PE	Timbaúba	1637
1638	BR	Brasil	Pernambuco	PE	Toritama	1638
1639	BR	Brasil	Pernambuco	PE	Tracunhaém	1639
1640	BR	Brasil	Pernambuco	PE	Trindade	1640
1641	BR	Brasil	Pernambuco	PE	Triunfo	1641
1642	BR	Brasil	Pernambuco	PE	Tupanatinga	1642
1643	BR	Brasil	Pernambuco	PE	Tuparetama	1643
1644	BR	Brasil	Pernambuco	PE	Venturosa	1644
1645	BR	Brasil	Pernambuco	PE	Verdejante	1645
1646	BR	Brasil	Pernambuco	PE	Vertente do Lério	1646
1647	BR	Brasil	Pernambuco	PE	Vertentes	1647
1648	BR	Brasil	Pernambuco	PE	Vicência	1648
1649	BR	Brasil	Pernambuco	PE	Vitória de Santo Antão	1649
1650	BR	Brasil	Pernambuco	PE	Xexéu	1650
1651	BR	Brasil	Alagoas	AL	Água Branca	1651
1653	BR	Brasil	Alagoas	AL	Arapiraca	1653
1654	BR	Brasil	Alagoas	AL	Atalaia	1654
1655	BR	Brasil	Alagoas	AL	Barra de Santo Antônio	1655
2595	BR	Brasil	Minas Gerais	MG	Ingaí	2595
2596	BR	Brasil	Minas Gerais	MG	Inhapim	2596
2597	BR	Brasil	Minas Gerais	MG	Inhaúma	2597
2598	BR	Brasil	Minas Gerais	MG	Inimutaba	2598
2599	BR	Brasil	Minas Gerais	MG	Ipaba	2599
2600	BR	Brasil	Minas Gerais	MG	Ipanema	2600
559	BR	Brasil	Maranhão	MA	Magalhães de Almeida	559
560	BR	Brasil	Maranhão	MA	Maracaçumé	560
561	BR	Brasil	Maranhão	MA	Marajá do Sena	561
562	BR	Brasil	Maranhão	MA	Maranhãozinho	562
563	BR	Brasil	Maranhão	MA	Mata Roma	563
564	BR	Brasil	Maranhão	MA	Matinha	564
565	BR	Brasil	Maranhão	MA	Matões	565
566	BR	Brasil	Maranhão	MA	Matões do Norte	566
567	BR	Brasil	Maranhão	MA	Milagres do Maranhão	567
568	BR	Brasil	Maranhão	MA	Mirador	568
611	BR	Brasil	Maranhão	MA	Santa Filomena do Maranhão	611
634	BR	Brasil	Maranhão	MA	São José de Ribamar	634
654	BR	Brasil	Maranhão	MA	Timon	654
655	BR	Brasil	Maranhão	MA	Trizidela do Vale	655
656	BR	Brasil	Maranhão	MA	Tufilândia	656
657	BR	Brasil	Maranhão	MA	Tuntum	657
658	BR	Brasil	Maranhão	MA	Turiaçu	658
660	BR	Brasil	Maranhão	MA	Tutóia	660
661	BR	Brasil	Maranhão	MA	Urbano Santos	661
662	BR	Brasil	Maranhão	MA	Vargem Grande	662
663	BR	Brasil	Maranhão	MA	Viana	663
664	BR	Brasil	Maranhão	MA	Vila Nova Dos Martírios	664
667	BR	Brasil	Maranhão	MA	zé Doca	667
1656	BR	Brasil	Alagoas	AL	Barra de São Miguel	1656
1657	BR	Brasil	Alagoas	AL	Batalha	1657
1659	BR	Brasil	Alagoas	AL	Belo Monte	1659
1660	BR	Brasil	Alagoas	AL	Boca da Mata	1660
1661	BR	Brasil	Alagoas	AL	Branquinha	1661
1662	BR	Brasil	Alagoas	AL	Cacimbinhas	1662
1663	BR	Brasil	Alagoas	AL	Cajueiro	1663
1664	BR	Brasil	Alagoas	AL	Campestre	1664
1665	BR	Brasil	Alagoas	AL	Campo Alegre	1665
1666	BR	Brasil	Alagoas	AL	Campo Grande	1666
1667	BR	Brasil	Alagoas	AL	Canapi	1667
1668	BR	Brasil	Alagoas	AL	Capela	1668
1669	BR	Brasil	Alagoas	AL	Carneiros	1669
1670	BR	Brasil	Alagoas	AL	Chã Preta	1670
1671	BR	Brasil	Alagoas	AL	Coité do Nóia	1671
1672	BR	Brasil	Alagoas	AL	Colônia Leopoldina	1672
1673	BR	Brasil	Alagoas	AL	Coqueiro Seco	1673
1674	BR	Brasil	Alagoas	AL	Coruripe	1674
1675	BR	Brasil	Alagoas	AL	Craíbas	1675
1684	BR	Brasil	Alagoas	AL	Igaci	1684
1685	BR	Brasil	Alagoas	AL	Igreja Nova	1685
1686	BR	Brasil	Alagoas	AL	Inhapi	1686
1687	BR	Brasil	Alagoas	AL	Jacaré Dos Homens	1687
1688	BR	Brasil	Alagoas	AL	Jacuípe	1688
1689	BR	Brasil	Alagoas	AL	Japaratinga	1689
3167	BR	Brasil	Espírito Santo	ES	Serra	3167
491	BR	Brasil	Maranhão	MA	Buriticupu	491
492	BR	Brasil	Maranhão	MA	Buritirana	492
493	BR	Brasil	Maranhão	MA	Cachoeira Grande	493
494	BR	Brasil	Maranhão	MA	Cajapió	494
979	BR	Brasil	Ceará	CE	Itapipoca	979
1005	BR	Brasil	Ceará	CE	Missão Velha	1005
1006	BR	Brasil	Ceará	CE	Mombaça	1006
1007	BR	Brasil	Ceará	CE	Monsenhor Tabosa	1007
1711	BR	Brasil	Alagoas	AL	Olho D´água Das Flores	1711
1712	BR	Brasil	Alagoas	AL	Olho D´água do Casado	1712
1713	BR	Brasil	Alagoas	AL	Olho D´água Grande	1713
1714	BR	Brasil	Alagoas	AL	Olivença	1714
1715	BR	Brasil	Alagoas	AL	Ouro Branco	1715
1716	BR	Brasil	Alagoas	AL	Palestina	1716
1717	BR	Brasil	Alagoas	AL	Palmeira Dos Índios	1717
1718	BR	Brasil	Alagoas	AL	Pão de Açúcar	1718
2650	BR	Brasil	Minas Gerais	MG	Jequitibá	2650
2651	BR	Brasil	Minas Gerais	MG	Jequitinhonha	2651
2652	BR	Brasil	Minas Gerais	MG	Jesuânia	2652
2653	BR	Brasil	Minas Gerais	MG	Joaíma	2653
2664	BR	Brasil	Minas Gerais	MG	Juiz de Fora	2664
2667	BR	Brasil	Minas Gerais	MG	Juvenília	2667
2668	BR	Brasil	Minas Gerais	MG	Ladainha	2668
2669	BR	Brasil	Minas Gerais	MG	Lagamar	2669
2670	BR	Brasil	Minas Gerais	MG	Lagoa da Prata	2670
2671	BR	Brasil	Minas Gerais	MG	Lagoa Dos Patos	2671
2672	BR	Brasil	Minas Gerais	MG	Lagoa Dourada	2672
2673	BR	Brasil	Minas Gerais	MG	Lagoa Formosa	2673
2674	BR	Brasil	Minas Gerais	MG	Lagoa Grande	2674
2675	BR	Brasil	Minas Gerais	MG	Lagoa Santa	2675
2676	BR	Brasil	Minas Gerais	MG	Lajinha	2676
2677	BR	Brasil	Minas Gerais	MG	Lambari	2677
1070	BR	Brasil	Ceará	CE	Umirim	1070
1071	BR	Brasil	Ceará	CE	Uruburetama	1071
1072	BR	Brasil	Ceará	CE	Uruoca	1072
1073	BR	Brasil	Ceará	CE	Varjota	1073
1074	BR	Brasil	Ceará	CE	Várzea Alegre	1074
1149	BR	Brasil	Rio Grande do Norte	RN	Lajes	1149
1150	BR	Brasil	Rio Grande do Norte	RN	Lajes Pintadas	1150
1151	BR	Brasil	Rio Grande do Norte	RN	Lucrécia	1151
1153	BR	Brasil	Rio Grande do Norte	RN	Macaíba	1153
1817	BR	Brasil	Sergipe	SE	Santo Amaro Das Brotas	1817
1818	BR	Brasil	Sergipe	SE	São Cristóvão	1818
1819	BR	Brasil	Sergipe	SE	São Domingos	1819
1820	BR	Brasil	Sergipe	SE	São Francisco	1820
1821	BR	Brasil	Sergipe	SE	São Miguel do Aleixo	1821
1822	BR	Brasil	Sergipe	SE	Simão Dias	1822
1824	BR	Brasil	Sergipe	SE	Telha	1824
1825	BR	Brasil	Sergipe	SE	Tobias Barreto	1825
1826	BR	Brasil	Sergipe	SE	Tomar do Geru	1826
2715	BR	Brasil	Minas Gerais	MG	Mateus Leme	2715
2716	BR	Brasil	Minas Gerais	MG	Matias Barbosa	2716
2717	BR	Brasil	Minas Gerais	MG	Matias Cardoso	2717
2718	BR	Brasil	Minas Gerais	MG	Matipó	2718
2719	BR	Brasil	Minas Gerais	MG	Mato Verde	2719
2720	BR	Brasil	Minas Gerais	MG	Matozinhos	2720
2721	BR	Brasil	Minas Gerais	MG	Matutina	2721
2722	BR	Brasil	Minas Gerais	MG	Medeiros	2722
2746	BR	Brasil	Minas Gerais	MG	Montezuma	2746
2747	BR	Brasil	Minas Gerais	MG	Morada Nova de Minas	2747
2748	BR	Brasil	Minas Gerais	MG	Morro da Garça	2748
2749	BR	Brasil	Minas Gerais	MG	Morro do Pilar	2749
2750	BR	Brasil	Minas Gerais	MG	Munhoz	2750
2751	BR	Brasil	Minas Gerais	MG	Muriaé	2751
2752	BR	Brasil	Minas Gerais	MG	Mutum	2752
2753	BR	Brasil	Minas Gerais	MG	Muzambinho	2753
2754	BR	Brasil	Minas Gerais	MG	Nacip Raydan	2754
2755	BR	Brasil	Minas Gerais	MG	Nanuque	2755
1179	BR	Brasil	Rio Grande do Norte	RN	Pedra Grande	1179
1180	BR	Brasil	Rio Grande do Norte	RN	Pedra Preta	1180
1181	BR	Brasil	Rio Grande do Norte	RN	Pedro Avelino	1181
1182	BR	Brasil	Rio Grande do Norte	RN	Pedro Velho	1182
1183	BR	Brasil	Rio Grande do Norte	RN	Pendências	1183
1184	BR	Brasil	Rio Grande do Norte	RN	Pilões	1184
1185	BR	Brasil	Rio Grande do Norte	RN	Poço Branco	1185
1186	BR	Brasil	Rio Grande do Norte	RN	Portalegre	1186
1187	BR	Brasil	Rio Grande do Norte	RN	Porto do Mangue	1187
1188	BR	Brasil	Rio Grande do Norte	RN	Presidente Juscelino	1188
1221	BR	Brasil	Rio Grande do Norte	RN	Serra do Mel	1221
1222	BR	Brasil	Rio Grande do Norte	RN	Serra Negra do Norte	1222
1223	BR	Brasil	Rio Grande do Norte	RN	Serrinha	1223
1224	BR	Brasil	Rio Grande do Norte	RN	Serrinha Dos Pintos	1224
1225	BR	Brasil	Rio Grande do Norte	RN	Severiano Melo	1225
1226	BR	Brasil	Rio Grande do Norte	RN	Sítio Novo	1226
1227	BR	Brasil	Rio Grande do Norte	RN	Taboleiro Grande	1227
1228	BR	Brasil	Rio Grande do Norte	RN	Taipu	1228
1229	BR	Brasil	Rio Grande do Norte	RN	Tangará	1229
1230	BR	Brasil	Rio Grande do Norte	RN	Tenente Ananias	1230
1231	BR	Brasil	Rio Grande do Norte	RN	Tenente Laurentino Cruz	1231
1232	BR	Brasil	Rio Grande do Norte	RN	Tibau do Sul	1232
1233	BR	Brasil	Rio Grande do Norte	RN	Timbaúba Dos Batistas	1233
1234	BR	Brasil	Rio Grande do Norte	RN	Touros	1234
1235	BR	Brasil	Rio Grande do Norte	RN	Triunfo Potiguar	1235
1236	BR	Brasil	Rio Grande do Norte	RN	Umarizal	1236
1237	BR	Brasil	Rio Grande do Norte	RN	Upanema	1237
4660	BR	Brasil	Rio Grande do Sul	RS	Bossoroca	4660
4864	BR	Brasil	Rio Grande do Sul	RS	Monte Belo do Sul	4864
4895	BR	Brasil	Rio Grande do Sul	RS	Novo Tiradentes	4895
4896	BR	Brasil	Rio Grande do Sul	RS	Novo Xingu	4896
874	BR	Brasil	Piauí	PI	Sebastião Barros	874
875	BR	Brasil	Piauí	PI	Sebastião Leal	875
876	BR	Brasil	Piauí	PI	Sigefredo Pacheco	876
878	BR	Brasil	Piauí	PI	Simplício Mendes	878
879	BR	Brasil	Piauí	PI	Socorro do Piauí	879
880	BR	Brasil	Piauí	PI	Sussuapara	880
881	BR	Brasil	Piauí	PI	Tamboril do Piauí	881
882	BR	Brasil	Piauí	PI	Tanque do Piauí	882
883	BR	Brasil	Piauí	PI	Teresina	883
885	BR	Brasil	Piauí	PI	Uruçuí	885
886	BR	Brasil	Piauí	PI	Valença do Piauí	886
887	BR	Brasil	Piauí	PI	Várzea Branca	887
888	BR	Brasil	Piauí	PI	Várzea Grande	888
1380	BR	Brasil	Paraíba	PB	Pedra Branca	1380
1381	BR	Brasil	Paraíba	PB	Pedra Lavrada	1381
1382	BR	Brasil	Paraíba	PB	Pedras de Fogo	1382
1383	BR	Brasil	Paraíba	PB	Piancó	1383
1384	BR	Brasil	Paraíba	PB	Picuí	1384
1385	BR	Brasil	Paraíba	PB	Pilar	1385
1386	BR	Brasil	Paraíba	PB	Pilões	1386
1387	BR	Brasil	Paraíba	PB	Pilõezinhos	1387
1389	BR	Brasil	Paraíba	PB	Pitimbu	1389
1390	BR	Brasil	Paraíba	PB	Pocinhos	1390
1391	BR	Brasil	Paraíba	PB	Poço Dantas	1391
1392	BR	Brasil	Paraíba	PB	Poço de José de Moura	1392
1393	BR	Brasil	Paraíba	PB	Pombal	1393
1399	BR	Brasil	Paraíba	PB	Remígio	1399
1400	BR	Brasil	Paraíba	PB	Pedro Régis	1400
1401	BR	Brasil	Paraíba	PB	Riachão	1401
1402	BR	Brasil	Paraíba	PB	Riachão do Bacamarte	1402
1403	BR	Brasil	Paraíba	PB	Riachão do Poço	1403
1404	BR	Brasil	Paraíba	PB	Riacho de Santo Antônio	1404
1405	BR	Brasil	Paraíba	PB	Riacho Dos Cavalos	1405
1406	BR	Brasil	Paraíba	PB	Rio Tinto	1406
1407	BR	Brasil	Paraíba	PB	Salgadinho	1407
1408	BR	Brasil	Paraíba	PB	Salgado de São Félix	1408
1409	BR	Brasil	Paraíba	PB	Santa Cecília	1409
1410	BR	Brasil	Paraíba	PB	Santa Cruz	1410
1411	BR	Brasil	Paraíba	PB	Santa Helena	1411
1412	BR	Brasil	Paraíba	PB	Santa Inês	1412
1413	BR	Brasil	Paraíba	PB	Santa Luzia	1413
1414	BR	Brasil	Paraíba	PB	Santana de Mangueira	1414
1415	BR	Brasil	Paraíba	PB	Santana Dos Garrotes	1415
1416	BR	Brasil	Paraíba	PB	Santarém	1416
399	BR	Brasil	Tocantins	TO	Oliveira de Fátima	399
466	BR	Brasil	Maranhão	MA	Araioses	466
467	BR	Brasil	Maranhão	MA	Arame	467
889	BR	Brasil	Piauí	PI	Vera Mendes	889
890	BR	Brasil	Piauí	PI	Vila Nova do Piauí	890
891	BR	Brasil	Piauí	PI	Wall Ferraz	891
1428	BR	Brasil	Paraíba	PB	São José de Caiana	1428
1429	BR	Brasil	Paraíba	PB	São José de Espinharas	1429
1430	BR	Brasil	Paraíba	PB	São José Dos Ramos	1430
1431	BR	Brasil	Paraíba	PB	São José de Piranhas	1431
1432	BR	Brasil	Paraíba	PB	São José de Princesa	1432
1617	BR	Brasil	Pernambuco	PE	São Joaquim do Monte	1617
1618	BR	Brasil	Pernambuco	PE	São José da Coroa Grande	1618
1623	BR	Brasil	Pernambuco	PE	Serra Talhada	1623
1624	BR	Brasil	Pernambuco	PE	Serrita	1624
1625	BR	Brasil	Pernambuco	PE	Sertânia	1625
1626	BR	Brasil	Pernambuco	PE	Sirinhaém	1626
1627	BR	Brasil	Pernambuco	PE	Moreilândia	1627
1628	BR	Brasil	Pernambuco	PE	Solidão	1628
1629	BR	Brasil	Pernambuco	PE	Surubim	1629
1630	BR	Brasil	Pernambuco	PE	Tabira	1630
1631	BR	Brasil	Pernambuco	PE	Tacaimbó	1631
1632	BR	Brasil	Pernambuco	PE	Tacaratu	1632
2111	BR	Brasil	Bahia	BA	Olindina	2111
2112	BR	Brasil	Bahia	BA	Oliveira Dos Brejinhos	2112
2113	BR	Brasil	Bahia	BA	Ouriçangas	2113
2114	BR	Brasil	Bahia	BA	Ourolândia	2114
2115	BR	Brasil	Bahia	BA	Palmas de Monte Alto	2115
2116	BR	Brasil	Bahia	BA	Palmeiras	2116
2121	BR	Brasil	Bahia	BA	Paulo Afonso	2121
2122	BR	Brasil	Bahia	BA	pé de Serra	2122
2125	BR	Brasil	Bahia	BA	Piatã	2125
2126	BR	Brasil	Bahia	BA	Pilão Arcado	2126
2127	BR	Brasil	Bahia	BA	Pindaí	2127
2128	BR	Brasil	Bahia	BA	Pindobaçu	2128
2184	BR	Brasil	Bahia	BA	São Francisco do Conde	2184
2185	BR	Brasil	Bahia	BA	São Gabriel	2185
2186	BR	Brasil	Bahia	BA	São Gonçalo Dos Campos	2186
2187	BR	Brasil	Bahia	BA	São José da Vitória	2187
2188	BR	Brasil	Bahia	BA	São José do Jacuípe	2188
2189	BR	Brasil	Bahia	BA	São Miguel Das Matas	2189
2190	BR	Brasil	Bahia	BA	São Sebastião do Passé	2190
2191	BR	Brasil	Bahia	BA	Sapeaçu	2191
2192	BR	Brasil	Bahia	BA	Sátiro Dias	2192
2193	BR	Brasil	Bahia	BA	Saubara	2193
2194	BR	Brasil	Bahia	BA	Saúde	2194
2195	BR	Brasil	Bahia	BA	Seabra	2195
2196	BR	Brasil	Bahia	BA	Sebastião Laranjeiras	2196
4971	BR	Brasil	Rio Grande do Sul	RS	Santa Maria	4971
501	BR	Brasil	Maranhão	MA	Carutapera	501
502	BR	Brasil	Maranhão	MA	Caxias	502
503	BR	Brasil	Maranhão	MA	Cedral	503
504	BR	Brasil	Maranhão	MA	Central do Maranhão	504
505	BR	Brasil	Maranhão	MA	Centro do Guilherme	505
506	BR	Brasil	Maranhão	MA	Centro Novo do Maranhão	506
669	BR	Brasil	Piauí	PI	Agricolândia	669
670	BR	Brasil	Piauí	PI	Água Branca	670
671	BR	Brasil	Piauí	PI	Alagoinha do Piauí	671
672	BR	Brasil	Piauí	PI	Alegrete do Piauí	672
673	BR	Brasil	Piauí	PI	Alto Longá	673
674	BR	Brasil	Piauí	PI	Altos	674
675	BR	Brasil	Piauí	PI	Alvorada do Gurguéia	675
676	BR	Brasil	Piauí	PI	Amarante	676
677	BR	Brasil	Piauí	PI	Angical do Piauí	677
678	BR	Brasil	Piauí	PI	Anísio de Abreu	678
679	BR	Brasil	Piauí	PI	Antônio Almeida	679
680	BR	Brasil	Piauí	PI	Aroazes	680
681	BR	Brasil	Piauí	PI	Aroeiras do Itaim	681
682	BR	Brasil	Piauí	PI	Arraial	682
683	BR	Brasil	Piauí	PI	Assunção do Piauí	683
684	BR	Brasil	Piauí	PI	Avelino Lopes	684
685	BR	Brasil	Piauí	PI	Baixa Grande do Ribeiro	685
686	BR	Brasil	Piauí	PI	Barra D´alcântara	686
687	BR	Brasil	Piauí	PI	Barras	687
688	BR	Brasil	Piauí	PI	Barreiras do Piauí	688
689	BR	Brasil	Piauí	PI	Barro Duro	689
1046	BR	Brasil	Ceará	CE	Russas	1046
1048	BR	Brasil	Ceará	CE	Salitre	1048
1049	BR	Brasil	Ceará	CE	Santana do Acaraú	1049
1050	BR	Brasil	Ceará	CE	Santana do Cariri	1050
1051	BR	Brasil	Ceará	CE	Santa Quitéria	1051
1052	BR	Brasil	Ceará	CE	São Benedito	1052
1053	BR	Brasil	Ceará	CE	São Gonçalo do Amarante	1053
1054	BR	Brasil	Ceará	CE	São João do Jaguaribe	1054
1055	BR	Brasil	Ceará	CE	São Luís do Curu	1055
1056	BR	Brasil	Ceará	CE	Senador Pompeu	1056
1057	BR	Brasil	Ceará	CE	Senador sá	1057
1058	BR	Brasil	Ceará	CE	Sobral	1058
1059	BR	Brasil	Ceará	CE	Solonópole	1059
1060	BR	Brasil	Ceará	CE	Tabuleiro do Norte	1060
1061	BR	Brasil	Ceará	CE	Tamboril	1061
1062	BR	Brasil	Ceará	CE	Tarrafas	1062
1063	BR	Brasil	Ceará	CE	Tauá	1063
449	BR	Brasil	Tocantins	TO	Wanderlândia	449
690	BR	Brasil	Piauí	PI	Batalha	690
691	BR	Brasil	Piauí	PI	Bela Vista do Piauí	691
692	BR	Brasil	Piauí	PI	Belém do Piauí	692
693	BR	Brasil	Piauí	PI	Beneditinos	693
694	BR	Brasil	Piauí	PI	Bertolínia	694
695	BR	Brasil	Piauí	PI	Betânia do Piauí	695
696	BR	Brasil	Piauí	PI	Boa Hora	696
697	BR	Brasil	Piauí	PI	Bocaina	697
698	BR	Brasil	Piauí	PI	Bom Jesus	698
699	BR	Brasil	Piauí	PI	Bom Princípio do Piauí	699
700	BR	Brasil	Piauí	PI	Bonfim do Piauí	700
701	BR	Brasil	Piauí	PI	Boqueirão do Piauí	701
702	BR	Brasil	Piauí	PI	Brasileira	702
704	BR	Brasil	Piauí	PI	Buriti Dos Lopes	704
705	BR	Brasil	Piauí	PI	Buriti Dos Montes	705
706	BR	Brasil	Piauí	PI	Cabeceiras do Piauí	706
707	BR	Brasil	Piauí	PI	Cajazeiras do Piauí	707
708	BR	Brasil	Piauí	PI	Cajueiro da Praia	708
709	BR	Brasil	Piauí	PI	Caldeirão Grande do Piauí	709
710	BR	Brasil	Piauí	PI	Campinas do Piauí	710
711	BR	Brasil	Piauí	PI	Campo Alegre do Fidalgo	711
712	BR	Brasil	Piauí	PI	Campo Grande do Piauí	712
713	BR	Brasil	Piauí	PI	Campo Largo do Piauí	713
714	BR	Brasil	Piauí	PI	Campo Maior	714
719	BR	Brasil	Piauí	PI	Caracol	719
721	BR	Brasil	Piauí	PI	Caridade do Piauí	721
722	BR	Brasil	Piauí	PI	Castelo do Piauí	722
723	BR	Brasil	Piauí	PI	Caxingó	723
724	BR	Brasil	Piauí	PI	Cocal	724
725	BR	Brasil	Piauí	PI	Cocal de Telha	725
726	BR	Brasil	Piauí	PI	Cocal Dos Alves	726
727	BR	Brasil	Piauí	PI	Coivaras	727
732	BR	Brasil	Piauí	PI	Corrente	732
733	BR	Brasil	Piauí	PI	Cristalândia do Piauí	733
734	BR	Brasil	Piauí	PI	Cristino Castro	734
777	BR	Brasil	Piauí	PI	Júlio Borges	777
778	BR	Brasil	Piauí	PI	Jurema	778
779	BR	Brasil	Piauí	PI	Lagoinha do Piauí	779
780	BR	Brasil	Piauí	PI	Lagoa Alegre	780
781	BR	Brasil	Piauí	PI	Lagoa do Barro do Piauí	781
782	BR	Brasil	Piauí	PI	Lagoa de São Francisco	782
783	BR	Brasil	Piauí	PI	Lagoa do Piauí	783
784	BR	Brasil	Piauí	PI	Lagoa do Sítio	784
785	BR	Brasil	Piauí	PI	Landri Sales	785
786	BR	Brasil	Piauí	PI	Luís Correia	786
787	BR	Brasil	Piauí	PI	Luzilândia	787
788	BR	Brasil	Piauí	PI	Madeiro	788
789	BR	Brasil	Piauí	PI	Manoel Emídio	789
790	BR	Brasil	Piauí	PI	Marcolândia	790
450	BR	Brasil	Tocantins	TO	Xambioá	450
792	BR	Brasil	Piauí	PI	Massapê do Piauí	792
793	BR	Brasil	Piauí	PI	Matias Olímpio	793
794	BR	Brasil	Piauí	PI	Miguel Alves	794
795	BR	Brasil	Piauí	PI	Miguel Leão	795
796	BR	Brasil	Piauí	PI	Milton Brandão	796
797	BR	Brasil	Piauí	PI	Monsenhor Gil	797
798	BR	Brasil	Piauí	PI	Monsenhor Hipólito	798
799	BR	Brasil	Piauí	PI	Monte Alegre do Piauí	799
800	BR	Brasil	Piauí	PI	Morro Cabeça no Tempo	800
801	BR	Brasil	Piauí	PI	Morro do Chapéu do Piauí	801
802	BR	Brasil	Piauí	PI	Murici Dos Portelas	802
803	BR	Brasil	Piauí	PI	Nazaré do Piauí	803
804	BR	Brasil	Piauí	PI	Nazária	804
805	BR	Brasil	Piauí	PI	Nossa Senhora de Nazaré	805
806	BR	Brasil	Piauí	PI	Nossa Senhora Dos Remédios	806
807	BR	Brasil	Piauí	PI	Novo Oriente do Piauí	807
808	BR	Brasil	Piauí	PI	Novo Santo Antônio	808
809	BR	Brasil	Piauí	PI	Oeiras	809
810	BR	Brasil	Piauí	PI	Olho D´água do Piauí	810
811	BR	Brasil	Piauí	PI	Padre Marcos	811
812	BR	Brasil	Piauí	PI	Paes Landim	812
813	BR	Brasil	Piauí	PI	Pajeú do Piauí	813
814	BR	Brasil	Piauí	PI	Palmeira do Piauí	814
819	BR	Brasil	Piauí	PI	Passagem Franca do Piauí	819
820	BR	Brasil	Piauí	PI	Patos do Piauí	820
824	BR	Brasil	Piauí	PI	Pedro ii	824
825	BR	Brasil	Piauí	PI	Pedro Laurentino	825
826	BR	Brasil	Piauí	PI	Nova Santa Rita	826
828	BR	Brasil	Piauí	PI	Pimenteiras	828
829	BR	Brasil	Piauí	PI	Pio ix	829
830	BR	Brasil	Piauí	PI	Piracuruca	830
831	BR	Brasil	Piauí	PI	Piripiri	831
832	BR	Brasil	Piauí	PI	Porto	832
833	BR	Brasil	Piauí	PI	Porto Alegre do Piauí	833
834	BR	Brasil	Piauí	PI	Prata do Piauí	834
835	BR	Brasil	Piauí	PI	Queimada Nova	835
836	BR	Brasil	Piauí	PI	Redenção do Gurguéia	836
837	BR	Brasil	Piauí	PI	Regeneração	837
838	BR	Brasil	Piauí	PI	Riacho Frio	838
839	BR	Brasil	Piauí	PI	Ribeira do Piauí	839
840	BR	Brasil	Piauí	PI	Ribeiro Gonçalves	840
841	BR	Brasil	Piauí	PI	Rio Grande do Piauí	841
842	BR	Brasil	Piauí	PI	Santa Cruz do Piauí	842
843	BR	Brasil	Piauí	PI	Santa Cruz Dos Milagres	843
844	BR	Brasil	Piauí	PI	Santa Filomena	844
845	BR	Brasil	Piauí	PI	Santa Luz	845
846	BR	Brasil	Piauí	PI	Santana do Piauí	846
1078	BR	Brasil	Rio Grande do Norte	RN	Afonso Bezerra	1078
5507	BR	Brasil	Goiás	GO	Piranhas	5507
5508	BR	Brasil	Goiás	GO	Pirenópolis	5508
5509	BR	Brasil	Goiás	GO	Pires do Rio	5509
5510	BR	Brasil	Goiás	GO	Planaltina	5510
5511	BR	Brasil	Goiás	GO	Pontalina	5511
5512	BR	Brasil	Goiás	GO	Porangatu	5512
5513	BR	Brasil	Goiás	GO	Porteirão	5513
5514	BR	Brasil	Goiás	GO	Portelândia	5514
5515	BR	Brasil	Goiás	GO	Posse	5515
5516	BR	Brasil	Goiás	GO	Professor Jamil	5516
5517	BR	Brasil	Goiás	GO	Quirinópolis	5517
5518	BR	Brasil	Goiás	GO	Rialma	5518
5519	BR	Brasil	Goiás	GO	Rianápolis	5519
5520	BR	Brasil	Goiás	GO	Rio Quente	5520
5521	BR	Brasil	Goiás	GO	Rio Verde	5521
5522	BR	Brasil	Goiás	GO	Rubiataba	5522
5523	BR	Brasil	Goiás	GO	Sanclerlândia	5523
5524	BR	Brasil	Goiás	GO	Santa Bárbara de Goiás	5524
5525	BR	Brasil	Goiás	GO	Santa Cruz de Goiás	5525
5526	BR	Brasil	Goiás	GO	Santa fé de Goiás	5526
5527	BR	Brasil	Goiás	GO	Santa Helena de Goiás	5527
5528	BR	Brasil	Goiás	GO	Santa Isabel	5528
5529	BR	Brasil	Goiás	GO	Santa Rita do Araguaia	5529
5530	BR	Brasil	Goiás	GO	Santa Rita do Novo Destino	5530
5531	BR	Brasil	Goiás	GO	Santa Rosa de Goiás	5531
5532	BR	Brasil	Goiás	GO	Santa Tereza de Goiás	5532
5533	BR	Brasil	Goiás	GO	Santa Terezinha de Goiás	5533
5534	BR	Brasil	Goiás	GO	Santo Antônio da Barra	5534
5535	BR	Brasil	Goiás	GO	Santo Antônio de Goiás	5535
5536	BR	Brasil	Goiás	GO	Santo Antônio do Descoberto	5536
5537	BR	Brasil	Goiás	GO	São Domingos	5537
5538	BR	Brasil	Goiás	GO	São Francisco de Goiás	5538
5539	BR	Brasil	Goiás	GO	São João D´aliança	5539
5540	BR	Brasil	Goiás	GO	São João da Paraúna	5540
5541	BR	Brasil	Goiás	GO	São Luís de Montes Belos	5541
5542	BR	Brasil	Goiás	GO	São Luíz do Norte	5542
5543	BR	Brasil	Goiás	GO	São Miguel do Araguaia	5543
5544	BR	Brasil	Goiás	GO	São Miguel do Passa Quatro	5544
5546	BR	Brasil	Goiás	GO	São Simão	5546
5547	BR	Brasil	Goiás	GO	Senador Canedo	5547
5548	BR	Brasil	Goiás	GO	Serranópolis	5548
5549	BR	Brasil	Goiás	GO	Silvânia	5549
5550	BR	Brasil	Goiás	GO	Simolândia	5550
5551	BR	Brasil	Goiás	GO	Sítio D´abadia	5551
5552	BR	Brasil	Goiás	GO	Taquaral de Goiás	5552
5553	BR	Brasil	Goiás	GO	Teresina de Goiás	5553
5554	BR	Brasil	Goiás	GO	Terezópolis de Goiás	5554
5555	BR	Brasil	Goiás	GO	Três Ranchos	5555
5556	BR	Brasil	Goiás	GO	Trindade	5556
427	BR	Brasil	Tocantins	TO	Santa Maria do Tocantins	427
428	BR	Brasil	Tocantins	TO	Santa Rita do Tocantins	428
429	BR	Brasil	Tocantins	TO	Santa Rosa do Tocantins	429
430	BR	Brasil	Tocantins	TO	Santa Tereza do Tocantins	430
431	BR	Brasil	Tocantins	TO	Santa Terezinha do Tocantins	431
432	BR	Brasil	Tocantins	TO	São Bento do Tocantins	432
433	BR	Brasil	Tocantins	TO	São Félix do Tocantins	433
434	BR	Brasil	Tocantins	TO	São Miguel do Tocantins	434
435	BR	Brasil	Tocantins	TO	São Salvador do Tocantins	435
436	BR	Brasil	Tocantins	TO	São Sebastião do Tocantins	436
437	BR	Brasil	Tocantins	TO	São Valério da Natividade	437
451	BR	Brasil	Maranhão	MA	Açailândia	451
452	BR	Brasil	Maranhão	MA	Afonso Cunha	452
453	BR	Brasil	Maranhão	MA	Água Doce do Maranhão	453
454	BR	Brasil	Maranhão	MA	Alcântara	454
455	BR	Brasil	Maranhão	MA	Aldeias Altas	455
456	BR	Brasil	Maranhão	MA	Altamira do Maranhão	456
457	BR	Brasil	Maranhão	MA	Alto Alegre do Maranhão	457
458	BR	Brasil	Maranhão	MA	Alto Alegre do Pindaré	458
459	BR	Brasil	Maranhão	MA	Alto Parnaíba	459
460	BR	Brasil	Maranhão	MA	Amapá do Maranhão	460
461	BR	Brasil	Maranhão	MA	Amarante do Maranhão	461
462	BR	Brasil	Maranhão	MA	Anajatuba	462
463	BR	Brasil	Maranhão	MA	Anapurus	463
848	BR	Brasil	Piauí	PI	Santo Antônio de Lisboa	848
849	BR	Brasil	Piauí	PI	Santo Antônio Dos Milagres	849
850	BR	Brasil	Piauí	PI	Santo Inácio do Piauí	850
851	BR	Brasil	Piauí	PI	São Braz do Piauí	851
852	BR	Brasil	Piauí	PI	São Félix do Piauí	852
853	BR	Brasil	Piauí	PI	São Francisco de Assis do Piauí	853
854	BR	Brasil	Piauí	PI	São Francisco do Piauí	854
855	BR	Brasil	Piauí	PI	São Gonçalo do Gurguéia	855
856	BR	Brasil	Piauí	PI	São Gonçalo do Piauí	856
857	BR	Brasil	Piauí	PI	São João da Canabrava	857
858	BR	Brasil	Piauí	PI	São João da Fronteira	858
859	BR	Brasil	Piauí	PI	São João da Serra	859
860	BR	Brasil	Piauí	PI	São João da Varjota	860
861	BR	Brasil	Piauí	PI	São João do Arraial	861
862	BR	Brasil	Piauí	PI	São João do Piauí	862
863	BR	Brasil	Piauí	PI	São José do Divino	863
864	BR	Brasil	Piauí	PI	São José do Peixe	864
865	BR	Brasil	Piauí	PI	São José do Piauí	865
866	BR	Brasil	Piauí	PI	São Julião	866
867	BR	Brasil	Piauí	PI	São Lourenço do Piauí	867
1719	BR	Brasil	Alagoas	AL	Pariconha	1719
519	BR	Brasil	Maranhão	MA	Estreito	519
868	BR	Brasil	Piauí	PI	São Luis do Piauí	868
1083	BR	Brasil	Rio Grande do Norte	RN	Angicos	1083
1619	BR	Brasil	Pernambuco	PE	São José do Belmonte	1619
1620	BR	Brasil	Pernambuco	PE	São José do Egito	1620
1621	BR	Brasil	Pernambuco	PE	São Lourenço da Mata	1621
1622	BR	Brasil	Pernambuco	PE	São Vicente Ferrer	1622
1721	BR	Brasil	Alagoas	AL	Passo de Camaragibe	1721
1722	BR	Brasil	Alagoas	AL	Paulo Jacinto	1722
1723	BR	Brasil	Alagoas	AL	Penedo	1723
1724	BR	Brasil	Alagoas	AL	Piaçabuçu	1724
1725	BR	Brasil	Alagoas	AL	Pilar	1725
1726	BR	Brasil	Alagoas	AL	Pindoba	1726
1727	BR	Brasil	Alagoas	AL	Piranhas	1727
1728	BR	Brasil	Alagoas	AL	Poço Das Trincheiras	1728
2251	BR	Brasil	Minas Gerais	MG	Água Comprida	2251
2252	BR	Brasil	Minas Gerais	MG	Aguanil	2252
2253	BR	Brasil	Minas Gerais	MG	Águas Formosas	2253
2254	BR	Brasil	Minas Gerais	MG	Águas Vermelhas	2254
2255	BR	Brasil	Minas Gerais	MG	Aimorés	2255
2256	BR	Brasil	Minas Gerais	MG	Aiuruoca	2256
2257	BR	Brasil	Minas Gerais	MG	Alagoa	2257
2258	BR	Brasil	Minas Gerais	MG	Albertina	2258
2259	BR	Brasil	Minas Gerais	MG	Além Paraíba	2259
2260	BR	Brasil	Minas Gerais	MG	Alfenas	2260
2261	BR	Brasil	Minas Gerais	MG	Alfredo Vasconcelos	2261
2262	BR	Brasil	Minas Gerais	MG	Almenara	2262
2263	BR	Brasil	Minas Gerais	MG	Alpercata	2263
2264	BR	Brasil	Minas Gerais	MG	Alpinópolis	2264
2265	BR	Brasil	Minas Gerais	MG	Alterosa	2265
2266	BR	Brasil	Minas Gerais	MG	Alto Caparaó	2266
2267	BR	Brasil	Minas Gerais	MG	Alto Rio Doce	2267
2268	BR	Brasil	Minas Gerais	MG	Alvarenga	2268
2269	BR	Brasil	Minas Gerais	MG	Alvinópolis	2269
2270	BR	Brasil	Minas Gerais	MG	Alvorada de Minas	2270
2305	BR	Brasil	Minas Gerais	MG	Barbacena	2305
2306	BR	Brasil	Minas Gerais	MG	Barra Longa	2306
2307	BR	Brasil	Minas Gerais	MG	Barroso	2307
2308	BR	Brasil	Minas Gerais	MG	Bela Vista de Minas	2308
2309	BR	Brasil	Minas Gerais	MG	Belmiro Braga	2309
5029	BR	Brasil	Rio Grande do Sul	RS	Sede Nova	5029
5030	BR	Brasil	Rio Grande do Sul	RS	Segredo	5030
5031	BR	Brasil	Rio Grande do Sul	RS	Selbach	5031
5032	BR	Brasil	Rio Grande do Sul	RS	Senador Salgado Filho	5032
5033	BR	Brasil	Rio Grande do Sul	RS	Sentinela do Sul	5033
5034	BR	Brasil	Rio Grande do Sul	RS	Serafina Corrêa	5034
5035	BR	Brasil	Rio Grande do Sul	RS	Sério	5035
5036	BR	Brasil	Rio Grande do Sul	RS	Sertão	5036
5037	BR	Brasil	Rio Grande do Sul	RS	Sertão Santana	5037
5038	BR	Brasil	Rio Grande do Sul	RS	Sete de Setembro	5038
5039	BR	Brasil	Rio Grande do Sul	RS	Severiano de Almeida	5039
5040	BR	Brasil	Rio Grande do Sul	RS	Silveira Martins	5040
4279	BR	Brasil	Paraná	PR	Sulina	4279
4949	BR	Brasil	Rio Grande do Sul	RS	Rio Dos Índios	4949
5125	BR	Brasil	Mato Grosso do Sul	MS	Cassilândia	5125
5126	BR	Brasil	Mato Grosso do Sul	MS	Chapadão do Sul	5126
5127	BR	Brasil	Mato Grosso do Sul	MS	Corguinho	5127
5128	BR	Brasil	Mato Grosso do Sul	MS	Coronel Sapucaia	5128
5129	BR	Brasil	Mato Grosso do Sul	MS	Corumbá	5129
5130	BR	Brasil	Mato Grosso do Sul	MS	Costa Rica	5130
5131	BR	Brasil	Mato Grosso do Sul	MS	Coxim	5131
5132	BR	Brasil	Mato Grosso do Sul	MS	Deodápolis	5132
5133	BR	Brasil	Mato Grosso do Sul	MS	Dois Irmãos do Buriti	5133
5134	BR	Brasil	Mato Grosso do Sul	MS	Douradina	5134
5135	BR	Brasil	Mato Grosso do Sul	MS	Dourados	5135
5136	BR	Brasil	Mato Grosso do Sul	MS	Eldorado	5136
5137	BR	Brasil	Mato Grosso do Sul	MS	Fátima do Sul	5137
5138	BR	Brasil	Mato Grosso do Sul	MS	Figueirão	5138
5382	BR	Brasil	Goiás	GO	Catalão	5382
5383	BR	Brasil	Goiás	GO	Caturaí	5383
5500	BR	Brasil	Goiás	GO	Panamá	5500
4359	BR	Brasil	Santa Catarina	SC	Brusque	4359
5045	BR	Brasil	Rio Grande do Sul	RS	Tapejara	5045
2124	BR	Brasil	Bahia	BA	Pedro Alexandre	2124
2233	BR	Brasil	Bahia	BA	Valente	2233
2793	BR	Brasil	Minas Gerais	MG	Papagaios	2793
2794	BR	Brasil	Minas Gerais	MG	Paracatu	2794
3606	BR	Brasil	São Paulo	SP	Mirandópolis	3606
3607	BR	Brasil	São Paulo	SP	Mirante do Paranapanema	3607
3608	BR	Brasil	São Paulo	SP	Mirassol	3608
4180	BR	Brasil	Paraná	PR	Pinhão	4180
4182	BR	Brasil	Paraná	PR	Piraquara	4182
4200	BR	Brasil	Paraná	PR	Quatiguá	4200
4201	BR	Brasil	Paraná	PR	Quatro Barras	4201
4202	BR	Brasil	Paraná	PR	Quatro Pontes	4202
4203	BR	Brasil	Paraná	PR	Quedas do Iguaçu	4203
4204	BR	Brasil	Paraná	PR	Querência do Norte	4204
4465	BR	Brasil	Santa Catarina	SC	Major Gercino	4465
4466	BR	Brasil	Santa Catarina	SC	Major Vieira	4466
4467	BR	Brasil	Santa Catarina	SC	Maracajá	4467
4468	BR	Brasil	Santa Catarina	SC	Maravilha	4468
4469	BR	Brasil	Santa Catarina	SC	Marema	4469
4470	BR	Brasil	Santa Catarina	SC	Massaranduba	4470
4471	BR	Brasil	Santa Catarina	SC	Matos Costa	4471
4472	BR	Brasil	Santa Catarina	SC	Meleiro	4472
4473	BR	Brasil	Santa Catarina	SC	Mirim Doce	4473
4474	BR	Brasil	Santa Catarina	SC	Modelo	4474
4475	BR	Brasil	Santa Catarina	SC	Mondaí	4475
4476	BR	Brasil	Santa Catarina	SC	Monte Carlo	4476
4477	BR	Brasil	Santa Catarina	SC	Monte Castelo	4477
4478	BR	Brasil	Santa Catarina	SC	Morro da Fumaça	4478
5162	BR	Brasil	Mato Grosso do Sul	MS	Paranaíba	5162
5163	BR	Brasil	Mato Grosso do Sul	MS	Paranhos	5163
5164	BR	Brasil	Mato Grosso do Sul	MS	Pedro Gomes	5164
5165	BR	Brasil	Mato Grosso do Sul	MS	Ponta Porã	5165
5166	BR	Brasil	Mato Grosso do Sul	MS	Porto Murtinho	5166
5167	BR	Brasil	Mato Grosso do Sul	MS	Ribas do Rio Pardo	5167
5193	BR	Brasil	Mato Grosso	MT	Araguainha	5193
5194	BR	Brasil	Mato Grosso	MT	Araputanga	5194
5195	BR	Brasil	Mato Grosso	MT	Arenápolis	5195
5196	BR	Brasil	Mato Grosso	MT	Aripuanã	5196
5197	BR	Brasil	Mato Grosso	MT	Barão de Melgaço	5197
5198	BR	Brasil	Mato Grosso	MT	Barra do Bugres	5198
2345	BR	Brasil	Minas Gerais	MG	Buritis	2345
3008	BR	Brasil	Minas Gerais	MG	São Tomás de Aquino	3008
3715	BR	Brasil	São Paulo	SP	Pongaí	3715
3799	BR	Brasil	São Paulo	SP	Santa Rosa de Viterbo	3799
4274	BR	Brasil	Paraná	PR	Sengés	4274
4275	BR	Brasil	Paraná	PR	Serranópolis do Iguaçu	4275
4276	BR	Brasil	Paraná	PR	Sertaneja	4276
4277	BR	Brasil	Paraná	PR	Sertanópolis	4277
4529	BR	Brasil	Santa Catarina	SC	Rio do Sul	4529
4530	BR	Brasil	Santa Catarina	SC	Rio Fortuna	4530
4531	BR	Brasil	Santa Catarina	SC	Rio Negrinho	4531
4532	BR	Brasil	Santa Catarina	SC	Rio Rufino	4532
4534	BR	Brasil	Santa Catarina	SC	Rodeio	4534
4535	BR	Brasil	Santa Catarina	SC	Romelândia	4535
4536	BR	Brasil	Santa Catarina	SC	Salete	4536
4537	BR	Brasil	Santa Catarina	SC	Saltinho	4537
5199	BR	Brasil	Mato Grosso	MT	Barra do Garças	5199
5200	BR	Brasil	Mato Grosso	MT	Bom Jesus do Araguaia	5200
5201	BR	Brasil	Mato Grosso	MT	Brasnorte	5201
5202	BR	Brasil	Mato Grosso	MT	Cáceres	5202
5203	BR	Brasil	Mato Grosso	MT	Campinápolis	5203
5204	BR	Brasil	Mato Grosso	MT	Campo Novo do Parecis	5204
5205	BR	Brasil	Mato Grosso	MT	Campo Verde	5205
5206	BR	Brasil	Mato Grosso	MT	Campos de Júlio	5206
5207	BR	Brasil	Mato Grosso	MT	Canabrava do Norte	5207
5247	BR	Brasil	Mato Grosso	MT	Vila Bela da Santíssima Trindade	5247
5248	BR	Brasil	Mato Grosso	MT	Marcelândia	5248
5301	BR	Brasil	Mato Grosso	MT	Santa Terezinha	5301
5302	BR	Brasil	Mato Grosso	MT	Santo Antônio do Leste	5302
5303	BR	Brasil	Mato Grosso	MT	Santo Antônio do Leverger	5303
5304	BR	Brasil	Mato Grosso	MT	São Félix do Araguaia	5304
5305	BR	Brasil	Mato Grosso	MT	Sapezal	5305
5306	BR	Brasil	Mato Grosso	MT	Serra Nova Dourada	5306
5307	BR	Brasil	Mato Grosso	MT	Sinop	5307
5308	BR	Brasil	Mato Grosso	MT	Sorriso	5308
5309	BR	Brasil	Mato Grosso	MT	Tabaporã	5309
5310	BR	Brasil	Mato Grosso	MT	Tangará da Serra	5310
5311	BR	Brasil	Mato Grosso	MT	Tapurah	5311
5312	BR	Brasil	Mato Grosso	MT	Terra Nova do Norte	5312
5313	BR	Brasil	Mato Grosso	MT	Tesouro	5313
5314	BR	Brasil	Mato Grosso	MT	Torixoréu	5314
5316	BR	Brasil	Mato Grosso	MT	Vale de São Domingos	5316
5501	BR	Brasil	Goiás	GO	Paranaiguara	5501
4367	BR	Brasil	Santa Catarina	SC	Campo Erê	4367
4601	BR	Brasil	Santa Catarina	SC	Witmarsum	4601
4479	BR	Brasil	Santa Catarina	SC	Morro Grande	4479
4480	BR	Brasil	Santa Catarina	SC	Navegantes	4480
4481	BR	Brasil	Santa Catarina	SC	Nova Erechim	4481
4482	BR	Brasil	Santa Catarina	SC	Nova Itaberaba	4482
4483	BR	Brasil	Santa Catarina	SC	Nova Trento	4483
4484	BR	Brasil	Santa Catarina	SC	Nova Veneza	4484
4485	BR	Brasil	Santa Catarina	SC	Novo Horizonte	4485
4486	BR	Brasil	Santa Catarina	SC	Orleans	4486
4487	BR	Brasil	Santa Catarina	SC	Otacílio Costa	4487
4488	BR	Brasil	Santa Catarina	SC	Ouro	4488
4489	BR	Brasil	Santa Catarina	SC	Ouro Verde	4489
4822	BR	Brasil	Rio Grande do Sul	RS	Itatiba do Sul	4822
4823	BR	Brasil	Rio Grande do Sul	RS	Ivorá	4823
4824	BR	Brasil	Rio Grande do Sul	RS	Ivoti	4824
4825	BR	Brasil	Rio Grande do Sul	RS	Jaboticaba	4825
4826	BR	Brasil	Rio Grande do Sul	RS	Jacuizinho	4826
4827	BR	Brasil	Rio Grande do Sul	RS	Jacutinga	4827
4828	BR	Brasil	Rio Grande do Sul	RS	Jaguarão	4828
4829	BR	Brasil	Rio Grande do Sul	RS	Jaguari	4829
4830	BR	Brasil	Rio Grande do Sul	RS	Jaquirana	4830
4832	BR	Brasil	Rio Grande do Sul	RS	Jóia	4832
4833	BR	Brasil	Rio Grande do Sul	RS	Júlio de Castilhos	4833
4834	BR	Brasil	Rio Grande do Sul	RS	Lagoa Bonita do Sul	4834
4835	BR	Brasil	Rio Grande do Sul	RS	Lagoão	4835
4836	BR	Brasil	Rio Grande do Sul	RS	Lagoa Dos Três Cantos	4836
4837	BR	Brasil	Rio Grande do Sul	RS	Lagoa Vermelha	4837
4838	BR	Brasil	Rio Grande do Sul	RS	Lajeado	4838
4839	BR	Brasil	Rio Grande do Sul	RS	Lajeado do Bugre	4839
4840	BR	Brasil	Rio Grande do Sul	RS	Lavras do Sul	4840
4841	BR	Brasil	Rio Grande do Sul	RS	Liberato Salzano	4841
4842	BR	Brasil	Rio Grande do Sul	RS	Lindolfo Collor	4842
4843	BR	Brasil	Rio Grande do Sul	RS	Linha Nova	4843
4844	BR	Brasil	Rio Grande do Sul	RS	Machadinho	4844
5027	BR	Brasil	Rio Grande do Sul	RS	Sarandi	5027
2164	BR	Brasil	Bahia	BA	Santa Bárbara	2164
2338	BR	Brasil	Minas Gerais	MG	Brás Pires	2338
2974	BR	Brasil	Minas Gerais	MG	São João Del Rei	2974
2975	BR	Brasil	Minas Gerais	MG	São João do Manhuaçu	2975
2976	BR	Brasil	Minas Gerais	MG	São João do Manteninha	2976
2977	BR	Brasil	Minas Gerais	MG	São João do Oriente	2977
2978	BR	Brasil	Minas Gerais	MG	São João do Pacuí	2978
2979	BR	Brasil	Minas Gerais	MG	São João do Paraíso	2979
2980	BR	Brasil	Minas Gerais	MG	São João Evangelista	2980
2981	BR	Brasil	Minas Gerais	MG	São João Nepomuceno	2981
2982	BR	Brasil	Minas Gerais	MG	São Joaquim de Bicas	2982
2983	BR	Brasil	Minas Gerais	MG	São José da Barra	2983
2984	BR	Brasil	Minas Gerais	MG	São José da Lapa	2984
2985	BR	Brasil	Minas Gerais	MG	São José da Safira	2985
2986	BR	Brasil	Minas Gerais	MG	São José da Varginha	2986
2987	BR	Brasil	Minas Gerais	MG	São José do Alegre	2987
2988	BR	Brasil	Minas Gerais	MG	São José do Divino	2988
2989	BR	Brasil	Minas Gerais	MG	São José do Goiabal	2989
2990	BR	Brasil	Minas Gerais	MG	São José do Jacuri	2990
2991	BR	Brasil	Minas Gerais	MG	São José do Mantimento	2991
2996	BR	Brasil	Minas Gerais	MG	São Pedro do Suaçuí	2996
2998	BR	Brasil	Minas Gerais	MG	São Roque de Minas	2998
2999	BR	Brasil	Minas Gerais	MG	São Sebastião da Bela Vista	2999
3000	BR	Brasil	Minas Gerais	MG	São Sebastião da Vargem Alegre	3000
3001	BR	Brasil	Minas Gerais	MG	São Sebastião do Anta	3001
3002	BR	Brasil	Minas Gerais	MG	São Sebastião do Maranhão	3002
3003	BR	Brasil	Minas Gerais	MG	São Sebastião do Oeste	3003
3004	BR	Brasil	Minas Gerais	MG	São Sebastião do Paraíso	3004
3005	BR	Brasil	Minas Gerais	MG	São Sebastião do Rio Preto	3005
3012	BR	Brasil	Minas Gerais	MG	Sardoá	3012
3110	BR	Brasil	Espírito Santo	ES	Boa Esperança	3110
4058	BR	Brasil	Paraná	PR	Imbituva	4058
4059	BR	Brasil	Paraná	PR	Inácio Martins	4059
4889	BR	Brasil	Rio Grande do Sul	RS	Nova Ramada	4889
4890	BR	Brasil	Rio Grande do Sul	RS	Nova Roma do Sul	4890
4891	BR	Brasil	Rio Grande do Sul	RS	Nova Santa Rita	4891
4892	BR	Brasil	Rio Grande do Sul	RS	Novo Cabrais	4892
5098	BR	Brasil	Rio Grande do Sul	RS	Vista Alegre	5098
5099	BR	Brasil	Rio Grande do Sul	RS	Vista Alegre do Prata	5099
5100	BR	Brasil	Rio Grande do Sul	RS	Vista Gaúcha	5100
5101	BR	Brasil	Rio Grande do Sul	RS	Vitória Das Missões	5101
5103	BR	Brasil	Rio Grande do Sul	RS	Xangri-lá	5103
5104	BR	Brasil	Mato Grosso do Sul	MS	Água Clara	5104
5105	BR	Brasil	Mato Grosso do Sul	MS	Alcinópolis	5105
5168	BR	Brasil	Mato Grosso do Sul	MS	Rio Brilhante	5168
5169	BR	Brasil	Mato Grosso do Sul	MS	Rio Negro	5169
5170	BR	Brasil	Mato Grosso do Sul	MS	Rio Verde de Mato Grosso	5170
5171	BR	Brasil	Mato Grosso do Sul	MS	Rochedo	5171
5172	BR	Brasil	Mato Grosso do Sul	MS	Santa Rita do Pardo	5172
5173	BR	Brasil	Mato Grosso do Sul	MS	São Gabriel do Oeste	5173
5174	BR	Brasil	Mato Grosso do Sul	MS	Sete Quedas	5174
5175	BR	Brasil	Mato Grosso do Sul	MS	Selvíria	5175
5176	BR	Brasil	Mato Grosso do Sul	MS	Sidrolândia	5176
5177	BR	Brasil	Mato Grosso do Sul	MS	Sonora	5177
5178	BR	Brasil	Mato Grosso do Sul	MS	Tacuru	5178
5179	BR	Brasil	Mato Grosso do Sul	MS	Taquarussu	5179
5180	BR	Brasil	Mato Grosso do Sul	MS	Terenos	5180
5249	BR	Brasil	Mato Grosso	MT	Matupá	5249
5250	BR	Brasil	Mato Grosso	MT	Mirassol D´oeste	5250
5251	BR	Brasil	Mato Grosso	MT	Nobres	5251
5252	BR	Brasil	Mato Grosso	MT	Nortelândia	5252
5253	BR	Brasil	Mato Grosso	MT	Nossa Senhora do Livramento	5253
5254	BR	Brasil	Mato Grosso	MT	Nova Bandeirantes	5254
5290	BR	Brasil	Mato Grosso	MT	Santo Afonso	5290
5292	BR	Brasil	Mato Grosso	MT	São José do Rio Claro	5292
5293	BR	Brasil	Mato Grosso	MT	São José do Xingu	5293
5294	BR	Brasil	Mato Grosso	MT	São Pedro da Cipa	5294
5295	BR	Brasil	Mato Grosso	MT	Rondolândia	5295
5296	BR	Brasil	Mato Grosso	MT	Rondonópolis	5296
5297	BR	Brasil	Mato Grosso	MT	Rosário Oeste	5297
5298	BR	Brasil	Mato Grosso	MT	Santa Cruz do Xingu	5298
5299	BR	Brasil	Mato Grosso	MT	Salto do Céu	5299
5300	BR	Brasil	Mato Grosso	MT	Santa Rita do Trivelato	5300
5317	BR	Brasil	Mato Grosso	MT	Várzea Grande	5317
5318	BR	Brasil	Mato Grosso	MT	Vera	5318
5319	BR	Brasil	Mato Grosso	MT	Vila Rica	5319
5320	BR	Brasil	Mato Grosso	MT	Nova Guarita	5320
5321	BR	Brasil	Mato Grosso	MT	Nova Marilândia	5321
5322	BR	Brasil	Mato Grosso	MT	Nova Maringá	5322
5323	BR	Brasil	Mato Grosso	MT	Nova Monte Verde	5323
5353	BR	Brasil	Goiás	GO	Baliza	5353
5373	BR	Brasil	Goiás	GO	Campestre de Goiás	5373
5374	BR	Brasil	Goiás	GO	Campinaçu	5374
5375	BR	Brasil	Goiás	GO	Campinorte	5375
5376	BR	Brasil	Goiás	GO	Campo Alegre de Goiás	5376
2045	BR	Brasil	Bahia	BA	Juazeiro	2045
2490	BR	Brasil	Minas Gerais	MG	Divinolândia de Minas	2490
2665	BR	Brasil	Minas Gerais	MG	Juramento	2665
2666	BR	Brasil	Minas Gerais	MG	Juruaia	2666
3240	BR	Brasil	Rio de Janeiro	RJ	Rio Claro	3240
3241	BR	Brasil	Rio de Janeiro	RJ	Rio Das Flores	3241
3242	BR	Brasil	Rio de Janeiro	RJ	Rio Das Ostras	3242
3350	BR	Brasil	São Paulo	SP	Boracéia	3350
3351	BR	Brasil	São Paulo	SP	Borborema	3351
3352	BR	Brasil	São Paulo	SP	Borebi	3352
3353	BR	Brasil	São Paulo	SP	Botucatu	3353
3354	BR	Brasil	São Paulo	SP	Bragança Paulista	3354
3355	BR	Brasil	São Paulo	SP	Braúna	3355
3356	BR	Brasil	São Paulo	SP	Brejo Alegre	3356
4369	BR	Brasil	Santa Catarina	SC	Canelinha	4369
4370	BR	Brasil	Santa Catarina	SC	Canoinhas	4370
4371	BR	Brasil	Santa Catarina	SC	Capinzal	4371
4372	BR	Brasil	Santa Catarina	SC	Capivari de Baixo	4372
4373	BR	Brasil	Santa Catarina	SC	Catanduvas	4373
4374	BR	Brasil	Santa Catarina	SC	Caxambu do Sul	4374
4376	BR	Brasil	Santa Catarina	SC	Cerro Negro	4376
4377	BR	Brasil	Santa Catarina	SC	Chapadão do Lageado	4377
4378	BR	Brasil	Santa Catarina	SC	Chapecó	4378
4379	BR	Brasil	Santa Catarina	SC	Cocal do Sul	4379
4380	BR	Brasil	Santa Catarina	SC	Concórdia	4380
4381	BR	Brasil	Santa Catarina	SC	Cordilheira Alta	4381
4406	BR	Brasil	Santa Catarina	SC	Garuva	4406
5072	BR	Brasil	Rio Grande do Sul	RS	Tupanci do Sul	5072
5073	BR	Brasil	Rio Grande do Sul	RS	Tupanciretã	5073
5074	BR	Brasil	Rio Grande do Sul	RS	Tupandi	5074
5075	BR	Brasil	Rio Grande do Sul	RS	Tuparendi	5075
5076	BR	Brasil	Rio Grande do Sul	RS	Turuçu	5076
5077	BR	Brasil	Rio Grande do Sul	RS	Ubiretama	5077
5078	BR	Brasil	Rio Grande do Sul	RS	União da Serra	5078
5079	BR	Brasil	Rio Grande do Sul	RS	Unistalda	5079
5080	BR	Brasil	Rio Grande do Sul	RS	Uruguaiana	5080
5081	BR	Brasil	Rio Grande do Sul	RS	Vacaria	5081
5082	BR	Brasil	Rio Grande do Sul	RS	Vale Verde	5082
5083	BR	Brasil	Rio Grande do Sul	RS	Vale do Sol	5083
5084	BR	Brasil	Rio Grande do Sul	RS	Vale Real	5084
5085	BR	Brasil	Rio Grande do Sul	RS	Vanini	5085
5086	BR	Brasil	Rio Grande do Sul	RS	Venâncio Aires	5086
5087	BR	Brasil	Rio Grande do Sul	RS	Vera Cruz	5087
5181	BR	Brasil	Mato Grosso do Sul	MS	Três Lagoas	5181
5182	BR	Brasil	Mato Grosso do Sul	MS	Vicentina	5182
5184	BR	Brasil	Mato Grosso	MT	Água Boa	5184
5185	BR	Brasil	Mato Grosso	MT	Alta Floresta	5185
5186	BR	Brasil	Mato Grosso	MT	Alto Araguaia	5186
5187	BR	Brasil	Mato Grosso	MT	Alto Boa Vista	5187
5188	BR	Brasil	Mato Grosso	MT	Alto Garças	5188
5189	BR	Brasil	Mato Grosso	MT	Alto Paraguai	5189
5190	BR	Brasil	Mato Grosso	MT	Alto Taquari	5190
5191	BR	Brasil	Mato Grosso	MT	Apiacás	5191
5192	BR	Brasil	Mato Grosso	MT	Araguaiana	5192
2371	BR	Brasil	Minas Gerais	MG	Canaã	2371
2809	BR	Brasil	Minas Gerais	MG	Paulistas	2809
2969	BR	Brasil	Minas Gerais	MG	São João Batista do Glória	2969
3007	BR	Brasil	Minas Gerais	MG	São Tiago	3007
3592	BR	Brasil	São Paulo	SP	Marapoama	3592
3593	BR	Brasil	São Paulo	SP	Mariápolis	3593
3594	BR	Brasil	São Paulo	SP	Marília	3594
3595	BR	Brasil	São Paulo	SP	Marinópolis	3595
3695	BR	Brasil	São Paulo	SP	Pindamonhangaba	3695
3696	BR	Brasil	São Paulo	SP	Pindorama	3696
3697	BR	Brasil	São Paulo	SP	Pinhalzinho	3697
3698	BR	Brasil	São Paulo	SP	Piquerobi	3698
3699	BR	Brasil	São Paulo	SP	Piquete	3699
3700	BR	Brasil	São Paulo	SP	Piracaia	3700
3701	BR	Brasil	São Paulo	SP	Piracicaba	3701
3702	BR	Brasil	São Paulo	SP	Piraju	3702
4792	BR	Brasil	Rio Grande do Sul	RS	Gravataí	4792
4793	BR	Brasil	Rio Grande do Sul	RS	Guabiju	4793
4794	BR	Brasil	Rio Grande do Sul	RS	Guaíba	4794
4795	BR	Brasil	Rio Grande do Sul	RS	Guaporé	4795
4796	BR	Brasil	Rio Grande do Sul	RS	Guarani Das Missões	4796
4797	BR	Brasil	Rio Grande do Sul	RS	Harmonia	4797
4798	BR	Brasil	Rio Grande do Sul	RS	Herveiras	4798
4799	BR	Brasil	Rio Grande do Sul	RS	Horizontina	4799
4800	BR	Brasil	Rio Grande do Sul	RS	Hulha Negra	4800
4801	BR	Brasil	Rio Grande do Sul	RS	Humaitá	4801
4802	BR	Brasil	Rio Grande do Sul	RS	Ibarama	4802
4803	BR	Brasil	Rio Grande do Sul	RS	Ibiaçá	4803
4804	BR	Brasil	Rio Grande do Sul	RS	Ibiraiaras	4804
4805	BR	Brasil	Rio Grande do Sul	RS	Ibirapuitã	4805
4806	BR	Brasil	Rio Grande do Sul	RS	Ibirubá	4806
3924	BR	Brasil	Paraná	PR	Anahy	3924
4955	BR	Brasil	Rio Grande do Sul	RS	Rolador	4955
4027	BR	Brasil	Paraná	PR	Floresta	4027
5049	BR	Brasil	Rio Grande do Sul	RS	Taquari	5049
5051	BR	Brasil	Rio Grande do Sul	RS	Tavares	5051
4225	BR	Brasil	Paraná	PR	Rondon	4225
5183	BR	Brasil	Mato Grosso	MT	Acorizal	5183
2918	BR	Brasil	Minas Gerais	MG	Santa Juliana	2918
3323	BR	Brasil	São Paulo	SP	Bananal	3323
3495	BR	Brasil	São Paulo	SP	Iepê	3495
3496	BR	Brasil	São Paulo	SP	Igaraçu do Tietê	3496
4181	BR	Brasil	Paraná	PR	Piraí do Sul	4181
4192	BR	Brasil	Paraná	PR	Porto Rico	4192
4193	BR	Brasil	Paraná	PR	Porto Vitória	4193
4194	BR	Brasil	Paraná	PR	Prado Ferreira	4194
4335	BR	Brasil	Santa Catarina	SC	Atalanta	4335
4336	BR	Brasil	Santa Catarina	SC	Aurora	4336
4337	BR	Brasil	Santa Catarina	SC	Balneário Arroio do Silva	4337
4338	BR	Brasil	Santa Catarina	SC	Balneário Camboriú	4338
4339	BR	Brasil	Santa Catarina	SC	Balneário Barra do Sul	4339
4340	BR	Brasil	Santa Catarina	SC	Balneário Gaivota	4340
4341	BR	Brasil	Santa Catarina	SC	Bandeirante	4341
5502	BR	Brasil	Goiás	GO	Paraúna	5502
5503	BR	Brasil	Goiás	GO	Perolândia	5503
5504	BR	Brasil	Goiás	GO	Petrolina de Goiás	5504
5505	BR	Brasil	Goiás	GO	Pilar de Goiás	5505
5557	BR	Brasil	Goiás	GO	Trombas	5557
3645	BR	Brasil	São Paulo	SP	Nova Odessa	3645
3825	BR	Brasil	São Paulo	SP	São José Dos Campos	3825
4543	BR	Brasil	Santa Catarina	SC	Santa Rosa do Sul	4543
4571	BR	Brasil	Santa Catarina	SC	Seara	4571
4652	BR	Brasil	Rio Grande do Sul	RS	Boa Vista do Cadeado	4652
4653	BR	Brasil	Rio Grande do Sul	RS	Boa Vista do Incra	4653
4654	BR	Brasil	Rio Grande do Sul	RS	Boa Vista do Sul	4654
4287	BR	Brasil	Paraná	PR	Terra Rica	4287
4937	BR	Brasil	Rio Grande do Sul	RS	Pouso Novo	4937
5025	BR	Brasil	Rio Grande do Sul	RS	Sapiranga	5025
5026	BR	Brasil	Rio Grande do Sul	RS	Sapucaia do Sul	5026
5208	BR	Brasil	Mato Grosso	MT	Canarana	5208
5209	BR	Brasil	Mato Grosso	MT	Carlinda	5209
5210	BR	Brasil	Mato Grosso	MT	Castanheira	5210
5211	BR	Brasil	Mato Grosso	MT	Chapada Dos Guimarães	5211
5212	BR	Brasil	Mato Grosso	MT	Cláudia	5212
5213	BR	Brasil	Mato Grosso	MT	Cocalinho	5213
5214	BR	Brasil	Mato Grosso	MT	Colíder	5214
5215	BR	Brasil	Mato Grosso	MT	Colniza	5215
5216	BR	Brasil	Mato Grosso	MT	Comodoro	5216
5217	BR	Brasil	Mato Grosso	MT	Confresa	5217
5218	BR	Brasil	Mato Grosso	MT	Conquista D´oeste	5218
5219	BR	Brasil	Mato Grosso	MT	Cotriguaçu	5219
5220	BR	Brasil	Mato Grosso	MT	Cuiabá	5220
5221	BR	Brasil	Mato Grosso	MT	Curvelândia	5221
5222	BR	Brasil	Mato Grosso	MT	Denise	5222
5223	BR	Brasil	Mato Grosso	MT	Diamantino	5223
5224	BR	Brasil	Mato Grosso	MT	Dom Aquino	5224
5225	BR	Brasil	Mato Grosso	MT	Feliz Natal	5225
5226	BR	Brasil	Mato Grosso	MT	Figueirópolis D´oeste	5226
5227	BR	Brasil	Mato Grosso	MT	Gaúcha do Norte	5227
5228	BR	Brasil	Mato Grosso	MT	General Carneiro	5228
5229	BR	Brasil	Mato Grosso	MT	Glória D´oeste	5229
5230	BR	Brasil	Mato Grosso	MT	Guarantã do Norte	5230
5231	BR	Brasil	Mato Grosso	MT	Guiratinga	5231
5232	BR	Brasil	Mato Grosso	MT	Indiavaí	5232
5233	BR	Brasil	Mato Grosso	MT	Ipiranga do Norte	5233
5234	BR	Brasil	Mato Grosso	MT	Itanhangá	5234
5235	BR	Brasil	Mato Grosso	MT	Itaúba	5235
5236	BR	Brasil	Mato Grosso	MT	Itiquira	5236
5237	BR	Brasil	Mato Grosso	MT	Jaciara	5237
5238	BR	Brasil	Mato Grosso	MT	Jangada	5238
5239	BR	Brasil	Mato Grosso	MT	Jauru	5239
5240	BR	Brasil	Mato Grosso	MT	Juara	5240
5241	BR	Brasil	Mato Grosso	MT	Juína	5241
5242	BR	Brasil	Mato Grosso	MT	Juruena	5242
5243	BR	Brasil	Mato Grosso	MT	Juscimeira	5243
5244	BR	Brasil	Mato Grosso	MT	Lambari D´oeste	5244
5245	BR	Brasil	Mato Grosso	MT	Lucas do Rio Verde	5245
5246	BR	Brasil	Mato Grosso	MT	Luciára	5246
5291	BR	Brasil	Mato Grosso	MT	São José do Povo	5291
4604	BR	Brasil	Santa Catarina	SC	Xaxim	4604
5384	BR	Brasil	Goiás	GO	Cavalcante	5384
5385	BR	Brasil	Goiás	GO	Ceres	5385
5391	BR	Brasil	Goiás	GO	Córrego do Ouro	5391
5392	BR	Brasil	Goiás	GO	Corumbá de Goiás	5392
5393	BR	Brasil	Goiás	GO	Corumbaíba	5393
5394	BR	Brasil	Goiás	GO	Cristalina	5394
5395	BR	Brasil	Goiás	GO	Cristianópolis	5395
5396	BR	Brasil	Goiás	GO	Crixás	5396
5400	BR	Brasil	Goiás	GO	Damolândia	5400
5401	BR	Brasil	Goiás	GO	Davinópolis	5401
5406	BR	Brasil	Goiás	GO	Estrela do Norte	5406
5407	BR	Brasil	Goiás	GO	Faina	5407
5408	BR	Brasil	Goiás	GO	Fazenda Nova	5408
5409	BR	Brasil	Goiás	GO	Firminópolis	5409
5410	BR	Brasil	Goiás	GO	Flores de Goiás	5410
5411	BR	Brasil	Goiás	GO	Formosa	5411
5415	BR	Brasil	Goiás	GO	Goianápolis	5415
5416	BR	Brasil	Goiás	GO	Goiandira	5416
5417	BR	Brasil	Goiás	GO	Goianésia	5417
5419	BR	Brasil	Goiás	GO	Goianira	5419
5424	BR	Brasil	Goiás	GO	Guaraíta	5424
5425	BR	Brasil	Goiás	GO	Guarani de Goiás	5425
5426	BR	Brasil	Goiás	GO	Guarinos	5426
5457	BR	Brasil	Goiás	GO	Leopoldo de Bulhões	5457
5459	BR	Brasil	Goiás	GO	Mairipotaba	5459
5460	BR	Brasil	Goiás	GO	Mambaí	5460
5477	BR	Brasil	Goiás	GO	Mundo Novo	5477
5478	BR	Brasil	Goiás	GO	Mutunópolis	5478
5479	BR	Brasil	Goiás	GO	Nazário	5479
5480	BR	Brasil	Goiás	GO	Nerópolis	5480
5481	BR	Brasil	Goiás	GO	Niquelândia	5481
5482	BR	Brasil	Goiás	GO	Nova América	5482
5483	BR	Brasil	Goiás	GO	Nova Aurora	5483
5484	BR	Brasil	Goiás	GO	Nova Crixás	5484
5485	BR	Brasil	Goiás	GO	Nova Glória	5485
5486	BR	Brasil	Goiás	GO	Nova Iguaçu de Goiás	5486
5487	BR	Brasil	Goiás	GO	Nova Roma	5487
5488	BR	Brasil	Goiás	GO	Nova Veneza	5488
5489	BR	Brasil	Goiás	GO	Novo Brasil	5489
5490	BR	Brasil	Goiás	GO	Novo Gama	5490
5491	BR	Brasil	Goiás	GO	Novo Planalto	5491
5492	BR	Brasil	Goiás	GO	Orizona	5492
5493	BR	Brasil	Goiás	GO	Ouro Verde de Goiás	5493
5494	BR	Brasil	Goiás	GO	Ouvidor	5494
5495	BR	Brasil	Goiás	GO	Padre Bernardo	5495
5496	BR	Brasil	Goiás	GO	Palestina de Goiás	5496
5497	BR	Brasil	Goiás	GO	Palmeiras de Goiás	5497
5498	BR	Brasil	Goiás	GO	Palmelo	5498
5499	BR	Brasil	Goiás	GO	Palminópolis	5499
4831	BR	Brasil	Rio Grande do Sul	RS	Jari	4831
4977	BR	Brasil	Rio Grande do Sul	RS	Santa Tereza	4977
4533	BR	Brasil	Santa Catarina	SC	Riqueza	4533
4911	BR	Brasil	Rio Grande do Sul	RS	Passo Fundo	4911
5069	BR	Brasil	Rio Grande do Sul	RS	Triunfo	5069
5070	BR	Brasil	Rio Grande do Sul	RS	Tucunduva	5070
5255	BR	Brasil	Mato Grosso	MT	Nova Nazaré	5255
5256	BR	Brasil	Mato Grosso	MT	Nova Lacerda	5256
5257	BR	Brasil	Mato Grosso	MT	Nova Santa Helena	5257
5258	BR	Brasil	Mato Grosso	MT	Nova Brasilândia	5258
5259	BR	Brasil	Mato Grosso	MT	Nova Canaã do Norte	5259
5260	BR	Brasil	Mato Grosso	MT	Nova Mutum	5260
5261	BR	Brasil	Mato Grosso	MT	Nova Olímpia	5261
5262	BR	Brasil	Mato Grosso	MT	Nova Ubiratã	5262
5263	BR	Brasil	Mato Grosso	MT	Nova Xavantina	5263
5264	BR	Brasil	Mato Grosso	MT	Novo Mundo	5264
5265	BR	Brasil	Mato Grosso	MT	Novo Horizonte do Norte	5265
5266	BR	Brasil	Mato Grosso	MT	Novo São Joaquim	5266
5267	BR	Brasil	Mato Grosso	MT	Paranaíta	5267
5268	BR	Brasil	Mato Grosso	MT	Paranatinga	5268
5269	BR	Brasil	Mato Grosso	MT	Novo Santo Antônio	5269
5270	BR	Brasil	Mato Grosso	MT	Pedra Preta	5270
5271	BR	Brasil	Mato Grosso	MT	Peixoto de Azevedo	5271
5272	BR	Brasil	Mato Grosso	MT	Planalto da Serra	5272
5273	BR	Brasil	Mato Grosso	MT	Poconé	5273
5274	BR	Brasil	Mato Grosso	MT	Pontal do Araguaia	5274
5275	BR	Brasil	Mato Grosso	MT	Ponte Branca	5275
5276	BR	Brasil	Mato Grosso	MT	Pontes e Lacerda	5276
5277	BR	Brasil	Mato Grosso	MT	Porto Alegre do Norte	5277
5278	BR	Brasil	Mato Grosso	MT	Porto Dos Gaúchos	5278
5279	BR	Brasil	Mato Grosso	MT	Porto Esperidião	5279
5280	BR	Brasil	Mato Grosso	MT	Porto Estrela	5280
5281	BR	Brasil	Mato Grosso	MT	Poxoréo	5281
5282	BR	Brasil	Mato Grosso	MT	Primavera do Leste	5282
5283	BR	Brasil	Mato Grosso	MT	Querência	5283
5284	BR	Brasil	Mato Grosso	MT	São José Dos Quatro Marcos	5284
5285	BR	Brasil	Mato Grosso	MT	Reserva do Cabaçal	5285
5286	BR	Brasil	Mato Grosso	MT	Ribeirão Cascalheira	5286
5287	BR	Brasil	Mato Grosso	MT	Ribeirãozinho	5287
5288	BR	Brasil	Mato Grosso	MT	Rio Branco	5288
5289	BR	Brasil	Mato Grosso	MT	Santa Carmem	5289
5315	BR	Brasil	Mato Grosso	MT	União do Sul	5315
5326	BR	Brasil	Goiás	GO	Acreúna	5326
5350	BR	Brasil	Goiás	GO	Aruanã	5350
5427	BR	Brasil	Goiás	GO	Heitoraí	5427
5428	BR	Brasil	Goiás	GO	Hidrolândia	5428
5429	BR	Brasil	Goiás	GO	Hidrolina	5429
5430	BR	Brasil	Goiás	GO	Iaciara	5430
5431	BR	Brasil	Goiás	GO	Inaciolândia	5431
5432	BR	Brasil	Goiás	GO	Indiara	5432
5433	BR	Brasil	Goiás	GO	Inhumas	5433
5434	BR	Brasil	Goiás	GO	Ipameri	5434
5435	BR	Brasil	Goiás	GO	Ipiranga de Goiás	5435
5436	BR	Brasil	Goiás	GO	Iporá	5436
5438	BR	Brasil	Goiás	GO	Itaberaí	5438
5440	BR	Brasil	Goiás	GO	Itaguaru	5440
5442	BR	Brasil	Goiás	GO	Itapaci	5442
5443	BR	Brasil	Goiás	GO	Itapirapuã	5443
5444	BR	Brasil	Goiás	GO	Itapuranga	5444
5445	BR	Brasil	Goiás	GO	Itarumã	5445
5446	BR	Brasil	Goiás	GO	Itauçu	5446
5447	BR	Brasil	Goiás	GO	Itumbiara	5447
5448	BR	Brasil	Goiás	GO	Ivolândia	5448
5449	BR	Brasil	Goiás	GO	Jandaia	5449
5450	BR	Brasil	Goiás	GO	Jaraguá	5450
5451	BR	Brasil	Goiás	GO	Jataí	5451
5452	BR	Brasil	Goiás	GO	Jaupaci	5452
5453	BR	Brasil	Goiás	GO	Jesúpolis	5453
5454	BR	Brasil	Goiás	GO	Joviânia	5454
5455	BR	Brasil	Goiás	GO	Jussara	5455
5461	BR	Brasil	Goiás	GO	Mara Rosa	5461
5462	BR	Brasil	Goiás	GO	Marzagão	5462
5463	BR	Brasil	Goiás	GO	Matrinchã	5463
5464	BR	Brasil	Goiás	GO	Maurilândia	5464
5465	BR	Brasil	Goiás	GO	Mimoso de Goiás	5465
5466	BR	Brasil	Goiás	GO	Minaçu	5466
5467	BR	Brasil	Goiás	GO	Mineiros	5467
5468	BR	Brasil	Goiás	GO	Moiporá	5468
5469	BR	Brasil	Goiás	GO	Monte Alegre de Goiás	5469
5470	BR	Brasil	Goiás	GO	Montes Claros de Goiás	5470
5471	BR	Brasil	Goiás	GO	Montividiu	5471
5472	BR	Brasil	Goiás	GO	Montividiu do Norte	5472
5473	BR	Brasil	Goiás	GO	Morrinhos	5473
5474	BR	Brasil	Goiás	GO	Morro Agudo de Goiás	5474
5475	BR	Brasil	Goiás	GO	Mossâmedes	5475
5476	BR	Brasil	Goiás	GO	Mozarlândia	5476
4989	BR	Brasil	Rio Grande do Sul	RS	São Domingos do Sul	4989
4990	BR	Brasil	Rio Grande do Sul	RS	São Francisco de Assis	4990
4991	BR	Brasil	Rio Grande do Sul	RS	São Francisco de Paula	4991
4992	BR	Brasil	Rio Grande do Sul	RS	São Gabriel	4992
4993	BR	Brasil	Rio Grande do Sul	RS	São Jerônimo	4993
5358	BR	Brasil	Goiás	GO	Bonfinópolis	5358
5359	BR	Brasil	Goiás	GO	Bonópolis	5359
5360	BR	Brasil	Goiás	GO	Brazabrantes	5360
5361	BR	Brasil	Goiás	GO	Britânia	5361
5362	BR	Brasil	Goiás	GO	Buriti Alegre	5362
5363	BR	Brasil	Goiás	GO	Buriti de Goiás	5363
5364	BR	Brasil	Goiás	GO	Buritinópolis	5364
5365	BR	Brasil	Goiás	GO	Cabeceiras	5365
5366	BR	Brasil	Goiás	GO	Cachoeira Alta	5366
5367	BR	Brasil	Goiás	GO	Cachoeira de Goiás	5367
5368	BR	Brasil	Goiás	GO	Cachoeira Dourada	5368
5369	BR	Brasil	Goiás	GO	Caçu	5369
5370	BR	Brasil	Goiás	GO	Caiapônia	5370
5371	BR	Brasil	Goiás	GO	Caldas Novas	5371
5372	BR	Brasil	Goiás	GO	Caldazinha	5372
5377	BR	Brasil	Goiás	GO	Campo Limpo de Goiás	5377
5378	BR	Brasil	Goiás	GO	Campos Belos	5378
5379	BR	Brasil	Goiás	GO	Campos Verdes	5379
5380	BR	Brasil	Goiás	GO	Carmo do Rio Verde	5380
5386	BR	Brasil	Goiás	GO	Cezarina	5386
5387	BR	Brasil	Goiás	GO	Chapadão do Céu	5387
5388	BR	Brasil	Goiás	GO	Cidade Ocidental	5388
5389	BR	Brasil	Goiás	GO	Cocalzinho de Goiás	5389
5390	BR	Brasil	Goiás	GO	Colinas do Sul	5390
5397	BR	Brasil	Goiás	GO	Cromínia	5397
5398	BR	Brasil	Goiás	GO	Cumari	5398
5399	BR	Brasil	Goiás	GO	Damianópolis	5399
5402	BR	Brasil	Goiás	GO	Diorama	5402
5403	BR	Brasil	Goiás	GO	Doverlândia	5403
5404	BR	Brasil	Goiás	GO	Edealina	5404
5405	BR	Brasil	Goiás	GO	Edéia	5405
5412	BR	Brasil	Goiás	GO	Formoso	5412
5413	BR	Brasil	Goiás	GO	Gameleira de Goiás	5413
5414	BR	Brasil	Goiás	GO	Divinópolis de Goiás	5414
5418	BR	Brasil	Goiás	GO	Goiânia	5418
5420	BR	Brasil	Goiás	GO	Goiás	5420
5422	BR	Brasil	Goiás	GO	Gouvelândia	5422
5423	BR	Brasil	Goiás	GO	Guapó	5423
5437	BR	Brasil	Goiás	GO	Israelândia	5437
5439	BR	Brasil	Goiás	GO	Itaguari	5439
5441	BR	Brasil	Goiás	GO	Itajá	5441
5456	BR	Brasil	Goiás	GO	Lagoa Santa	5456
5458	BR	Brasil	Goiás	GO	Luziânia	5458
5324	BR	Brasil	Goiás	GO	Abadia de Goiás	5324
5325	BR	Brasil	Goiás	GO	Abadiânia	5325
5327	BR	Brasil	Goiás	GO	Adelândia	5327
5328	BR	Brasil	Goiás	GO	Água Fria de Goiás	5328
5329	BR	Brasil	Goiás	GO	Água Limpa	5329
5330	BR	Brasil	Goiás	GO	Águas Lindas de Goiás	5330
5331	BR	Brasil	Goiás	GO	Alexânia	5331
5332	BR	Brasil	Goiás	GO	Aloândia	5332
5333	BR	Brasil	Goiás	GO	Alto Horizonte	5333
5334	BR	Brasil	Goiás	GO	Alto Paraíso de Goiás	5334
5335	BR	Brasil	Goiás	GO	Alvorada do Norte	5335
5336	BR	Brasil	Goiás	GO	Amaralina	5336
5337	BR	Brasil	Goiás	GO	Americano do Brasil	5337
5338	BR	Brasil	Goiás	GO	Amorinópolis	5338
5339	BR	Brasil	Goiás	GO	Anápolis	5339
5340	BR	Brasil	Goiás	GO	Anhanguera	5340
5341	BR	Brasil	Goiás	GO	Anicuns	5341
5342	BR	Brasil	Goiás	GO	Aparecida de Goiânia	5342
5343	BR	Brasil	Goiás	GO	Aparecida do Rio Doce	5343
5344	BR	Brasil	Goiás	GO	Aporé	5344
5345	BR	Brasil	Goiás	GO	Araçu	5345
5346	BR	Brasil	Goiás	GO	Aragarças	5346
5347	BR	Brasil	Goiás	GO	Aragoiânia	5347
5348	BR	Brasil	Goiás	GO	Araguapaz	5348
5349	BR	Brasil	Goiás	GO	Arenópolis	5349
5351	BR	Brasil	Goiás	GO	Aurilândia	5351
5352	BR	Brasil	Goiás	GO	Avelinópolis	5352
5354	BR	Brasil	Goiás	GO	Barro Alto	5354
5355	BR	Brasil	Goiás	GO	Bela Vista de Goiás	5355
5356	BR	Brasil	Goiás	GO	Bom Jardim de Goiás	5356
5357	BR	Brasil	Goiás	GO	Bom Jesus de Goiás	5357
5421	BR	Brasil	Goiás	GO	Goiatuba	5421
5506	BR	Brasil	Goiás	GO	Piracanjuba	5506
5545	BR	Brasil	Goiás	GO	São Patrício	5545
5558	BR	Brasil	Goiás	GO	Turvânia	5558
5559	BR	Brasil	Goiás	GO	Turvelândia	5559
5560	BR	Brasil	Goiás	GO	Uirapuru	5560
5561	BR	Brasil	Goiás	GO	Uruaçu	5561
5562	BR	Brasil	Goiás	GO	Uruana	5562
5563	BR	Brasil	Goiás	GO	Urutaí	5563
5564	BR	Brasil	Goiás	GO	Valparaíso de Goiás	5564
5565	BR	Brasil	Goiás	GO	Varjão	5565
5566	BR	Brasil	Goiás	GO	Vianópolis	5566
5567	BR	Brasil	Goiás	GO	Vicentinópolis	5567
5568	BR	Brasil	Goiás	GO	Vila Boa	5568
5569	BR	Brasil	Goiás	GO	Vila Propício	5569
5570	BR	Brasil	Distrito Federal	DF	Brasília	5570
\.


--
-- Data for Name: aggregation_type; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.aggregation_type (id, name, "order") FROM stdin;
1	sum	1
2	avg	1
3	percent	1
4	max	1
5	min	1
6	count	1
\.


--
-- Data for Name: attachments; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.attachments (id, created_at, updated_at, file, bucket, file_attachments_path, file_url, file_size, date, field_id, form_id) FROM stdin;
\.


--
-- Data for Name: auth_group; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.auth_group (id, name) FROM stdin;
\.


--
-- Data for Name: auth_group_permissions; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.auth_group_permissions (id, group_id, permission_id) FROM stdin;
\.


--
-- Data for Name: auth_permission; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.auth_permission (id, name, content_type_id, codename) FROM stdin;
1	Can add user extended	1	add_userextended
2	Can change user extended	1	change_userextended
3	Can delete user extended	1	delete_userextended
4	Can view user extended	1	view_userextended
5	Can add company	2	add_company
6	Can change company	2	change_company
7	Can delete company	2	delete_company
8	Can view company	2	view_company
9	Can add company type	3	add_companytype
10	Can change company type	3	change_companytype
11	Can delete company type	3	delete_companytype
12	Can view company type	3	view_companytype
13	Can add profile type	4	add_profiletype
14	Can change profile type	4	change_profiletype
15	Can delete profile type	4	delete_profiletype
16	Can view profile type	4	view_profiletype
17	Can add visualization type	5	add_visualizationtype
18	Can change visualization type	5	change_visualizationtype
19	Can delete visualization type	5	delete_visualizationtype
20	Can view visualization type	5	view_visualizationtype
21	Can add address helper	6	add_addresshelper
22	Can change address helper	6	change_addresshelper
23	Can delete address helper	6	delete_addresshelper
24	Can view address helper	6	view_addresshelper
25	Can add public access	7	add_publicaccess
26	Can change public access	7	change_publicaccess
27	Can delete public access	7	delete_publicaccess
28	Can view public access	7	view_publicaccess
29	Can add charge frequency type	8	add_chargefrequencytype
30	Can change charge frequency type	8	change_chargefrequencytype
31	Can delete charge frequency type	8	delete_chargefrequencytype
32	Can view charge frequency type	8	view_chargefrequencytype
33	Can add charge type	9	add_chargetype
34	Can change charge type	9	change_chargetype
35	Can delete charge type	9	delete_chargetype
36	Can view charge type	9	view_chargetype
37	Can add discount coupon	10	add_discountcoupon
38	Can change discount coupon	10	change_discountcoupon
39	Can delete discount coupon	10	delete_discountcoupon
40	Can view discount coupon	10	view_discountcoupon
41	Can add invoice date type	11	add_invoicedatetype
42	Can change invoice date type	11	change_invoicedatetype
43	Can delete invoice date type	11	delete_invoicedatetype
44	Can view invoice date type	11	view_invoicedatetype
45	Can add payment method type	12	add_paymentmethodtype
46	Can change payment method type	12	change_paymentmethodtype
47	Can delete payment method type	12	delete_paymentmethodtype
48	Can view payment method type	12	view_paymentmethodtype
49	Can add individual charge value type	13	add_individualchargevaluetype
50	Can change individual charge value type	13	change_individualchargevaluetype
51	Can delete individual charge value type	13	delete_individualchargevaluetype
52	Can view individual charge value type	13	view_individualchargevaluetype
53	Can add discount by individual value quantity	14	add_discountbyindividualvaluequantity
54	Can change discount by individual value quantity	14	change_discountbyindividualvaluequantity
55	Can delete discount by individual value quantity	14	delete_discountbyindividualvaluequantity
56	Can view discount by individual value quantity	14	view_discountbyindividualvaluequantity
57	Can add current company charge	15	add_currentcompanycharge
58	Can change current company charge	15	change_currentcompanycharge
59	Can delete current company charge	15	delete_currentcompanycharge
60	Can view current company charge	15	view_currentcompanycharge
61	Can add company invoice mails	16	add_companyinvoicemails
62	Can change company invoice mails	16	change_companyinvoicemails
63	Can delete company invoice mails	16	delete_companyinvoicemails
64	Can view company invoice mails	16	view_companyinvoicemails
65	Can add company coupons	17	add_companycoupons
66	Can change company coupons	17	change_companycoupons
67	Can delete company coupons	17	delete_companycoupons
68	Can view company coupons	17	view_companycoupons
69	Can add company charge	18	add_companycharge
70	Can change company charge	18	change_companycharge
71	Can delete company charge	18	delete_companycharge
72	Can view company charge	18	view_companycharge
73	Can add discount by individual name for company	19	add_discountbyindividualnameforcompany
74	Can change discount by individual name for company	19	change_discountbyindividualnameforcompany
75	Can delete discount by individual name for company	19	delete_discountbyindividualnameforcompany
76	Can view discount by individual name for company	19	view_discountbyindividualnameforcompany
77	Can add company billing	20	add_companybilling
78	Can change company billing	20	change_companybilling
79	Can delete company billing	20	delete_companybilling
80	Can view company billing	20	view_companybilling
81	Can add partner default and discounts	21	add_partnerdefaultanddiscounts
82	Can change partner default and discounts	21	change_partnerdefaultanddiscounts
83	Can delete partner default and discounts	21	delete_partnerdefaultanddiscounts
84	Can view partner default and discounts	21	view_partnerdefaultanddiscounts
85	Can add aggregation type	22	add_aggregationtype
86	Can change aggregation type	22	change_aggregationtype
87	Can delete aggregation type	22	delete_aggregationtype
88	Can view aggregation type	22	view_aggregationtype
89	Can add chart type	23	add_charttype
90	Can change chart type	23	change_charttype
91	Can delete chart type	23	delete_charttype
92	Can view chart type	23	view_charttype
93	Can add dashboard chart configuration	24	add_dashboardchartconfiguration
94	Can change dashboard chart configuration	24	change_dashboardchartconfiguration
95	Can delete dashboard chart configuration	24	delete_dashboardchartconfiguration
96	Can view dashboard chart configuration	24	view_dashboardchartconfiguration
97	Can add formula type	25	add_formulatype
98	Can change formula type	25	change_formulatype
99	Can delete formula type	25	delete_formulatype
100	Can view formula type	25	view_formulatype
101	Can add draft type	26	add_drafttype
102	Can change draft type	26	change_drafttype
103	Can delete draft type	26	delete_drafttype
104	Can view draft type	26	view_drafttype
105	Can add draft	27	add_draft
106	Can change draft	27	change_draft
107	Can delete draft	27	delete_draft
108	Can view draft	27	view_draft
109	Can add dynamic form	28	add_dynamicform
110	Can change dynamic form	28	change_dynamicform
111	Can delete dynamic form	28	delete_dynamicform
112	Can view dynamic form	28	view_dynamicform
113	Can add form value	29	add_formvalue
114	Can change form value	29	change_formvalue
115	Can delete form value	29	delete_formvalue
116	Can view form value	29	view_formvalue
117	Can add attachments	30	add_attachments
118	Can change attachments	30	change_attachments
119	Can delete attachments	30	delete_attachments
120	Can view attachments	30	view_attachments
121	Can add extract file data	31	add_extractfiledata
122	Can change extract file data	31	change_extractfiledata
123	Can delete extract file data	31	delete_extractfiledata
124	Can view extract file data	31	view_extractfiledata
125	Can add conditional type	32	add_conditionaltype
126	Can change conditional type	32	change_conditionaltype
127	Can delete conditional type	32	delete_conditionaltype
128	Can view conditional type	32	view_conditionaltype
129	Can add field	33	add_field
130	Can change field	33	change_field
131	Can delete field	33	delete_field
132	Can view field	33	view_field
133	Can add field date format type	34	add_fielddateformattype
134	Can change field date format type	34	change_fielddateformattype
135	Can delete field date format type	34	delete_fielddateformattype
136	Can view field date format type	34	view_fielddateformattype
137	Can add field number format type	35	add_fieldnumberformattype
138	Can change field number format type	35	change_fieldnumberformattype
139	Can delete field number format type	35	delete_fieldnumberformattype
140	Can view field number format type	35	view_fieldnumberformattype
141	Can add field options	36	add_fieldoptions
142	Can change field options	36	change_fieldoptions
143	Can delete field options	36	delete_fieldoptions
144	Can view field options	36	view_fieldoptions
145	Can add field period interval type	37	add_fieldperiodintervaltype
146	Can change field period interval type	37	change_fieldperiodintervaltype
147	Can delete field period interval type	37	delete_fieldperiodintervaltype
148	Can view field period interval type	37	view_fieldperiodintervaltype
149	Can add field type	38	add_fieldtype
150	Can change field type	38	change_fieldtype
151	Can delete field type	38	delete_fieldtype
152	Can view field type	38	view_fieldtype
153	Can add form	39	add_form
154	Can change form	39	change_form
155	Can delete form	39	delete_form
156	Can view form	39	view_form
157	Can add section type	40	add_sectiontype
158	Can change section type	40	change_sectiontype
159	Can delete section type	40	delete_sectiontype
160	Can view section type	40	view_sectiontype
161	Can add option accessed by	41	add_optionaccessedby
162	Can change option accessed by	41	change_optionaccessedby
163	Can delete option accessed by	41	delete_optionaccessedby
164	Can view option accessed by	41	view_optionaccessedby
165	Can add group	42	add_group
166	Can change group	42	change_group
167	Can delete group	42	delete_group
168	Can view group	42	view_group
169	Can add form accessed by	43	add_formaccessedby
170	Can change form accessed by	43	change_formaccessedby
171	Can delete form accessed by	43	delete_formaccessedby
172	Can view form accessed by	43	view_formaccessedby
173	Can add public access form	44	add_publicaccessform
174	Can change public access form	44	change_publicaccessform
175	Can delete public access form	44	delete_publicaccessform
176	Can view public access form	44	view_publicaccessform
177	Can add public access field	45	add_publicaccessfield
178	Can change public access field	45	change_publicaccessfield
179	Can delete public access field	45	delete_publicaccessfield
180	Can view public access field	45	view_publicaccessfield
181	Can add default field value	46	add_defaultfieldvalue
182	Can change default field value	46	change_defaultfieldvalue
183	Can delete default field value	46	delete_defaultfieldvalue
184	Can view default field value	46	view_defaultfieldvalue
185	Can add default field value attachments	47	add_defaultfieldvalueattachments
186	Can change default field value attachments	47	change_defaultfieldvalueattachments
187	Can delete default field value attachments	47	delete_defaultfieldvalueattachments
188	Can view default field value attachments	47	view_defaultfieldvalueattachments
189	Can add user accessed by	48	add_useraccessedby
190	Can change user accessed by	48	change_useraccessedby
191	Can delete user accessed by	48	delete_useraccessedby
192	Can view user accessed by	48	view_useraccessedby
193	Can add kanban card	49	add_kanbancard
194	Can change kanban card	49	change_kanbancard
195	Can delete kanban card	49	delete_kanbancard
196	Can view kanban card	49	view_kanbancard
197	Can add kanban dimension order	50	add_kanbandimensionorder
198	Can change kanban dimension order	50	change_kanbandimensionorder
199	Can delete kanban dimension order	50	delete_kanbandimensionorder
200	Can view kanban dimension order	50	view_kanbandimensionorder
201	Can add kanban card field	51	add_kanbancardfield
202	Can change kanban card field	51	change_kanbancardfield
203	Can delete kanban card field	51	delete_kanbancardfield
204	Can view kanban card field	51	view_kanbancardfield
205	Can add kanban default	52	add_kanbandefault
206	Can change kanban default	52	change_kanbandefault
207	Can delete kanban default	52	delete_kanbandefault
208	Can view kanban default	52	view_kanbandefault
209	Can add kanban collapsed option	53	add_kanbancollapsedoption
210	Can change kanban collapsed option	53	change_kanbancollapsedoption
211	Can delete kanban collapsed option	53	delete_kanbancollapsedoption
212	Can view kanban collapsed option	53	view_kanbancollapsedoption
213	Can add log entry	54	add_logentry
214	Can change log entry	54	change_logentry
215	Can delete log entry	54	delete_logentry
216	Can view log entry	54	view_logentry
217	Can add permission	55	add_permission
218	Can change permission	55	change_permission
219	Can delete permission	55	delete_permission
220	Can view permission	55	view_permission
221	Can add group	56	add_group
222	Can change group	56	change_group
223	Can delete group	56	delete_group
224	Can view group	56	view_group
225	Can add content type	57	add_contenttype
226	Can change content type	57	change_contenttype
227	Can delete content type	57	delete_contenttype
228	Can view content type	57	view_contenttype
829	Can add formula context attribute type	200	add_formulacontextattributetype
830	Can change formula context attribute type	200	change_formulacontextattributetype
831	Can delete formula context attribute type	200	delete_formulacontextattributetype
832	Can view formula context attribute type	200	view_formulacontextattributetype
833	Can add formula attribute type	201	add_formulaattributetype
834	Can change formula attribute type	201	change_formulaattributetype
835	Can delete formula attribute type	201	delete_formulaattributetype
836	Can view formula attribute type	201	view_formulaattributetype
837	Can add formula context for company	202	add_formulacontextforcompany
838	Can change formula context for company	202	change_formulacontextforcompany
839	Can delete formula context for company	202	delete_formulacontextforcompany
840	Can view formula context for company	202	view_formulacontextforcompany
841	Can add formula context type	203	add_formulacontexttype
842	Can change formula context type	203	change_formulacontexttype
843	Can delete formula context type	203	delete_formulacontexttype
844	Can view formula context type	203	view_formulacontexttype
845	Can add user notification	204	add_usernotification
846	Can change user notification	204	change_usernotification
847	Can delete user notification	204	delete_usernotification
848	Can view user notification	204	view_usernotification
849	Can add notification configuration variable	205	add_notificationconfigurationvariable
850	Can change notification configuration variable	205	change_notificationconfigurationvariable
851	Can delete notification configuration variable	205	delete_notificationconfigurationvariable
852	Can view notification configuration variable	205	view_notificationconfigurationvariable
853	Can add notification configuration	206	add_notificationconfiguration
854	Can change notification configuration	206	change_notificationconfiguration
855	Can delete notification configuration	206	delete_notificationconfiguration
856	Can view notification configuration	206	view_notificationconfiguration
857	Can add pre notification	207	add_prenotification
858	Can change pre notification	207	change_prenotification
859	Can delete pre notification	207	delete_prenotification
860	Can view pre notification	207	view_prenotification
861	Can add notification	208	add_notification
862	Can change notification	208	change_notification
863	Can delete notification	208	delete_notification
864	Can view notification	208	view_notification
865	Can add push notification tag type	209	add_pushnotificationtagtype
866	Can change push notification tag type	209	change_pushnotificationtagtype
867	Can delete push notification tag type	209	delete_pushnotificationtagtype
868	Can view push notification tag type	209	view_pushnotificationtagtype
869	Can add push notification	210	add_pushnotification
870	Can change push notification	210	change_pushnotification
871	Can delete push notification	210	delete_pushnotification
872	Can view push notification	210	view_pushnotification
873	Can add listing selected fields	211	add_listingselectedfields
874	Can change listing selected fields	211	change_listingselectedfields
875	Can delete listing selected fields	211	delete_listingselectedfields
876	Can view listing selected fields	211	view_listingselectedfields
877	Can add theme photos	212	add_themephotos
878	Can change theme photos	212	change_themephotos
879	Can delete theme photos	212	delete_themephotos
880	Can view theme photos	212	view_themephotos
881	Can add theme dashboard chart configuration	213	add_themedashboardchartconfiguration
882	Can change theme dashboard chart configuration	213	change_themedashboardchartconfiguration
883	Can delete theme dashboard chart configuration	213	delete_themedashboardchartconfiguration
884	Can view theme dashboard chart configuration	213	view_themedashboardchartconfiguration
885	Can add theme type	214	add_themetype
886	Can change theme type	214	change_themetype
887	Can delete theme type	214	delete_themetype
888	Can view theme type	214	view_themetype
889	Can add theme kanban card	215	add_themekanbancard
890	Can change theme kanban card	215	change_themekanbancard
891	Can delete theme kanban card	215	delete_themekanbancard
892	Can view theme kanban card	215	view_themekanbancard
893	Can add theme form	216	add_themeform
894	Can change theme form	216	change_themeform
895	Can delete theme form	216	delete_themeform
896	Can view theme form	216	view_themeform
897	Can add theme notification configuration variable	217	add_themenotificationconfigurationvariable
898	Can change theme notification configuration variable	217	change_themenotificationconfigurationvariable
899	Can delete theme notification configuration variable	217	delete_themenotificationconfigurationvariable
900	Can view theme notification configuration variable	217	view_themenotificationconfigurationvariable
901	Can add theme kanban card field	218	add_themekanbancardfield
902	Can change theme kanban card field	218	change_themekanbancardfield
903	Can delete theme kanban card field	218	delete_themekanbancardfield
904	Can view theme kanban card field	218	view_themekanbancardfield
905	Can add theme field	219	add_themefield
906	Can change theme field	219	change_themefield
907	Can delete theme field	219	delete_themefield
908	Can view theme field	219	view_themefield
909	Can add theme	220	add_theme
910	Can change theme	220	change_theme
911	Can delete theme	220	delete_theme
912	Can view theme	220	view_theme
913	Can add theme kanban dimension order	221	add_themekanbandimensionorder
914	Can change theme kanban dimension order	221	change_themekanbandimensionorder
915	Can delete theme kanban dimension order	221	delete_themekanbandimensionorder
916	Can view theme kanban dimension order	221	view_themekanbandimensionorder
917	Can add theme notification configuration	222	add_themenotificationconfiguration
918	Can change theme notification configuration	222	change_themenotificationconfiguration
919	Can delete theme notification configuration	222	delete_themenotificationconfiguration
920	Can view theme notification configuration	222	view_themenotificationconfiguration
921	Can add theme kanban default	223	add_themekanbandefault
922	Can change theme kanban default	223	change_themekanbandefault
923	Can delete theme kanban default	223	delete_themekanbandefault
924	Can view theme kanban default	223	view_themekanbandefault
925	Can add theme field options	224	add_themefieldoptions
926	Can change theme field options	224	change_themefieldoptions
927	Can delete theme field options	224	delete_themefieldoptions
928	Can view theme field options	224	view_themefieldoptions
929	Can add text table option	225	add_texttableoption
930	Can change text table option	225	change_texttableoption
931	Can delete text table option	225	delete_texttableoption
932	Can view text table option	225	view_texttableoption
933	Can add text text option	226	add_texttextoption
934	Can change text text option	226	change_texttextoption
935	Can delete text text option	226	delete_texttextoption
936	Can view text text option	226	view_texttextoption
937	Can add text list type	227	add_textlisttype
938	Can change text list type	227	change_textlisttype
939	Can delete text list type	227	delete_textlisttype
940	Can view text list type	227	view_textlisttype
941	Can add text alignment type	228	add_textalignmenttype
942	Can change text alignment type	228	change_textalignmenttype
943	Can delete text alignment type	228	delete_textalignmenttype
944	Can view text alignment type	228	view_textalignmenttype
945	Can add text table option column dimension	229	add_texttableoptioncolumndimension
946	Can change text table option column dimension	229	change_texttableoptioncolumndimension
947	Can delete text table option column dimension	229	delete_texttableoptioncolumndimension
948	Can view text table option column dimension	229	view_texttableoptioncolumndimension
949	Can add text table option row dimension	230	add_texttableoptionrowdimension
950	Can change text table option row dimension	230	change_texttableoptionrowdimension
951	Can delete text table option row dimension	230	delete_texttableoptionrowdimension
952	Can view text table option row dimension	230	view_texttableoptionrowdimension
953	Can add text block type	231	add_textblocktype
954	Can change text block type	231	change_textblocktype
955	Can delete text block type	231	delete_textblocktype
956	Can view text block type	231	view_textblocktype
957	Can add text page	232	add_textpage
958	Can change text page	232	change_textpage
959	Can delete text page	232	delete_textpage
960	Can view text page	232	view_textpage
961	Can add text content	233	add_textcontent
962	Can change text content	233	change_textcontent
963	Can delete text content	233	delete_textcontent
964	Can view text content	233	view_textcontent
965	Can add text block	234	add_textblock
966	Can change text block	234	change_textblock
967	Can delete text block	234	delete_textblock
968	Can view text block	234	view_textblock
969	Can add text list option	235	add_textlistoption
970	Can change text list option	235	change_textlistoption
971	Can delete text list option	235	delete_textlistoption
972	Can view text list option	235	view_textlistoption
973	Can add text block type can contain type	236	add_textblocktypecancontaintype
974	Can change text block type can contain type	236	change_textblocktypecancontaintype
975	Can delete text block type can contain type	236	delete_textblocktypecancontaintype
976	Can view text block type can contain type	236	view_textblocktypecancontaintype
977	Can add text image option	237	add_textimageoption
978	Can change text image option	237	change_textimageoption
979	Can delete text image option	237	delete_textimageoption
980	Can view text image option	237	view_textimageoption
981	Can add pdf template configuration	238	add_pdftemplateconfiguration
982	Can change pdf template configuration	238	change_pdftemplateconfiguration
983	Can delete pdf template configuration	238	delete_pdftemplateconfiguration
984	Can view pdf template configuration	238	view_pdftemplateconfiguration
985	Can add pdf generated	239	add_pdfgenerated
986	Can change pdf generated	239	change_pdfgenerated
987	Can delete pdf generated	239	delete_pdfgenerated
988	Can view pdf generated	239	view_pdfgenerated
989	Can add pdf template allowed text block	240	add_pdftemplateallowedtextblock
990	Can change pdf template allowed text block	240	change_pdftemplateallowedtextblock
991	Can delete pdf template allowed text block	240	delete_pdftemplateallowedtextblock
992	Can view pdf template allowed text block	240	view_pdftemplateallowedtextblock
993	Can add pdf template configuration variables	241	add_pdftemplateconfigurationvariables
994	Can change pdf template configuration variables	241	change_pdftemplateconfigurationvariables
995	Can delete pdf template configuration variables	241	delete_pdftemplateconfigurationvariables
996	Can view pdf template configuration variables	241	view_pdftemplateconfigurationvariables
997	Can add session	242	add_session
998	Can change session	242	change_session
999	Can delete session	242	delete_session
1000	Can view session	242	view_session
1001	Can add formula variable	243	add_formulavariable
1002	Can change formula variable	243	change_formulavariable
1003	Can delete formula variable	243	delete_formulavariable
1004	Can view formula variable	243	view_formulavariable
1005	Can add theme formula variable	244	add_themeformulavariable
1006	Can change theme formula variable	244	change_themeformulavariable
1007	Can delete theme formula variable	244	delete_themeformulavariable
1008	Can view theme formula variable	244	view_themeformulavariable
\.


--
-- Data for Name: charge_frequency_type; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.charge_frequency_type (id, name, "order") FROM stdin;
1	monthly	1
\.


--
-- Data for Name: charge_type; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.charge_type (id, name, "order") FROM stdin;
1	user	1
2	company	1
\.


--
-- Data for Name: chart_type; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.chart_type (id, name, "order") FROM stdin;
1	pie	1
2	line	1
3	bar	1
4	card	1
\.


--
-- Data for Name: company; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.company (id, name, endpoint, updated_at, created_at, is_active, partner, company_type_id, shared_by_id, logo_image_bucket, logo_image_path, logo_image_url) FROM stdin;
6	teste	teste	2019-07-28 14:25:22.131892+00	2019-07-28 14:25:22.132173+00	t	\N	\N	\N	reflow-crm	company-logo	\N
7	asdasdasd	asdasdasd	2019-07-29 19:00:39.574115+00	2019-07-29 19:00:39.574387+00	t	\N	\N	\N	reflow-crm	company-logo	\N
8	Teste	testeteste1	2019-11-05 16:48:17.059542+00	2019-11-05 16:48:17.059891+00	t	\N	1	\N	reflow-crm	company-logo	\N
3	reflow	reflow	2019-03-01 02:00:49.548484+00	2018-07-18 02:39:10.828+00	t	\N	\N	\N	reflow-crm	company-logo	\N
1	reflow	reflow	2020-09-09 01:07:00.769551+00	2019-03-20 21:18:13.761+00	t	\N	3	\N	reflow-crm	company-logo	https://reflow-crm.s3.amazonaws.com/company-logo/1/complete_logo.png
9	Rapid Rhino	rapidrhino	2020-09-29 23:01:05.291124+00	2020-09-29 23:01:05.291151+00	t	\N	\N	\N	reflow-crm	company-logo	\N
\.


--
-- Data for Name: company_billing; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.company_billing (id, address, zip_code, street, number, neighborhood, country, state, city, cnpj, additional_details, is_supercompany, is_paying_company, vindi_plan_id, vindi_client_id, vindi_product_id, vindi_payment_profile_id, vindi_signature_id, charge_frequency_type_id, company_id, invoice_date_type_id, payment_method_type_id) FROM stdin;
1	teste	\N	\N	\N	\N	\N	\N	\N	\N	\N	f	f	\N	\N	\N	\N	\N	\N	6	\N	\N
2	asdasd	\N	\N	\N	\N	\N	\N	\N	\N	\N	f	f	\N	\N	\N	\N	\N	\N	7	\N	\N
3	R. Frei Caneca, 485 - Consolação, São Paulo - SP, 01307-001, Brasil	01307-001	R. Frei Caneca	485	Consolação	BR	SP	São Paulo	\N	\N	f	f	\N	\N	\N	\N	\N	\N	8	\N	\N
4	Ap 96B	\N	\N	\N	\N	\N	\N	\N	\N	\N	t	t	\N	\N	\N	\N	\N	\N	3	\N	\N
5	Rua Frei Caneca	01307001	Rua Frei Caneca	485	Consolação	BR	SP	São Paulo	49469428000177	95B	t	t	18085	744875	78831	492579	\N	1	1	2	1
6	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	f	f	\N	\N	\N	\N	\N	\N	9	\N	\N
\.


--
-- Data for Name: company_charge; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.company_charge (id, updated_at, created_at, total_value, attempt_count, company_id) FROM stdin;
1	2020-10-02 20:22:24.964586+00	2020-10-02 20:22:24.96461+00	168.00	1	1
2	2020-11-01 12:35:12.163381+00	2020-11-01 12:35:12.163411+00	168.00	1	1
3	2020-12-01 11:31:10.901704+00	2020-12-01 11:31:10.90173+00	168.00	1	1
4	2020-12-31 14:59:42.148266+00	2020-12-31 14:59:42.148288+00	168.00	1	1
5	2021-02-01 12:49:51.442405+00	2021-02-01 12:49:51.442432+00	168.00	1	1
6	2021-03-01 14:11:09.328447+00	2021-03-01 14:11:09.32847+00	168.00	1	1
7	2021-04-01 13:20:11.495872+00	2021-04-01 13:20:11.495895+00	168.00	1	1
8	2021-05-01 14:40:16.815321+00	2021-05-01 14:40:16.815344+00	168.00	1	1
\.


--
-- Data for Name: company_coupon; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.company_coupon (id, company_id, discount_coupon_id) FROM stdin;
\.


--
-- Data for Name: company_invoice_mails; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.company_invoice_mails (id, email, company_id) FROM stdin;
23	nicolasmelo12@gmail.com	1
24	lleal_melo@hotmail.com	1
25	reflow@reflow.com.br	1
\.


--
-- Data for Name: company_type; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.company_type (id, name, label_name, "order") FROM stdin;
1	software	Software, Desenvolvimento de Aplicativos	1
2	insurance	Seguros	1
3	health	Saúde	1
4	startup	Start-up	1
5	education	Educação	1
6	realestate	Imobiliário	1
7	agency	Agência Criativa	1
8	financial	Serviços Financeiros	1
9	news	Imprensa	1
10	industry	Indústria	1
11	consulting	Consultoria	1
12	smallbusiness	Atacado, Varejo	1
13	building	Construção	1
14	others	Outros	1
\.


--
-- Data for Name: conditional_type; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.conditional_type (id, type, label_name, "order") FROM stdin;
1	equal	Igual	1
\.


--
-- Data for Name: current_company_charge; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.current_company_charge (id, updated_at, created_at, quantity, company_id, discount_by_individual_value_id, individual_charge_value_type_id) FROM stdin;
\.


--
-- Data for Name: dashboard_chart_configuration; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.dashboard_chart_configuration (id, name, for_company, aggregation_type_id, chart_type_id, company_id, form_id, label_field_id, number_format_type_id, user_id, value_field_id) FROM stdin;
\.


--
-- Data for Name: data_type; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.data_type (id, name, label_name, "order") FROM stdin;
1	kanban	Kanban	1
2	listing	Listagem	1
3	dashboard	Dashboard	1
\.


--
-- Data for Name: default_attachments; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.default_attachments (id, created_at, updated_at, file, bucket, file_default_attachments_path, file_url, file_size) FROM stdin;
\.


--
-- Data for Name: default_field_value; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.default_field_value (id, created_at, updated_at, value, field_id, default_attachment_id) FROM stdin;
\.


--
-- Data for Name: discount_by_individual_name_for_company; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.discount_by_individual_name_for_company (id, value, name, company_id, individual_charge_value_type_id) FROM stdin;
\.


--
-- Data for Name: discount_by_individual_value_quantity; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.discount_by_individual_value_quantity (id, quantity, value, name, individual_charge_value_type_id) FROM stdin;
1	10	0.90	per_10gb	1
2	20	0.75	per_25gb	1
3	0	0.00	per_5gb	1
6	10	0.75	per_10charts_for_company	4
5	5	0.90	per_5charts_for_company	4
4	0	0.00	per_2charts_for_company	4
7	0	0.00	per_2chart_for_user	3
9	10	0.75	per_10chart_for_user	3
8	5	0.90	per_5chart_for_user	3
10	30	0.00	per_30pdf_download_for_company	5
11	60	0.90	per_60pdf_download_for_company	5
12	200	0.75	per_200pdf_download_for_company	5
\.


--
-- Data for Name: discount_coupon; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.discount_coupon (id, name, value, permanent, start_at, end_at) FROM stdin;
\.


--
-- Data for Name: django_admin_log; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.django_admin_log (id, action_time, object_id, object_repr, action_flag, change_message, content_type_id, user_id) FROM stdin;
\.


--
-- Data for Name: django_celery_results_taskresult; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.django_celery_results_taskresult (id, task_id, status, content_type, content_encoding, result, date_done, traceback, hidden, meta, task_args, task_kwargs, task_name) FROM stdin;
\.


--
-- Data for Name: django_content_type; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.django_content_type (id, app_label, model) FROM stdin;
1	authentication	userextended
2	authentication	company
3	authentication	companytype
4	authentication	profiletype
5	authentication	visualizationtype
6	authentication	addresshelper
7	authentication	publicaccess
8	billing	chargefrequencytype
9	billing	chargetype
10	billing	discountcoupon
11	billing	invoicedatetype
12	billing	paymentmethodtype
13	billing	individualchargevaluetype
14	billing	discountbyindividualvaluequantity
15	billing	currentcompanycharge
16	billing	companyinvoicemails
17	billing	companycoupons
18	billing	companycharge
19	billing	discountbyindividualnameforcompany
20	billing	companybilling
21	billing	partnerdefaultanddiscounts
22	dashboard	aggregationtype
23	dashboard	charttype
24	dashboard	dashboardchartconfiguration
25	formula	formulatype
26	draft	drafttype
27	draft	draft
28	data	dynamicform
29	data	formvalue
30	data	attachments
31	data	extractfiledata
32	formulary	conditionaltype
33	formulary	field
34	formulary	fielddateformattype
35	formulary	fieldnumberformattype
36	formulary	fieldoptions
37	formulary	fieldperiodintervaltype
38	formulary	fieldtype
39	formulary	form
40	formulary	sectiontype
41	formulary	optionaccessedby
42	formulary	group
43	formulary	formaccessedby
44	formulary	publicaccessform
45	formulary	publicaccessfield
46	formulary	defaultfieldvalue
47	formulary	defaultfieldvalueattachments
48	formulary	useraccessedby
49	kanban	kanbancard
50	kanban	kanbandimensionorder
51	kanban	kanbancardfield
52	kanban	kanbandefault
53	kanban	kanbancollapsedoption
54	admin	logentry
55	auth	permission
56	auth	group
57	contenttypes	contenttype
200	formula	formulacontextattributetype
201	formula	formulaattributetype
202	formula	formulacontextforcompany
203	formula	formulacontexttype
204	notification	usernotification
205	notification	notificationconfigurationvariable
206	notification	notificationconfiguration
207	notification	prenotification
208	notification	notification
209	notify	pushnotificationtagtype
210	notify	pushnotification
211	listing	listingselectedfields
212	theme	themephotos
213	theme	themedashboardchartconfiguration
214	theme	themetype
215	theme	themekanbancard
216	theme	themeform
217	theme	themenotificationconfigurationvariable
218	theme	themekanbancardfield
219	theme	themefield
220	theme	theme
221	theme	themekanbandimensionorder
222	theme	themenotificationconfiguration
223	theme	themekanbandefault
224	theme	themefieldoptions
225	rich_text	texttableoption
226	rich_text	texttextoption
227	rich_text	textlisttype
228	rich_text	textalignmenttype
229	rich_text	texttableoptioncolumndimension
230	rich_text	texttableoptionrowdimension
231	rich_text	textblocktype
232	rich_text	textpage
233	rich_text	textcontent
234	rich_text	textblock
235	rich_text	textlistoption
236	rich_text	textblocktypecancontaintype
237	rich_text	textimageoption
238	pdf_generator	pdftemplateconfiguration
239	pdf_generator	pdfgenerated
240	pdf_generator	pdftemplateallowedtextblock
241	pdf_generator	pdftemplateconfigurationvariables
242	sessions	session
243	formulary	formulavariable
244	theme	themeformulavariable
\.


--
-- Data for Name: django_migrations; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.django_migrations (id, app, name, applied) FROM stdin;
1	contenttypes	0001_initial	2021-05-22 06:04:31.490027+00
2	authentication	0001_initial	2021-05-22 06:04:31.546305+00
3	admin	0001_initial	2021-05-22 06:04:31.599021+00
4	admin	0002_logentry_remove_auto_add	2021-05-22 06:04:31.619299+00
5	admin	0003_logentry_add_action_flag_choices	2021-05-22 06:04:31.629304+00
6	contenttypes	0002_remove_content_type_name	2021-05-22 06:04:31.652966+00
7	auth	0001_initial	2021-05-22 06:04:31.695597+00
8	auth	0002_alter_permission_name_max_length	2021-05-22 06:04:31.733577+00
9	auth	0003_alter_user_email_max_length	2021-05-22 06:04:31.74411+00
10	auth	0004_alter_user_username_opts	2021-05-22 06:04:31.760306+00
11	auth	0005_alter_user_last_login_null	2021-05-22 06:04:31.773918+00
12	auth	0006_require_contenttypes_0002	2021-05-22 06:04:31.778125+00
13	auth	0007_alter_validators_add_error_messages	2021-05-22 06:04:31.815308+00
14	auth	0008_alter_user_username_max_length	2021-05-22 06:04:31.832689+00
15	auth	0009_alter_user_last_name_max_length	2021-05-22 06:04:31.845938+00
16	auth	0010_alter_group_name_max_length	2021-05-22 06:04:31.863525+00
17	auth	0011_update_proxy_permissions	2021-05-22 06:04:31.883882+00
18	auth	0012_alter_user_first_name_max_length	2021-05-22 06:04:31.898724+00
19	billing	0001_initial	2021-05-22 06:04:32.037168+00
20	billing	0002_auto_20200719_1720	2021-05-22 06:04:32.175296+00
21	billing	0003_individualchargevaluetype_charge_group_name	2021-05-22 06:04:32.191682+00
22	billing	0004_discountbyindividualvalue_static	2021-05-22 06:04:32.204324+00
23	authentication	0002_auto_20200608_1957	2021-05-22 06:04:32.428505+00
24	authentication	0003_auto_20200719_1720	2021-05-22 06:04:32.519835+00
25	authentication	0004_addresstype	2021-05-22 06:04:32.538096+00
26	authentication	0005_auto_20200722_1450	2021-05-22 06:04:32.582023+00
27	authentication	0006_company_additional_details	2021-05-22 06:04:32.604098+00
28	billing	0005_auto_20200804_0005	2021-05-22 06:04:32.668702+00
29	billing	0006_auto_20200804_0557	2021-05-22 06:04:32.715479+00
30	authentication	0007_auto_20200818_0005	2021-05-22 06:04:32.74578+00
31	authentication	0008_auto_20200828_1928	2021-05-22 06:04:32.775399+00
32	billing	0007_companybilling	2021-05-22 06:04:32.824013+00
33	billing	0008_migrate_company_to_company_billing	2021-05-22 06:04:32.907271+00
34	authentication	0009_auto_20200828_2011	2021-05-22 06:04:33.363171+00
35	authentication	0010_auto_20200902_1555	2021-05-22 06:04:33.415091+00
36	authentication	0011_publicaccess	2021-05-22 06:04:33.450842+00
37	billing	0009_auto_20200828_2045	2021-05-22 06:04:33.497526+00
38	billing	0010_auto_20200828_2112	2021-05-22 06:04:33.540823+00
39	billing	0011_partnerdefaultanddiscounts	2021-05-22 06:04:33.574759+00
40	billing	0012_auto_20210126_2029	2021-05-22 06:04:33.613609+00
41	billing	0013_auto_20210213_2138	2021-05-22 06:04:33.650565+00
42	billing	0014_remove_currentcompanycharge_user	2021-05-22 06:04:33.688488+00
43	formulary	0001_initial	2021-05-22 06:04:34.284083+00
44	formulary	0002_auto_20200719_1720	2021-05-22 06:04:34.437694+00
45	dashboard	0001_initial	2021-05-22 06:04:34.505255+00
46	dashboard	0002_auto_20200719_1720	2021-05-22 06:04:34.561613+00
47	dashboard	0003_auto_20200917_2102	2021-05-22 06:04:34.712165+00
48	formulary	0003_fieldoptions_uuid	2021-05-22 06:04:34.73348+00
49	formulary	0004_auto_20210225_2352	2021-05-22 06:04:34.780709+00
50	formulary	0005_publicaccessfield_publicaccessform	2021-05-22 06:04:34.981033+00
51	formulary	0006_auto_20210302_1652	2021-05-22 06:04:35.065492+00
52	formulary	0007_auto_20210307_2157	2021-05-22 06:04:35.133353+00
53	formulary	0008_auto_20210317_1341	2021-05-22 06:04:35.212428+00
54	formulary	0009_defaultfieldvalue	2021-05-22 06:04:35.266002+00
55	formulary	0010_auto_20210325_0155	2021-05-22 06:04:35.326066+00
56	formulary	0011_auto_20210325_1716	2021-05-22 06:04:35.343487+00
57	formulary	0012_auto_20210326_0112	2021-05-22 06:04:35.36925+00
58	formulary	0013_auto_20210413_0050	2021-05-22 06:04:35.422919+00
59	formulary	0014_auto_20210413_0330	2021-05-22 06:04:35.472204+00
60	formulary	0015_auto_20210417_0106	2021-05-22 06:04:35.538175+00
61	formulary	0016_field_is_long_text_rich_text	2021-05-22 06:04:35.563587+00
62	formulary	0017_useraccessedby	2021-05-22 06:04:35.6146+00
63	formulary	0018_auto_20210507_1829	2021-05-22 06:04:35.675036+00
64	data	0001_initial	2021-05-22 06:04:35.94386+00
65	data	0002_auto_20200614_0232	2021-05-22 06:04:36.057143+00
66	data	0003_auto_20200624_1506	2021-05-22 06:04:36.106707+00
67	data	0004_dynamicform_user	2021-05-22 06:04:36.174612+00
68	data	0005_formvalue_is_long_text_rich_text	2021-05-22 06:04:36.216255+00
69	data	0006_dynamicform_uuid	2021-05-22 06:04:36.255992+00
70	data	0007_auto_20210514_1559	2021-05-22 06:04:36.311427+00
71	data	0008_extractfiledata	2021-05-22 06:04:36.372158+00
72	draft	0001_initial	2021-05-22 06:04:36.460309+00
73	draft	0002_auto_20210105_0535	2021-05-22 06:04:36.570293+00
74	draft	0003_draft_is_public	2021-05-22 06:04:36.608475+00
75	formula	0001_initial	2021-05-22 06:04:36.61977+00
76	formula	0002_auto_20200719_1720	2021-05-22 06:04:36.634466+00
77	kanban	0001_initial	2021-05-22 06:04:36.916425+00
78	kanban	0002_auto_20210220_0556	2021-05-22 06:04:37.167679+00
79	kanban	0003_auto_20210220_0556	2021-05-22 06:04:37.263395+00
80	kanban	0004_kanbancardfield_order	2021-05-22 06:04:37.297413+00
81	kanban	0005_auto_20210224_0438	2021-05-22 06:04:37.357309+00
82	kanban	0006_auto_20210225_1717	2021-05-22 06:04:37.407193+00
83	kanban	0007_auto_20210227_1913	2021-05-22 06:04:37.437906+00
84	listing	0001_initial	2021-05-22 06:04:54.359948+00
85	listing	0002_extractfiledata_file_id	2021-05-22 06:04:54.380569+00
86	listing	0003_delete_listingtotalforfield	2021-05-22 06:04:54.384735+00
87	listing	0004_delete_extractfiledata	2021-05-22 06:04:54.389225+00
88	notification	0001_initial	2021-05-22 06:04:54.392841+00
89	notification	0002_auto_20200719_1720	2021-05-22 06:04:54.396102+00
90	notify	0001_initial	2021-05-22 06:04:54.400602+00
91	notify	0002_auto_20200719_1720	2021-05-22 06:04:54.404994+00
92	rich_text	0001_initial	2021-05-22 06:04:54.410607+00
93	rich_text	0002_auto_20201016_2146	2021-05-22 06:04:54.414156+00
94	rich_text	0003_textcontent_link	2021-05-22 06:04:54.418432+00
95	rich_text	0004_auto_20201019_1430	2021-05-22 06:04:54.422588+00
96	rich_text	0005_auto_20201027_0030	2021-05-22 06:04:54.427071+00
97	rich_text	0006_auto_20201126_1627	2021-05-22 06:04:54.430541+00
98	rich_text	0007_auto_20201201_0108	2021-05-22 06:04:54.433818+00
99	rich_text	0008_auto_20201202_1739	2021-05-22 06:04:54.437214+00
100	rich_text	0009_textcontent_text_size	2021-05-22 06:04:54.441813+00
101	rich_text	0010_auto_20210106_0031	2021-05-22 06:04:54.445623+00
102	rich_text	0011_auto_20210106_1651	2021-05-22 06:04:54.449205+00
103	rich_text	0012_auto_20210107_1457	2021-05-22 06:04:54.452641+00
104	rich_text	0013_auto_20210113_2322	2021-05-22 06:04:54.456073+00
105	rich_text	0014_auto_20210113_2348	2021-05-22 06:04:54.460068+00
106	rich_text	0015_auto_20210113_2352	2021-05-22 06:04:54.46443+00
107	rich_text	0016_textimageoption_file_image_uuid	2021-05-22 06:04:54.467943+00
108	rich_text	0017_auto_20210126_2029	2021-05-22 06:04:54.471484+00
109	rich_text	0018_auto_20210126_2126	2021-05-22 06:04:54.474805+00
110	rich_text	0019_auto_20210127_1315	2021-05-22 06:04:54.478548+00
111	pdf_generator	0001_initial	2021-05-22 06:04:54.483007+00
112	pdf_generator	0002_auto_20201201_0108	2021-05-22 06:04:54.486531+00
113	pdf_generator	0003_auto_20201203_2308	2021-05-22 06:04:54.489941+00
114	pdf_generator	0004_pdftemplateconfiguration_rich_text	2021-05-22 06:04:54.493353+00
115	pdf_generator	0005_auto_20201211_1634	2021-05-22 06:04:54.496884+00
116	pdf_generator	0006_pdfgenerated	2021-05-22 06:04:54.500797+00
117	pdf_generator	0007_pdftemplateallowedtextblock	2021-05-22 06:04:54.504569+00
118	pdf_generator	0008_auto_20210210_2309	2021-05-22 06:04:54.508904+00
119	rich_text	0020_auto_20210210_2309	2021-05-22 06:04:54.512289+00
120	sessions	0001_initial	2021-05-22 06:04:54.515677+00
121	theme	0001_initial	2021-05-22 06:04:54.519919+00
122	theme	0002_auto_20200719_1720	2021-05-22 06:04:54.523967+00
123	theme	0003_auto_20200917_2102	2021-05-22 06:04:54.528929+00
124	theme	0004_auto_20200917_2105	2021-05-22 06:04:54.533244+00
125	theme	0005_auto_20200929_1701	2021-05-22 06:04:54.536586+00
126	theme	0006_migrate_company_to_theme	2021-05-22 06:04:54.540498+00
127	theme	0007_auto_20201016_1942	2021-05-22 06:04:54.54467+00
128	theme	0008_auto_20210222_1540	2021-05-22 06:04:54.548145+00
129	theme	0009_auto_20210222_1639	2021-05-22 06:04:54.551616+00
130	theme	0010_auto_20210222_1639	2021-05-22 06:04:54.555011+00
131	theme	0011_themekanbancardfield_order	2021-05-22 06:04:54.558776+00
132	theme	0012_auto_20210224_0438	2021-05-22 06:04:54.563114+00
133	theme	0013_themefieldoptions_uuid	2021-05-22 06:04:54.566873+00
134	theme	0014_auto_20210225_2352	2021-05-22 06:04:54.570403+00
135	theme	0015_auto_20210227_1913	2021-05-22 06:04:54.574168+00
136	theme	0016_auto_20210413_0050	2021-05-22 06:04:54.57759+00
137	theme	0017_auto_20210413_0329	2021-05-22 06:04:54.582387+00
138	theme	0018_auto_20210417_0106	2021-05-22 06:04:54.587008+00
139	theme	0019_themefield_is_long_text_rich_text	2021-05-22 06:04:54.590315+00
519	contenttypes	0001_initial	2020-06-19 07:39:51.379778+00
520	authentication	0001_initial	2020-06-19 07:39:51.385314+00
521	admin	0001_initial	2020-06-19 07:39:51.389492+00
522	admin	0002_logentry_remove_auto_add	2020-06-19 07:39:51.3937+00
523	admin	0003_logentry_add_action_flag_choices	2020-06-19 07:39:51.397804+00
524	contenttypes	0002_remove_content_type_name	2020-06-19 07:39:51.40177+00
525	auth	0001_initial	2020-06-19 07:39:51.405629+00
526	auth	0002_alter_permission_name_max_length	2020-06-19 07:39:51.409879+00
527	auth	0003_alter_user_email_max_length	2020-06-19 07:39:51.41396+00
528	auth	0004_alter_user_username_opts	2020-06-19 07:39:51.41792+00
529	auth	0005_alter_user_last_login_null	2020-06-19 07:39:51.422063+00
530	auth	0006_require_contenttypes_0002	2020-06-19 07:39:51.425866+00
531	auth	0007_alter_validators_add_error_messages	2020-06-19 07:39:51.429897+00
532	auth	0008_alter_user_username_max_length	2020-06-19 07:39:51.434211+00
533	auth	0009_alter_user_last_name_max_length	2020-06-19 07:39:51.438631+00
534	auth	0010_alter_group_name_max_length	2020-06-19 07:39:51.442623+00
535	auth	0011_update_proxy_permissions	2020-06-19 07:39:51.446692+00
536	billing	0001_initial	2020-06-19 07:39:51.450564+00
537	authentication	0002_auto_20200608_1957	2020-06-19 07:39:51.454608+00
538	formulary	0001_initial	2020-06-19 07:39:51.458649+00
539	data	0001_initial	2020-06-19 07:39:51.462769+00
540	data	0002_auto_20200614_0232	2020-06-19 07:39:51.466723+00
541	formula	0001_initial	2020-06-19 07:39:51.470911+00
542	kanban	0001_initial	2020-06-19 07:39:51.474923+00
543	listing	0001_initial	2020-06-19 07:39:51.479109+00
544	notification	0001_initial	2020-06-19 07:39:51.483502+00
545	notify	0001_initial	2020-06-19 07:39:51.487922+00
546	sessions	0001_initial	2020-06-19 07:39:51.492087+00
547	theme	0001_initial	2020-06-19 07:39:51.496114+00
548	data	0003_auto_20200624_1506	2020-06-24 15:22:44.926164+00
549	listing	0002_extractfiledata_file_id	2020-06-29 17:09:35.701678+00
550	dashboard	0001_initial	2020-07-03 23:25:40.846899+00
551	authentication	0003_auto_20200719_1720	2020-07-30 02:20:52.524046+00
552	authentication	0004_addresstype	2020-07-30 02:20:52.550323+00
553	authentication	0005_auto_20200722_1450	2020-07-30 02:20:52.618322+00
554	authentication	0006_company_additional_details	2020-07-30 02:20:52.638834+00
555	billing	0002_auto_20200719_1720	2020-07-30 02:20:52.784435+00
556	dashboard	0002_auto_20200719_1720	2020-07-30 02:20:52.821861+00
557	formula	0002_auto_20200719_1720	2020-07-30 02:20:52.851465+00
558	formulary	0002_auto_20200719_1720	2020-07-30 02:20:52.955976+00
559	notification	0002_auto_20200719_1720	2020-07-30 02:20:52.990457+00
560	notify	0002_auto_20200719_1720	2020-07-30 02:20:53.010504+00
561	theme	0002_auto_20200719_1720	2020-07-30 02:20:53.056164+00
562	billing	0003_individualchargevaluetype_charge_group_name	2020-08-02 05:35:37.263197+00
563	billing	0004_discountbyindividualvalue_static	2020-08-03 05:41:55.085464+00
564	billing	0005_auto_20200804_0005	2020-08-04 04:48:30.368767+00
565	billing	0006_auto_20200804_0557	2020-08-04 06:27:06.836012+00
566	auth	0012_alter_user_first_name_max_length	2020-08-10 06:22:45.478971+00
567	authentication	0007_auto_20200818_0005	2020-08-19 15:22:32.225133+00
568	data	0004_dynamicform_user	2020-08-19 15:22:32.44257+00
569	authentication	0008_auto_20200828_1928	2020-08-30 22:05:54.862131+00
570	billing	0007_companybilling	2020-08-30 22:05:55.337045+00
571	billing	0008_migrate_company_to_company_billing	2020-08-30 22:05:55.733856+00
572	authentication	0009_auto_20200828_2011	2020-08-30 22:05:56.416923+00
573	billing	0009_auto_20200828_2045	2020-08-30 22:05:56.485716+00
574	billing	0010_auto_20200828_2112	2020-08-30 22:05:56.565713+00
575	authentication	0010_auto_20200902_1555	2020-09-05 04:00:17.141193+00
576	dashboard	0003_auto_20200917_2102	2020-09-18 01:01:27.388655+00
577	listing	0003_delete_listingtotalforfield	2020-09-18 01:01:27.425412+00
578	theme	0003_auto_20200917_2102	2020-09-18 01:01:28.507024+00
579	theme	0004_auto_20200917_2105	2020-09-18 01:01:28.608748+00
580	theme	0005_auto_20200929_1701	2020-09-29 23:20:50.248041+00
581	rich_text	0001_initial	2020-12-03 06:48:30.533272+00
582	rich_text	0002_auto_20201016_2146	2020-12-03 06:48:30.650531+00
583	rich_text	0003_textcontent_link	2020-12-03 06:48:30.665841+00
584	rich_text	0004_auto_20201019_1430	2020-12-03 06:48:30.699172+00
585	rich_text	0005_auto_20201027_0030	2020-12-03 06:48:30.758028+00
586	rich_text	0006_auto_20201126_1627	2020-12-03 06:48:30.837598+00
587	pdf_generator	0001_initial	2020-12-03 06:48:31.054764+00
588	pdf_generator	0002_auto_20201201_0108	2020-12-03 06:48:31.196169+00
589	rich_text	0007_auto_20201201_0108	2020-12-03 06:48:31.22438+00
590	rich_text	0008_auto_20201202_1739	2020-12-03 06:48:31.516445+00
591	pdf_generator	0003_auto_20201203_2308	2020-12-11 03:11:43.734265+00
592	rich_text	0009_textcontent_text_size	2020-12-11 03:11:43.869458+00
593	pdf_generator	0004_pdftemplateconfiguration_rich_text	2020-12-12 16:31:40.291884+00
594	pdf_generator	0005_auto_20201211_1634	2020-12-12 16:31:40.355707+00
595	pdf_generator	0006_pdfgenerated	2020-12-12 16:31:40.431264+00
596	theme	0006_migrate_company_to_theme	2020-12-12 16:41:25.590843+00
597	theme	0007_auto_20201016_1942	2020-12-12 16:41:26.017696+00
598	draft	0001_initial	2021-01-10 03:46:58.91209+00
599	draft	0002_auto_20210105_0535	2021-01-10 03:46:59.197051+00
600	rich_text	0010_auto_20210106_0031	2021-01-10 03:46:59.2344+00
601	rich_text	0011_auto_20210106_1651	2021-01-10 03:46:59.324777+00
602	rich_text	0012_auto_20210107_1457	2021-01-10 03:46:59.358456+00
603	rich_text	0013_auto_20210113_2322	2021-01-14 01:31:21.215876+00
604	rich_text	0014_auto_20210113_2348	2021-01-14 01:31:21.246812+00
605	rich_text	0015_auto_20210113_2352	2021-01-14 01:31:21.276307+00
606	rich_text	0016_textimageoption_file_image_uuid	2021-01-15 06:46:12.381382+00
607	billing	0011_partnerdefaultanddiscounts	2021-01-21 03:19:29.732354+00
608	billing	0012_auto_20210126_2029	2021-01-27 23:53:18.143297+00
609	rich_text	0017_auto_20210126_2029	2021-01-27 23:53:18.368076+00
610	rich_text	0018_auto_20210126_2126	2021-01-27 23:53:18.478061+00
611	rich_text	0019_auto_20210127_1315	2021-01-27 23:53:18.513128+00
612	pdf_generator	0007_pdftemplateallowedtextblock	2021-01-27 23:53:18.673048+00
613	pdf_generator	0008_auto_20210210_2309	2021-02-10 23:19:34.049457+00
614	rich_text	0020_auto_20210210_2309	2021-02-10 23:19:34.155605+00
615	billing	0013_auto_20210213_2138	2021-02-16 01:48:17.59503+00
616	billing	0014_remove_currentcompanycharge_user	2021-02-16 01:48:17.872488+00
617	kanban	0002_auto_20210220_0556	2021-02-24 07:42:33.59857+00
618	kanban	0003_auto_20210220_0556	2021-02-24 07:42:34.022418+00
619	kanban	0004_kanbancardfield_order	2021-02-24 07:42:34.088186+00
620	kanban	0005_auto_20210224_0438	2021-02-24 07:42:34.388699+00
621	theme	0008_auto_20210222_1540	2021-02-24 07:42:34.973513+00
622	theme	0009_auto_20210222_1639	2021-02-24 07:42:35.240907+00
623	theme	0010_auto_20210222_1639	2021-02-24 07:42:37.404964+00
624	theme	0011_themekanbancardfield_order	2021-02-24 07:42:37.44352+00
625	theme	0012_auto_20210224_0438	2021-02-24 07:42:37.450121+00
626	kanban	0006_auto_20210225_1717	2021-02-25 21:58:15.438124+00
627	formulary	0003_fieldoptions_uuid	2021-02-26 04:43:31.980569+00
628	formulary	0004_auto_20210225_2352	2021-02-26 04:43:32.24145+00
629	theme	0013_themefieldoptions_uuid	2021-02-26 04:43:32.29883+00
630	theme	0014_auto_20210225_2352	2021-02-26 04:43:32.819892+00
631	kanban	0007_auto_20210227_1913	2021-02-27 19:23:10.231413+00
632	theme	0015_auto_20210227_1913	2021-02-27 19:23:10.276138+00
633	authentication	0011_publicaccess	2021-03-19 01:43:15.738279+00
634	draft	0003_draft_is_public	2021-03-19 01:43:15.876699+00
635	formulary	0005_publicaccessfield_publicaccessform	2021-03-19 01:43:16.05119+00
636	formulary	0006_auto_20210302_1652	2021-03-19 01:43:16.305862+00
637	formulary	0007_auto_20210307_2157	2021-03-19 01:43:16.522867+00
638	formulary	0008_auto_20210317_1341	2021-03-19 01:43:16.922059+00
639	formulary	0009_defaultfieldvalue	2021-04-01 04:07:31.248615+00
640	formulary	0010_auto_20210325_0155	2021-04-01 04:07:31.67468+00
641	formulary	0011_auto_20210325_1716	2021-04-01 04:07:31.705934+00
642	formulary	0012_auto_20210326_0112	2021-04-01 04:07:31.782763+00
643	formulary	0013_auto_20210413_0050	2021-04-18 04:12:43.883895+00
644	formulary	0014_auto_20210413_0330	2021-04-18 04:12:44.296716+00
645	formulary	0015_auto_20210417_0106	2021-04-18 04:12:44.573133+00
646	theme	0016_auto_20210413_0050	2021-04-18 04:12:44.782367+00
647	theme	0017_auto_20210413_0329	2021-04-18 04:12:45.627587+00
648	theme	0018_auto_20210417_0106	2021-04-18 04:12:45.760552+00
649	data	0005_formvalue_is_long_text_rich_text	2021-05-10 01:28:11.273943+00
650	formulary	0016_field_is_long_text_rich_text	2021-05-10 01:28:11.427427+00
651	formulary	0017_useraccessedby	2021-05-10 01:28:11.602484+00
652	formulary	0018_auto_20210507_1829	2021-05-10 01:28:12.386432+00
653	theme	0019_themefield_is_long_text_rich_text	2021-05-10 01:28:12.483692+00
654	data	0006_dynamicform_uuid	2021-05-15 04:54:51.123671+00
655	data	0007_auto_20210514_1559	2021-05-15 04:54:51.676814+00
656	data	0008_extractfiledata	2021-05-20 23:17:46.466915+00
657	listing	0004_delete_extractfiledata	2021-05-20 23:17:46.49118+00
658	formula	0003_auto_20210526_1335	2021-05-26 13:40:04.438281+00
660	formulary	0019_fieldtype_is_dynamic_evaluated	2021-05-27 19:00:52.537452+00
662	formula	0004_auto_20210527_1829	2021-05-27 19:36:22.068386+00
663	formulary	0020_fieldnumberformattype_has_to_enforce_decimal	2021-05-28 00:30:47.075076+00
664	formulary	0019_formulavariable	2021-06-07 14:31:36.339074+00
665	formulary	0021_formulavariable	2021-06-07 15:53:51.329065+00
666	formulary	0022_auto_20210607_1546	2021-06-07 17:06:46.06881+00
667	theme	0020_themeformulavariable	2021-06-07 17:19:07.599292+00
668	theme	0021_auto_20210607_1719	2021-06-07 17:22:03.740354+00
669	formulary	0023_auto_20210607_1747	2021-06-07 17:48:33.188576+00
670	theme	0022_auto_20210607_1747	2021-06-07 17:48:33.438515+00
\.


--
-- Data for Name: django_session; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.django_session (session_key, session_data, expire_date) FROM stdin;
thiin6pgkscp2rqhrftb3gdu1p0pprio	YTAwZGE0YWQ5MGI0NjNhNzQyMjc4NzA4NTZlZTlhY2VkYjQ1NTlhNjp7Il9hdXRoX3VzZXJfaWQiOiIyMCIsIl9hdXRoX3VzZXJfYmFja2VuZCI6InJlZmxvd19jcm0ubG9naW4ubW9kZWxzLkVtYWlsQmFja2VuZCIsIl9hdXRoX3VzZXJfaGFzaCI6IjFlNzIyYzczZmE2ZjhiM2MwODMxYTkyYzQzOTFjZWEzODI4M2Q0NjIifQ==	2019-06-10 00:00:49.226841+00
kfw8ql2j50uch6178vmyads9u5jfucs0	ZjZlYWQ5NDQxMjY4NzY3MjNiYTFhMTgyMWMyYzFiNTU3ZTUxYzRmYzp7Il9hdXRoX3VzZXJfaWQiOiI4IiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoibG9naW4ubW9kZWxzLkVtYWlsQmFja2VuZCIsIl9hdXRoX3VzZXJfaGFzaCI6ImEyZTZhNGU1ZTM5OGNmMDY4ODFkYzRiMTMxNjI1NmIzNTYyZTMzNDIifQ==	2019-01-17 16:30:34.23837+00
drkqwp8taw57f1aib0ryzf3y9v5sozjs	NTMyYWMxZDRlOWFhNWRjYTVmNTlmNmM3OGZlNTY0NzE0M2JjODM4OTp7Il9hdXRoX3VzZXJfaWQiOiI5IiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoibG9naW4ubW9kZWxzLkVtYWlsQmFja2VuZCIsIl9hdXRoX3VzZXJfaGFzaCI6ImFlY2VjOTgxY2U2ODBlYTdhZGU2YjIzOTEwODdiMmMzYzU1ZWMyNzAifQ==	2019-01-01 17:56:54.707659+00
e2i0eqcm00ckrdpkojf0lin9ht9nfdih	NTMyYWMxZDRlOWFhNWRjYTVmNTlmNmM3OGZlNTY0NzE0M2JjODM4OTp7Il9hdXRoX3VzZXJfaWQiOiI5IiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoibG9naW4ubW9kZWxzLkVtYWlsQmFja2VuZCIsIl9hdXRoX3VzZXJfaGFzaCI6ImFlY2VjOTgxY2U2ODBlYTdhZGU2YjIzOTEwODdiMmMzYzU1ZWMyNzAifQ==	2019-01-23 16:53:54.437925+00
yszw25ukpbuw7kiahlu2jx48rhjvmbrm	NTMyYWMxZDRlOWFhNWRjYTVmNTlmNmM3OGZlNTY0NzE0M2JjODM4OTp7Il9hdXRoX3VzZXJfaWQiOiI5IiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoibG9naW4ubW9kZWxzLkVtYWlsQmFja2VuZCIsIl9hdXRoX3VzZXJfaGFzaCI6ImFlY2VjOTgxY2U2ODBlYTdhZGU2YjIzOTEwODdiMmMzYzU1ZWMyNzAifQ==	2019-01-25 15:24:30.483249+00
4a6vd4kr8z114mx06donqewhcqcd21t8	OTQwZDExOTdlOWQwMmRiZTA1MWQ1Y2RmMDAwNWMzODdmNWVmYWFkNzp7Il9hdXRoX3VzZXJfaWQiOiIxMSIsIl9hdXRoX3VzZXJfYmFja2VuZCI6ImxvZ2luLm1vZGVscy5FbWFpbEJhY2tlbmQiLCJfYXV0aF91c2VyX2hhc2giOiI4YTFjMWNmY2IyZmJiZTgzNzdhM2E0MjRkMjllMmJhZmI5ZTQ2ZGQ1In0=	2019-01-27 21:12:13.120745+00
wlgr84iiyt8ec0gwkjykuq8262hf19a9	NTMyYWMxZDRlOWFhNWRjYTVmNTlmNmM3OGZlNTY0NzE0M2JjODM4OTp7Il9hdXRoX3VzZXJfaWQiOiI5IiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoibG9naW4ubW9kZWxzLkVtYWlsQmFja2VuZCIsIl9hdXRoX3VzZXJfaGFzaCI6ImFlY2VjOTgxY2U2ODBlYTdhZGU2YjIzOTEwODdiMmMzYzU1ZWMyNzAifQ==	2019-01-29 01:47:15.840419+00
336dt2stvo655ndscvye7fdbniyl70f1	NTMyYWMxZDRlOWFhNWRjYTVmNTlmNmM3OGZlNTY0NzE0M2JjODM4OTp7Il9hdXRoX3VzZXJfaWQiOiI5IiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoibG9naW4ubW9kZWxzLkVtYWlsQmFja2VuZCIsIl9hdXRoX3VzZXJfaGFzaCI6ImFlY2VjOTgxY2U2ODBlYTdhZGU2YjIzOTEwODdiMmMzYzU1ZWMyNzAifQ==	2019-01-29 20:17:00.774659+00
11bh0yw1bcxebf4dess3jhvlljzfiew1	NTMyYWMxZDRlOWFhNWRjYTVmNTlmNmM3OGZlNTY0NzE0M2JjODM4OTp7Il9hdXRoX3VzZXJfaWQiOiI5IiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoibG9naW4ubW9kZWxzLkVtYWlsQmFja2VuZCIsIl9hdXRoX3VzZXJfaGFzaCI6ImFlY2VjOTgxY2U2ODBlYTdhZGU2YjIzOTEwODdiMmMzYzU1ZWMyNzAifQ==	2019-01-30 21:17:40.53613+00
bqs7y0qphltflob68qpuw2tx3w6u23ym	NTMyYWMxZDRlOWFhNWRjYTVmNTlmNmM3OGZlNTY0NzE0M2JjODM4OTp7Il9hdXRoX3VzZXJfaWQiOiI5IiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoibG9naW4ubW9kZWxzLkVtYWlsQmFja2VuZCIsIl9hdXRoX3VzZXJfaGFzaCI6ImFlY2VjOTgxY2U2ODBlYTdhZGU2YjIzOTEwODdiMmMzYzU1ZWMyNzAifQ==	2019-01-31 23:40:29.035701+00
muj70o5k3wdsk9undxuq6e6lbzgsz1pq	NTMyYWMxZDRlOWFhNWRjYTVmNTlmNmM3OGZlNTY0NzE0M2JjODM4OTp7Il9hdXRoX3VzZXJfaWQiOiI5IiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoibG9naW4ubW9kZWxzLkVtYWlsQmFja2VuZCIsIl9hdXRoX3VzZXJfaGFzaCI6ImFlY2VjOTgxY2U2ODBlYTdhZGU2YjIzOTEwODdiMmMzYzU1ZWMyNzAifQ==	2019-01-07 23:53:47.823934+00
ksbr88fckz9199g5824ppg8b08bo3kad	NTMyYWMxZDRlOWFhNWRjYTVmNTlmNmM3OGZlNTY0NzE0M2JjODM4OTp7Il9hdXRoX3VzZXJfaWQiOiI5IiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoibG9naW4ubW9kZWxzLkVtYWlsQmFja2VuZCIsIl9hdXRoX3VzZXJfaGFzaCI6ImFlY2VjOTgxY2U2ODBlYTdhZGU2YjIzOTEwODdiMmMzYzU1ZWMyNzAifQ==	2019-02-14 01:36:08.853622+00
zp4ops145odxeu6od4syzdz8ircqscrf	NTMyYWMxZDRlOWFhNWRjYTVmNTlmNmM3OGZlNTY0NzE0M2JjODM4OTp7Il9hdXRoX3VzZXJfaWQiOiI5IiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoibG9naW4ubW9kZWxzLkVtYWlsQmFja2VuZCIsIl9hdXRoX3VzZXJfaGFzaCI6ImFlY2VjOTgxY2U2ODBlYTdhZGU2YjIzOTEwODdiMmMzYzU1ZWMyNzAifQ==	2019-02-14 20:53:25.362672+00
nh2lqwtjihryy4self1fetnbsj8qz2cy	NTMyYWMxZDRlOWFhNWRjYTVmNTlmNmM3OGZlNTY0NzE0M2JjODM4OTp7Il9hdXRoX3VzZXJfaWQiOiI5IiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoibG9naW4ubW9kZWxzLkVtYWlsQmFja2VuZCIsIl9hdXRoX3VzZXJfaGFzaCI6ImFlY2VjOTgxY2U2ODBlYTdhZGU2YjIzOTEwODdiMmMzYzU1ZWMyNzAifQ==	2019-01-10 02:15:16.098907+00
69ck3dg0wkvaoockb08dp1jpyudqz6va	NTMyYWMxZDRlOWFhNWRjYTVmNTlmNmM3OGZlNTY0NzE0M2JjODM4OTp7Il9hdXRoX3VzZXJfaWQiOiI5IiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoibG9naW4ubW9kZWxzLkVtYWlsQmFja2VuZCIsIl9hdXRoX3VzZXJfaGFzaCI6ImFlY2VjOTgxY2U2ODBlYTdhZGU2YjIzOTEwODdiMmMzYzU1ZWMyNzAifQ==	2019-02-15 02:12:14.020798+00
g3wn0fzsylhu14e8rncq4kg7c4w3ev33	NTMyYWMxZDRlOWFhNWRjYTVmNTlmNmM3OGZlNTY0NzE0M2JjODM4OTp7Il9hdXRoX3VzZXJfaWQiOiI5IiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoibG9naW4ubW9kZWxzLkVtYWlsQmFja2VuZCIsIl9hdXRoX3VzZXJfaGFzaCI6ImFlY2VjOTgxY2U2ODBlYTdhZGU2YjIzOTEwODdiMmMzYzU1ZWMyNzAifQ==	2019-02-15 14:52:44.903753+00
akwv7n05klq8agxwlgldjhjraf7yuqiz	NTMyYWMxZDRlOWFhNWRjYTVmNTlmNmM3OGZlNTY0NzE0M2JjODM4OTp7Il9hdXRoX3VzZXJfaWQiOiI5IiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoibG9naW4ubW9kZWxzLkVtYWlsQmFja2VuZCIsIl9hdXRoX3VzZXJfaGFzaCI6ImFlY2VjOTgxY2U2ODBlYTdhZGU2YjIzOTEwODdiMmMzYzU1ZWMyNzAifQ==	2019-02-15 15:37:15.088035+00
xa4m535oxesp2c2qcn7513nbx0phxphc	NTMyYWMxZDRlOWFhNWRjYTVmNTlmNmM3OGZlNTY0NzE0M2JjODM4OTp7Il9hdXRoX3VzZXJfaWQiOiI5IiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoibG9naW4ubW9kZWxzLkVtYWlsQmFja2VuZCIsIl9hdXRoX3VzZXJfaGFzaCI6ImFlY2VjOTgxY2U2ODBlYTdhZGU2YjIzOTEwODdiMmMzYzU1ZWMyNzAifQ==	2019-01-10 23:07:59.725933+00
wwufaxvbhb5xfkhywpoobp9h389q05s7	NTMyYWMxZDRlOWFhNWRjYTVmNTlmNmM3OGZlNTY0NzE0M2JjODM4OTp7Il9hdXRoX3VzZXJfaWQiOiI5IiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoibG9naW4ubW9kZWxzLkVtYWlsQmFja2VuZCIsIl9hdXRoX3VzZXJfaGFzaCI6ImFlY2VjOTgxY2U2ODBlYTdhZGU2YjIzOTEwODdiMmMzYzU1ZWMyNzAifQ==	2019-01-17 06:17:35.747726+00
3nt77jwui45w1fj20z5edfcddv47r84y	NTMyYWMxZDRlOWFhNWRjYTVmNTlmNmM3OGZlNTY0NzE0M2JjODM4OTp7Il9hdXRoX3VzZXJfaWQiOiI5IiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoibG9naW4ubW9kZWxzLkVtYWlsQmFja2VuZCIsIl9hdXRoX3VzZXJfaGFzaCI6ImFlY2VjOTgxY2U2ODBlYTdhZGU2YjIzOTEwODdiMmMzYzU1ZWMyNzAifQ==	2019-02-17 17:43:00.54553+00
ym9g7lm9x7gkqanwpw8w2dkok9bqtlyu	NTMyYWMxZDRlOWFhNWRjYTVmNTlmNmM3OGZlNTY0NzE0M2JjODM4OTp7Il9hdXRoX3VzZXJfaWQiOiI5IiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoibG9naW4ubW9kZWxzLkVtYWlsQmFja2VuZCIsIl9hdXRoX3VzZXJfaGFzaCI6ImFlY2VjOTgxY2U2ODBlYTdhZGU2YjIzOTEwODdiMmMzYzU1ZWMyNzAifQ==	2019-02-20 01:01:41.733665+00
16im4uknrkhtbkh369wllmjlaml3teuo	NTMyYWMxZDRlOWFhNWRjYTVmNTlmNmM3OGZlNTY0NzE0M2JjODM4OTp7Il9hdXRoX3VzZXJfaWQiOiI5IiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoibG9naW4ubW9kZWxzLkVtYWlsQmFja2VuZCIsIl9hdXRoX3VzZXJfaGFzaCI6ImFlY2VjOTgxY2U2ODBlYTdhZGU2YjIzOTEwODdiMmMzYzU1ZWMyNzAifQ==	2019-02-22 11:44:15.396112+00
duu04yq4edpaug8752fzuszotwe5r0vd	NTMyYWMxZDRlOWFhNWRjYTVmNTlmNmM3OGZlNTY0NzE0M2JjODM4OTp7Il9hdXRoX3VzZXJfaWQiOiI5IiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoibG9naW4ubW9kZWxzLkVtYWlsQmFja2VuZCIsIl9hdXRoX3VzZXJfaGFzaCI6ImFlY2VjOTgxY2U2ODBlYTdhZGU2YjIzOTEwODdiMmMzYzU1ZWMyNzAifQ==	2019-03-07 07:38:55.298805+00
fhwktil5pz8p9ypf2andsqutx4o0w98n	NTMyYWMxZDRlOWFhNWRjYTVmNTlmNmM3OGZlNTY0NzE0M2JjODM4OTp7Il9hdXRoX3VzZXJfaWQiOiI5IiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoibG9naW4ubW9kZWxzLkVtYWlsQmFja2VuZCIsIl9hdXRoX3VzZXJfaGFzaCI6ImFlY2VjOTgxY2U2ODBlYTdhZGU2YjIzOTEwODdiMmMzYzU1ZWMyNzAifQ==	2019-03-07 14:13:14.688896+00
sxyz8j2i1ky1lemo73gh5drup6yzba2g	NTMyYWMxZDRlOWFhNWRjYTVmNTlmNmM3OGZlNTY0NzE0M2JjODM4OTp7Il9hdXRoX3VzZXJfaWQiOiI5IiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoibG9naW4ubW9kZWxzLkVtYWlsQmFja2VuZCIsIl9hdXRoX3VzZXJfaGFzaCI6ImFlY2VjOTgxY2U2ODBlYTdhZGU2YjIzOTEwODdiMmMzYzU1ZWMyNzAifQ==	2019-03-08 02:20:43.476509+00
448x5d0zv9hj45f4yeg05l88tg9w19lz	NGQ4MTIzMjQ0YzY0M2UxY2JiZTc1MzdiZDZkMjVhMDJjZjg1MzY5Yjp7Il9hdXRoX3VzZXJfaWQiOiIxIiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoicmVmbG93X2NybS5sb2dpbi5tb2RlbHMuRW1haWxCYWNrZW5kIiwiX2F1dGhfdXNlcl9oYXNoIjoiODIzMDlhYjExYTU3N2UwMmNjNzE3ODA3ZWIzYzAzZjI1ZmYyNmMxNCJ9	2019-12-08 17:03:06.349687+00
5ffskdxsnwe0tlgn6m293fzzpj5ziy4j	OGQzZWQzODFjMGMwODlmMmI1YWVhMjdhYWI1NzQzZTgzMGI1MDEyMDp7Il9hdXRoX3VzZXJfaWQiOiIxIiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoicmVmbG93X2NybS5sb2dpbi5tb2RlbHMuRW1haWxCYWNrZW5kIiwiX2F1dGhfdXNlcl9oYXNoIjoiYWVjZWM5ODFjZTY4MGVhN2FkZTZiMjM5MTA4N2IyYzNjNTVlYzI3MCJ9	2019-05-01 15:44:41.450506+00
nxrbrain13zm6f6avb4nx5ypkbv10pwf	NDc0MmEyZDA3YzZiMGJmYWQ1ZDBlN2QzMzljZjIxMTI3OGIyN2NmZjp7Il9hdXRoX3VzZXJfaWQiOiIxNSIsIl9hdXRoX3VzZXJfYmFja2VuZCI6ImxvZ2luLm1vZGVscy5FbWFpbEJhY2tlbmQiLCJfYXV0aF91c2VyX2hhc2giOiI4OTE3OWQzNmQwNDU4YzIxMzMzNTRmMTA5YmI2NzZmOTMyYjI2OTk5In0=	2019-03-12 12:47:26.458525+00
3mm3n2g47v9tzt1vrri1u0ff03yo56kv	NGQ4MTIzMjQ0YzY0M2UxY2JiZTc1MzdiZDZkMjVhMDJjZjg1MzY5Yjp7Il9hdXRoX3VzZXJfaWQiOiIxIiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoicmVmbG93X2NybS5sb2dpbi5tb2RlbHMuRW1haWxCYWNrZW5kIiwiX2F1dGhfdXNlcl9oYXNoIjoiODIzMDlhYjExYTU3N2UwMmNjNzE3ODA3ZWIzYzAzZjI1ZmYyNmMxNCJ9	2019-06-29 14:09:29.253481+00
g1d1ed9p0j7eeorusfcvdady0evbhsqp	NDc0MmEyZDA3YzZiMGJmYWQ1ZDBlN2QzMzljZjIxMTI3OGIyN2NmZjp7Il9hdXRoX3VzZXJfaWQiOiIxNSIsIl9hdXRoX3VzZXJfYmFja2VuZCI6ImxvZ2luLm1vZGVscy5FbWFpbEJhY2tlbmQiLCJfYXV0aF91c2VyX2hhc2giOiI4OTE3OWQzNmQwNDU4YzIxMzMzNTRmMTA5YmI2NzZmOTMyYjI2OTk5In0=	2019-03-19 17:19:29.07304+00
pgvwlwjhjmx7tqha1a0l3kttanf5u97z	NDc0MmEyZDA3YzZiMGJmYWQ1ZDBlN2QzMzljZjIxMTI3OGIyN2NmZjp7Il9hdXRoX3VzZXJfaWQiOiIxNSIsIl9hdXRoX3VzZXJfYmFja2VuZCI6ImxvZ2luLm1vZGVscy5FbWFpbEJhY2tlbmQiLCJfYXV0aF91c2VyX2hhc2giOiI4OTE3OWQzNmQwNDU4YzIxMzMzNTRmMTA5YmI2NzZmOTMyYjI2OTk5In0=	2019-03-26 14:01:14.514307+00
7yr5azp5qx7ope2x8i92f770ogu710ek	NTMyYWMxZDRlOWFhNWRjYTVmNTlmNmM3OGZlNTY0NzE0M2JjODM4OTp7Il9hdXRoX3VzZXJfaWQiOiI5IiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoibG9naW4ubW9kZWxzLkVtYWlsQmFja2VuZCIsIl9hdXRoX3VzZXJfaGFzaCI6ImFlY2VjOTgxY2U2ODBlYTdhZGU2YjIzOTEwODdiMmMzYzU1ZWMyNzAifQ==	2019-03-26 19:09:14.716207+00
0l4xvwi5bc9tbywbh9f652mmf91phdlw	NTMyYWMxZDRlOWFhNWRjYTVmNTlmNmM3OGZlNTY0NzE0M2JjODM4OTp7Il9hdXRoX3VzZXJfaWQiOiI5IiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoibG9naW4ubW9kZWxzLkVtYWlsQmFja2VuZCIsIl9hdXRoX3VzZXJfaGFzaCI6ImFlY2VjOTgxY2U2ODBlYTdhZGU2YjIzOTEwODdiMmMzYzU1ZWMyNzAifQ==	2019-03-28 04:21:50.627311+00
28n9ykuwqezid297fec71mxo6d49uw7e	NDc0MmEyZDA3YzZiMGJmYWQ1ZDBlN2QzMzljZjIxMTI3OGIyN2NmZjp7Il9hdXRoX3VzZXJfaWQiOiIxNSIsIl9hdXRoX3VzZXJfYmFja2VuZCI6ImxvZ2luLm1vZGVscy5FbWFpbEJhY2tlbmQiLCJfYXV0aF91c2VyX2hhc2giOiI4OTE3OWQzNmQwNDU4YzIxMzMzNTRmMTA5YmI2NzZmOTMyYjI2OTk5In0=	2019-03-30 20:58:18.107528+00
eib0x2yjze9vak9e7i50oz3wbwdld4v2	NGQ4MTIzMjQ0YzY0M2UxY2JiZTc1MzdiZDZkMjVhMDJjZjg1MzY5Yjp7Il9hdXRoX3VzZXJfaWQiOiIxIiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoicmVmbG93X2NybS5sb2dpbi5tb2RlbHMuRW1haWxCYWNrZW5kIiwiX2F1dGhfdXNlcl9oYXNoIjoiODIzMDlhYjExYTU3N2UwMmNjNzE3ODA3ZWIzYzAzZjI1ZmYyNmMxNCJ9	2019-07-06 01:03:27.385357+00
gclixk6ig1phqjuasy3pnm745ym3i91o	NTMyYWMxZDRlOWFhNWRjYTVmNTlmNmM3OGZlNTY0NzE0M2JjODM4OTp7Il9hdXRoX3VzZXJfaWQiOiI5IiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoibG9naW4ubW9kZWxzLkVtYWlsQmFja2VuZCIsIl9hdXRoX3VzZXJfaGFzaCI6ImFlY2VjOTgxY2U2ODBlYTdhZGU2YjIzOTEwODdiMmMzYzU1ZWMyNzAifQ==	2019-04-03 00:29:53.388595+00
lauk6uv5oej05z7errzi2q6ptkxferi1	N2RiZDllMTI4ZDJmNDVkOGZjYjBjZjJjNzZhYjI3MWFkMGE5MmU3Yjp7Il9hdXRoX3VzZXJfaWQiOiI5IiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoicmVmbG93X2NybS5sb2dpbi5tb2RlbHMuRW1haWxCYWNrZW5kIiwiX2F1dGhfdXNlcl9oYXNoIjoiYWVjZWM5ODFjZTY4MGVhN2FkZTZiMjM5MTA4N2IyYzNjNTVlYzI3MCJ9	2019-05-16 17:16:50.806124+00
95asteyfl9leli9md3k2v0km2cbnlxqd	N2RiZDllMTI4ZDJmNDVkOGZjYjBjZjJjNzZhYjI3MWFkMGE5MmU3Yjp7Il9hdXRoX3VzZXJfaWQiOiI5IiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoicmVmbG93X2NybS5sb2dpbi5tb2RlbHMuRW1haWxCYWNrZW5kIiwiX2F1dGhfdXNlcl9oYXNoIjoiYWVjZWM5ODFjZTY4MGVhN2FkZTZiMjM5MTA4N2IyYzNjNTVlYzI3MCJ9	2019-05-16 17:40:43.294753+00
m8z4pc7srn36e9k77d5vaulh00yb9f0x	NGQ4MTIzMjQ0YzY0M2UxY2JiZTc1MzdiZDZkMjVhMDJjZjg1MzY5Yjp7Il9hdXRoX3VzZXJfaWQiOiIxIiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoicmVmbG93X2NybS5sb2dpbi5tb2RlbHMuRW1haWxCYWNrZW5kIiwiX2F1dGhfdXNlcl9oYXNoIjoiODIzMDlhYjExYTU3N2UwMmNjNzE3ODA3ZWIzYzAzZjI1ZmYyNmMxNCJ9	2019-07-16 02:35:34.73998+00
w4dtrjqtj8cdtep7pxcqxn0ms7e5nh1n	N2RiZDllMTI4ZDJmNDVkOGZjYjBjZjJjNzZhYjI3MWFkMGE5MmU3Yjp7Il9hdXRoX3VzZXJfaWQiOiI5IiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoicmVmbG93X2NybS5sb2dpbi5tb2RlbHMuRW1haWxCYWNrZW5kIiwiX2F1dGhfdXNlcl9oYXNoIjoiYWVjZWM5ODFjZTY4MGVhN2FkZTZiMjM5MTA4N2IyYzNjNTVlYzI3MCJ9	2019-05-16 19:53:57.73143+00
qm2tkwwzwr7uo3wjtqtv950y7b0zg76n	NGQ4MTIzMjQ0YzY0M2UxY2JiZTc1MzdiZDZkMjVhMDJjZjg1MzY5Yjp7Il9hdXRoX3VzZXJfaWQiOiIxIiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoicmVmbG93X2NybS5sb2dpbi5tb2RlbHMuRW1haWxCYWNrZW5kIiwiX2F1dGhfdXNlcl9oYXNoIjoiODIzMDlhYjExYTU3N2UwMmNjNzE3ODA3ZWIzYzAzZjI1ZmYyNmMxNCJ9	2019-07-16 18:45:28.303108+00
80jnaq10zkf04g909tf3634pkpyipepv	NTMyYWMxZDRlOWFhNWRjYTVmNTlmNmM3OGZlNTY0NzE0M2JjODM4OTp7Il9hdXRoX3VzZXJfaWQiOiI5IiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoibG9naW4ubW9kZWxzLkVtYWlsQmFja2VuZCIsIl9hdXRoX3VzZXJfaGFzaCI6ImFlY2VjOTgxY2U2ODBlYTdhZGU2YjIzOTEwODdiMmMzYzU1ZWMyNzAifQ==	2019-04-13 19:28:05.121715+00
0jvztnr56frh7r8ng87agzjig3zqo5x1	NTMyYWMxZDRlOWFhNWRjYTVmNTlmNmM3OGZlNTY0NzE0M2JjODM4OTp7Il9hdXRoX3VzZXJfaWQiOiI5IiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoibG9naW4ubW9kZWxzLkVtYWlsQmFja2VuZCIsIl9hdXRoX3VzZXJfaGFzaCI6ImFlY2VjOTgxY2U2ODBlYTdhZGU2YjIzOTEwODdiMmMzYzU1ZWMyNzAifQ==	2019-04-03 23:54:48.543138+00
qfm451o29kwcfwuk9tvhfd3445nxjzk5	NTMyYWMxZDRlOWFhNWRjYTVmNTlmNmM3OGZlNTY0NzE0M2JjODM4OTp7Il9hdXRoX3VzZXJfaWQiOiI5IiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoibG9naW4ubW9kZWxzLkVtYWlsQmFja2VuZCIsIl9hdXRoX3VzZXJfaGFzaCI6ImFlY2VjOTgxY2U2ODBlYTdhZGU2YjIzOTEwODdiMmMzYzU1ZWMyNzAifQ==	2019-04-04 13:02:01.234415+00
u3x10nusw2zppazkbkqi7pjf9dvettu0	NjZhMjc0MjljMjc4YjMzMDQ5ZDJkMmNhOGViMzFiMzZkYjE2MzUzNDp7Il9hdXRoX3VzZXJfaWQiOiIxIiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoicmVmbG93X2NybS5sb2dpbi5tb2RlbHMuRW1haWxCYWNrZW5kIiwiX2F1dGhfdXNlcl9oYXNoIjoiY2U4MGVhZjVlODI0YmIzNWFlYjFhZDM1Njc1ZGE2ODQ0YjZhYTA5MSJ9	2019-05-28 22:27:50.849743+00
026fie4lpbauhglhxs29zw119w8xarrb	NGQ4MTIzMjQ0YzY0M2UxY2JiZTc1MzdiZDZkMjVhMDJjZjg1MzY5Yjp7Il9hdXRoX3VzZXJfaWQiOiIxIiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoicmVmbG93X2NybS5sb2dpbi5tb2RlbHMuRW1haWxCYWNrZW5kIiwiX2F1dGhfdXNlcl9oYXNoIjoiODIzMDlhYjExYTU3N2UwMmNjNzE3ODA3ZWIzYzAzZjI1ZmYyNmMxNCJ9	2019-08-08 12:46:11.371852+00
052w1zmk8r3u3pk0qdzkpji6wyk3enjk	NDc0MmEyZDA3YzZiMGJmYWQ1ZDBlN2QzMzljZjIxMTI3OGIyN2NmZjp7Il9hdXRoX3VzZXJfaWQiOiIxNSIsIl9hdXRoX3VzZXJfYmFja2VuZCI6ImxvZ2luLm1vZGVscy5FbWFpbEJhY2tlbmQiLCJfYXV0aF91c2VyX2hhc2giOiI4OTE3OWQzNmQwNDU4YzIxMzMzNTRmMTA5YmI2NzZmOTMyYjI2OTk5In0=	2019-04-05 03:30:39.248567+00
7h9uzkrr270snbxqldslk72z76jnv1n1	YTQ5ODcwYzdmYzVjNDhlNDg3OWRiM2FmNjQ3YjY4ZDk4NmNjMjY2Mjp7Il9hdXRoX3VzZXJfaWQiOiIxIiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoicmVmbG93X2NybS5sb2dpbi5tb2RlbHMuRW1haWxCYWNrZW5kIiwiX2F1dGhfdXNlcl9oYXNoIjoiMzc1NDM0OWJjZGEwNzYwMWI4N2JmYzI1ZTcyZDAyNTc1NzU5MzdiMCJ9	2019-06-04 13:18:13.966568+00
kjrzkmdvbrui02ort0otllyfsm9wle9b	NGQ4MTIzMjQ0YzY0M2UxY2JiZTc1MzdiZDZkMjVhMDJjZjg1MzY5Yjp7Il9hdXRoX3VzZXJfaWQiOiIxIiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoicmVmbG93X2NybS5sb2dpbi5tb2RlbHMuRW1haWxCYWNrZW5kIiwiX2F1dGhfdXNlcl9oYXNoIjoiODIzMDlhYjExYTU3N2UwMmNjNzE3ODA3ZWIzYzAzZjI1ZmYyNmMxNCJ9	2019-06-11 14:39:34.742747+00
asw7m5xyb36lmar3cer77fj6htxhj77b	NGQ4MTIzMjQ0YzY0M2UxY2JiZTc1MzdiZDZkMjVhMDJjZjg1MzY5Yjp7Il9hdXRoX3VzZXJfaWQiOiIxIiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoicmVmbG93X2NybS5sb2dpbi5tb2RlbHMuRW1haWxCYWNrZW5kIiwiX2F1dGhfdXNlcl9oYXNoIjoiODIzMDlhYjExYTU3N2UwMmNjNzE3ODA3ZWIzYzAzZjI1ZmYyNmMxNCJ9	2019-06-11 18:25:23.909587+00
lgm7ab1t4xsh2k7bb8fo6iltovok8mug	.eJxVjMsOwiAQRf-FtSFQebo08TvIADOBWGlSWl0Y_9026UK355573izAupSwdpxDzezCJDv9sgjpjm0fZqRxeoUNPnHmu4FtqQmWOjV-aJ3fHlDH63H6KxXoZcs4ks4qnY2MZI1LHoYkMkE6K21BS5sQolU0aOMcoUALPnunALQyngT7fAGNkjw4:1l5XqM:mTPXPgiImbAtW-5grkfVq3_IWfn_aXx-6BPMGBxZHUw	2021-02-12 17:46:02.261839+00
2mv54pi12c2wjma25q9m13a1dsevtbxm	NGQ4MTIzMjQ0YzY0M2UxY2JiZTc1MzdiZDZkMjVhMDJjZjg1MzY5Yjp7Il9hdXRoX3VzZXJfaWQiOiIxIiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoicmVmbG93X2NybS5sb2dpbi5tb2RlbHMuRW1haWxCYWNrZW5kIiwiX2F1dGhfdXNlcl9oYXNoIjoiODIzMDlhYjExYTU3N2UwMmNjNzE3ODA3ZWIzYzAzZjI1ZmYyNmMxNCJ9	2019-12-23 16:10:35.381149+00
z6mttw21dv2cfo0sg2v4z1tibkbeonk5	.eJxVjMsOwiAQRf-FtSFQebo08TvIADOBWGlSWl0Y_9026UK355573izAupSwdpxDzezCJDv9sgjpjm0fZqRxeoUNPnHmu4FtqQmWOjV-aJ3fHlDH63H6KxXoZcs4ks4qnY2MZI1LHoYkMkE6K21BS5sQolU0aOMcoUALPnunALQyngT7fAGNkjw4:1kDGzb:6W9tES4KcPq-9QwDGfCDB-tRSpamuRZhY7C7ts-rq7s	2020-09-16 00:51:15.127625+00
2v3fhbrdhn791pqst1ktp6p1s6888pit	.eJxVjMsOwiAQRf-FtSFQebo08TvIADOBWGlSWl0Y_9026UK355573izAupSwdpxDzezCJDv9sgjpjm0fZqRxeoUNPnHmu4FtqQmWOjV-aJ3fHlDH63H6KxXoZcs4ks4qnY2MZI1LHoYkMkE6K21BS5sQolU0aOMcoUALPnunALQyngT7fAGNkjw4:1kkibF:ZXFV1IRb7QSFd4nBeDr3KSYDBbsaYu6e0aCkfUj0vsY	2020-12-17 07:00:21.412044+00
99vs1kcmse5eg2y6ya1zqn8m79o7r4g3	NGQ4MTIzMjQ0YzY0M2UxY2JiZTc1MzdiZDZkMjVhMDJjZjg1MzY5Yjp7Il9hdXRoX3VzZXJfaWQiOiIxIiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoicmVmbG93X2NybS5sb2dpbi5tb2RlbHMuRW1haWxCYWNrZW5kIiwiX2F1dGhfdXNlcl9oYXNoIjoiODIzMDlhYjExYTU3N2UwMmNjNzE3ODA3ZWIzYzAzZjI1ZmYyNmMxNCJ9	2019-07-31 13:32:33.74143+00
hk74uz406ndf706no38poxte2l08ag3u	.eJxVjMsOwiAQRf-FtSFQebo08TvIADOBWGlSWl0Y_9026UK355573izAupSwdpxDzezCJDv9sgjpjm0fZqRxeoUNPnHmu4FtqQmWOjV-aJ3fHlDH63H6KxXoZcs4ks4qnY2MZI1LHoYkMkE6K21BS5sQolU0aOMcoUALPnunALQyngT7fAGNkjw4:1lA1VW:qGBhZZqR2yakiOVbMIos8GVn0XSdJAWKf4M_i-BrKqg	2021-02-25 02:15:02.479768+00
0yfkxiuwtf5vrui0emw73gxs7lk65zfu	NGQ4MTIzMjQ0YzY0M2UxY2JiZTc1MzdiZDZkMjVhMDJjZjg1MzY5Yjp7Il9hdXRoX3VzZXJfaWQiOiIxIiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoicmVmbG93X2NybS5sb2dpbi5tb2RlbHMuRW1haWxCYWNrZW5kIiwiX2F1dGhfdXNlcl9oYXNoIjoiODIzMDlhYjExYTU3N2UwMmNjNzE3ODA3ZWIzYzAzZjI1ZmYyNmMxNCJ9	2020-02-28 19:26:11.907472+00
6ssnedugol1zr3qg1rmmevds0ipy2hwi	.eJxVjMsOwiAQRf-FtSFQebo08TvIADOBWGlSWl0Y_9026UK355573izAupSwdpxDzezCJDv9sgjpjm0fZqRxeoUNPnHmu4FtqQmWOjV-aJ3fHlDH63H6KxXoZcs4ks4qnY2MZI1LHoYkMkE6K21BS5sQolU0aOMcoUALPnunALQyngT7fAGNkjw4:1lNEpH:A16FDYPjqi_-GE8dvXkMBQiQLixTeQO028M8SJM4_7s	2021-04-02 13:06:03.487439+00
0h9tahqn9gct1306ucsbsg1qgjmc2e8f	.eJxVjMsOwiAQRf-FtSFQebo08TvIADOBWGlSWl0Y_9026UK355573izAupSwdpxDzezCJDv9sgjpjm0fZqRxeoUNPnHmu4FtqQmWOjV-aJ3fHlDH63H6KxXoZcs4ks4qnY2MZI1LHoYkMkE6K21BS5sQolU0aOMcoUALPnunALQyngT7fAGNkjw4:1kFi2h:CI3IcYSz0GszsXFBZ0VJj8rMTMc1K2sGjZL4yxiYk3Y	2020-09-22 18:08:31.187935+00
swcohst9jgtc0e3vvhnv584nztgjxkv8	.eJxVjMsOwiAQRf-FtSFQebo08TvIADOBWGlSWl0Y_9026UK355573izAupSwdpxDzezCJDv9sgjpjm0fZqRxeoUNPnHmu4FtqQmWOjV-aJ3fHlDH63H6KxXoZcs4ks4qnY2MZI1LHoYkMkE6K21BS5sQolU0aOMcoUALPnunALQyngT7fAGNkjw4:1kkpNj:Jf1ub45ewXEoDEreJBdwnCackFPk7hV08m-L0ctzt8M	2020-12-17 14:14:51.294804+00
ite2jwk4qnyof9j8phcfpk78j1lphnjf	NGQ4MTIzMjQ0YzY0M2UxY2JiZTc1MzdiZDZkMjVhMDJjZjg1MzY5Yjp7Il9hdXRoX3VzZXJfaWQiOiIxIiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoicmVmbG93X2NybS5sb2dpbi5tb2RlbHMuRW1haWxCYWNrZW5kIiwiX2F1dGhfdXNlcl9oYXNoIjoiODIzMDlhYjExYTU3N2UwMmNjNzE3ODA3ZWIzYzAzZjI1ZmYyNmMxNCJ9	2019-12-26 02:01:10.748824+00
hqcbj9cgu2q3l84uv6driqpvrtneh878	.eJxVjMsOwiAQRf-FtSFQebo08TvIADOBWGlSWl0Y_9026UK355573izAupSwdpxDzezCJDv9sgjpjm0fZqRxeoUNPnHmu4FtqQmWOjV-aJ3fHlDH63H6KxXoZcs4ks4qnY2MZI1LHoYkMkE6K21BS5sQolU0aOMcoUALPnunALQyngT7fAGNkjw4:1lEp1s:1N3EKpoQ4EQcJhEIxm7naTCHDfFo8Ny4499ADtg9HjU	2021-03-10 07:56:16.933043+00
2gb560qn201cjj283r4dqvyaft23293y	.eJxVjMsOwiAQRf-FtSFQebo08TvIADOBWGlSWl0Y_9026UK355573izAupSwdpxDzezCJDv9sgjpjm0fZqRxeoUNPnHmu4FtqQmWOjV-aJ3fHlDH63H6KxXoZcs4ks4qnY2MZI1LHoYkMkE6K21BS5sQolU0aOMcoUALPnunALQyngT7fAGNkjw4:1kFiPs:a1E79Mpgr4Q1NZjDcm_gH_JGAbYGjFaIjQWVr0lLbLM	2020-09-22 18:32:28.738493+00
zxrtg9dzr9glis1i1hk6eogfjhv6b03r	.eJxVjMsOwiAQRf-FtSFQebo08TvIADOBWGlSWl0Y_9026UK355573izAupSwdpxDzezCJDv9sgjpjm0fZqRxeoUNPnHmu4FtqQmWOjV-aJ3fHlDH63H6KxXoZcs4ks4qnY2MZI1LHoYkMkE6K21BS5sQolU0aOMcoUALPnunALQyngT7fAGNkjw4:1kkpNu:lV3fRE-bw7ZIeov__5Laz8BDWNDEgllY2dFJT3Tejvc	2020-12-17 14:15:02.343355+00
2qrx7cbnfw8w82sgvfy2swopc56if0cb	NGQ4MTIzMjQ0YzY0M2UxY2JiZTc1MzdiZDZkMjVhMDJjZjg1MzY5Yjp7Il9hdXRoX3VzZXJfaWQiOiIxIiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoicmVmbG93X2NybS5sb2dpbi5tb2RlbHMuRW1haWxCYWNrZW5kIiwiX2F1dGhfdXNlcl9oYXNoIjoiODIzMDlhYjExYTU3N2UwMmNjNzE3ODA3ZWIzYzAzZjI1ZmYyNmMxNCJ9	2019-08-13 05:33:15.692833+00
ro8oagldhygrzyl4bbqi0txz5bkoux2u	NGQ4MTIzMjQ0YzY0M2UxY2JiZTc1MzdiZDZkMjVhMDJjZjg1MzY5Yjp7Il9hdXRoX3VzZXJfaWQiOiIxIiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoicmVmbG93X2NybS5sb2dpbi5tb2RlbHMuRW1haWxCYWNrZW5kIiwiX2F1dGhfdXNlcl9oYXNoIjoiODIzMDlhYjExYTU3N2UwMmNjNzE3ODA3ZWIzYzAzZjI1ZmYyNmMxNCJ9	2019-12-26 03:33:06.695401+00
bpu31bmyid7yfnvoo324evj6tpmhaqly	.eJxVjMsOwiAQRf-FtSFQebo08TvIADOBWGlSWl0Y_9026UK355573izAupSwdpxDzezCJDv9sgjpjm0fZqRxeoUNPnHmu4FtqQmWOjV-aJ3fHlDH63H6KxXoZcs4ks4qnY2MZI1LHoYkMkE6K21BS5sQolU0aOMcoUALPnunALQyngT7fAGNkjw4:1lEuVH:pfqrHC1A2NMf3rpDIrgCOHApJG3LB7ajTjIIcKBCRxw	2021-03-10 13:46:59.54781+00
yw0q6u9uzejaa5jxtq68x0bdaojjg70v	NGQ4MTIzMjQ0YzY0M2UxY2JiZTc1MzdiZDZkMjVhMDJjZjg1MzY5Yjp7Il9hdXRoX3VzZXJfaWQiOiIxIiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoicmVmbG93X2NybS5sb2dpbi5tb2RlbHMuRW1haWxCYWNrZW5kIiwiX2F1dGhfdXNlcl9oYXNoIjoiODIzMDlhYjExYTU3N2UwMmNjNzE3ODA3ZWIzYzAzZjI1ZmYyNmMxNCJ9	2020-03-03 02:40:53.038811+00
qin561pjcqmfc21s8zawuaqufe39fdxk	.eJxVjMsOwiAQRf-FtSFQebo08TvIADOBWGlSWl0Y_9026UK355573izAupSwdpxDzezCJDv9sgjpjm0fZqRxeoUNPnHmu4FtqQmWOjV-aJ3fHlDH63H6KxXoZcs4ks4qnY2MZI1LHoYkMkE6K21BS5sQolU0aOMcoUALPnunALQyngT7fAGNkjw4:1kFoXs:QdBYdhiTgkoBV8TbkuOs9HPwa6Hxfclw9KyJULtPKc0	2020-09-23 01:05:08.985178+00
bmthozgtryozbldmmnhldnnyhn8ia53u	.eJxVjMsOwiAQRf-FtSFQebo08TvIADOBWGlSWl0Y_9026UK355573izAupSwdpxDzezCJDv9sgjpjm0fZqRxeoUNPnHmu4FtqQmWOjV-aJ3fHlDH63H6KxXoZcs4ks4qnY2MZI1LHoYkMkE6K21BS5sQolU0aOMcoUALPnunALQyngT7fAGNkjw4:1kkvIc:OHyw4SkGFMe-U8DjxS0kXF6lZ9ad1hb9lgxJSh6m0tY	2020-12-17 20:33:58.9117+00
l99rys9k8x52y2swannxab1e3w2vpvwk	NGQ4MTIzMjQ0YzY0M2UxY2JiZTc1MzdiZDZkMjVhMDJjZjg1MzY5Yjp7Il9hdXRoX3VzZXJfaWQiOiIxIiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoicmVmbG93X2NybS5sb2dpbi5tb2RlbHMuRW1haWxCYWNrZW5kIiwiX2F1dGhfdXNlcl9oYXNoIjoiODIzMDlhYjExYTU3N2UwMmNjNzE3ODA3ZWIzYzAzZjI1ZmYyNmMxNCJ9	2019-08-25 20:26:47.145659+00
59c0gbson1styo1z73itk20kih59k4ap	NGQ4MTIzMjQ0YzY0M2UxY2JiZTc1MzdiZDZkMjVhMDJjZjg1MzY5Yjp7Il9hdXRoX3VzZXJfaWQiOiIxIiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoicmVmbG93X2NybS5sb2dpbi5tb2RlbHMuRW1haWxCYWNrZW5kIiwiX2F1dGhfdXNlcl9oYXNoIjoiODIzMDlhYjExYTU3N2UwMmNjNzE3ODA3ZWIzYzAzZjI1ZmYyNmMxNCJ9	2019-12-26 04:00:22.685971+00
esl6dv3tikb0jjanw1rsu9vp0gl88c7v	NGQ4MTIzMjQ0YzY0M2UxY2JiZTc1MzdiZDZkMjVhMDJjZjg1MzY5Yjp7Il9hdXRoX3VzZXJfaWQiOiIxIiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoicmVmbG93X2NybS5sb2dpbi5tb2RlbHMuRW1haWxCYWNrZW5kIiwiX2F1dGhfdXNlcl9oYXNoIjoiODIzMDlhYjExYTU3N2UwMmNjNzE3ODA3ZWIzYzAzZjI1ZmYyNmMxNCJ9	2020-03-17 16:42:32.902728+00
ziqfr47mhh4bow6crh2i5wjiyg2ex331	.eJxVjM0KwjAQhN8lZwmSn-3Wo-BzhO1mQ4K1hbTVg_juptCDzvH7ZuatAm1rDtsiNZSoLsqgOv3Cgfgu026qpHF-hQafUvXekGktTGuZJ33UFn17UBmvx-jvKdOS202PYlo6EPTcy4CO6YwgAj5Z63xkw5gQIg0xkmWCDqxj4Oika059vrcbPPc:1kNOce:TZ833qHb3gEoDRRel6CktfwInyAL1leA-32K90Zf1h4	2020-10-13 23:01:24.868742+00
1p5h824kfc9bt0ane0xx8mv7d87qirqt	.eJxVjMsOwiAQRf-FtSFQebo08TvIADOBWGlSWl0Y_9026UK355573izAupSwdpxDzezCJDv9sgjpjm0fZqRxeoUNPnHmu4FtqQmWOjV-aJ3fHlDH63H6KxXoZcs4ks4qnY2MZI1LHoYkMkE6K21BS5sQolU0aOMcoUALPnunALQyngT7fAGNkjw4:1klJDZ:CzzvLsnoGBe7PFyrOG3gf_Lj4aiw0905WWHZpTsRZAI	2020-12-18 22:06:21.484912+00
a3kpuivrbbnr28vd2r0ektbxhho2wf8s	NGQ4MTIzMjQ0YzY0M2UxY2JiZTc1MzdiZDZkMjVhMDJjZjg1MzY5Yjp7Il9hdXRoX3VzZXJfaWQiOiIxIiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoicmVmbG93X2NybS5sb2dpbi5tb2RlbHMuRW1haWxCYWNrZW5kIiwiX2F1dGhfdXNlcl9oYXNoIjoiODIzMDlhYjExYTU3N2UwMmNjNzE3ODA3ZWIzYzAzZjI1ZmYyNmMxNCJ9	2019-08-25 23:05:07.573453+00
1bfncmvnt7v04qceqv20q0djep6qlqwy	NGQ4MTIzMjQ0YzY0M2UxY2JiZTc1MzdiZDZkMjVhMDJjZjg1MzY5Yjp7Il9hdXRoX3VzZXJfaWQiOiIxIiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoicmVmbG93X2NybS5sb2dpbi5tb2RlbHMuRW1haWxCYWNrZW5kIiwiX2F1dGhfdXNlcl9oYXNoIjoiODIzMDlhYjExYTU3N2UwMmNjNzE3ODA3ZWIzYzAzZjI1ZmYyNmMxNCJ9	2019-12-26 04:35:50.873084+00
l0ebra6kd4zc1kzvrw1765dcvz88bt9j	.eJxVjM0KwjAQhN8lZwmSn-3Wo-BzhO1mQ4K1hbTVg_juptCDzvH7ZuatAm1rDtsiNZSoLsqgOv3Cgfgu026qpHF-hQafUvXekGktTGuZJ33UFn17UBmvx-jvKdOS202PYlo6EPTcy4CO6YwgAj5Z63xkw5gQIg0xkmWCDqxj4Oika059vrcbPPc:1kNOcy:-hUzR4k9TVFg-yET941Mq1teUoX5akDrdbrab6cRfpE	2020-10-13 23:01:44.111485+00
tjwi43ghacsiqx8t5ioomia6r1p8i89s	.eJxVjMsOwiAQRf-FtSFQebo08TvIADOBWGlSWl0Y_9026UK355573izAupSwdpxDzezCJDv9sgjpjm0fZqRxeoUNPnHmu4FtqQmWOjV-aJ3fHlDH63H6KxXoZcs4ks4qnY2MZI1LHoYkMkE6K21BS5sQolU0aOMcoUALPnunALQyngT7fAGNkjw4:1klJF5:AWwQs7Xn48fwdnKBeDA-7XtHi6V2rsaHJOiL8BGlCmY	2020-12-18 22:07:55.947796+00
jtk1cjk0n0gwnlenzvqxsgqlf3msnla5	NGQ4MTIzMjQ0YzY0M2UxY2JiZTc1MzdiZDZkMjVhMDJjZjg1MzY5Yjp7Il9hdXRoX3VzZXJfaWQiOiIxIiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoicmVmbG93X2NybS5sb2dpbi5tb2RlbHMuRW1haWxCYWNrZW5kIiwiX2F1dGhfdXNlcl9oYXNoIjoiODIzMDlhYjExYTU3N2UwMmNjNzE3ODA3ZWIzYzAzZjI1ZmYyNmMxNCJ9	2019-08-26 00:34:13.489682+00
uyctead7juqebzqtms37firr6eqmf43m	NGQ4MTIzMjQ0YzY0M2UxY2JiZTc1MzdiZDZkMjVhMDJjZjg1MzY5Yjp7Il9hdXRoX3VzZXJfaWQiOiIxIiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoicmVmbG93X2NybS5sb2dpbi5tb2RlbHMuRW1haWxCYWNrZW5kIiwiX2F1dGhfdXNlcl9oYXNoIjoiODIzMDlhYjExYTU3N2UwMmNjNzE3ODA3ZWIzYzAzZjI1ZmYyNmMxNCJ9	2020-01-09 13:39:14.756931+00
dsg3wfg26xmownyq1kfx4p5grjw79nrr	NGQ4MTIzMjQ0YzY0M2UxY2JiZTc1MzdiZDZkMjVhMDJjZjg1MzY5Yjp7Il9hdXRoX3VzZXJfaWQiOiIxIiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoicmVmbG93X2NybS5sb2dpbi5tb2RlbHMuRW1haWxCYWNrZW5kIiwiX2F1dGhfdXNlcl9oYXNoIjoiODIzMDlhYjExYTU3N2UwMmNjNzE3ODA3ZWIzYzAzZjI1ZmYyNmMxNCJ9	2020-03-17 19:36:47.580276+00
cxvojg9ghg2ojbm3jyfqa48v0251bgg7	.eJxVjM0KwjAQhN8lZwmSn-3Wo-BzhO1mQ4K1hbTVg_juptCDzvH7ZuatAm1rDtsiNZSoLsqgOv3Cgfgu026qpHF-hQafUvXekGktTGuZJ33UFn17UBmvx-jvKdOS202PYlo6EPTcy4CO6YwgAj5Z63xkw5gQIg0xkmWCDqxj4Oika059vrcbPPc:1kNOd6:ytS3fqYO_04sfLDE2FgPa51FTyYXn2xgZzQfuDuV37M	2020-10-13 23:01:52.343624+00
go9deguerr96wg1yzhxq46x3cmwei9on	.eJxVjMsOwiAQRf-FtSFQebo08TvIADOBWGlSWl0Y_9026UK355573izAupSwdpxDzezCJDv9sgjpjm0fZqRxeoUNPnHmu4FtqQmWOjV-aJ3fHlDH63H6KxXoZcs4ks4qnY2MZI1LHoYkMkE6K21BS5sQolU0aOMcoUALPnunALQyngT7fAGNkjw4:1knZc3:PnaDLoUi4vi-dzCGXfl_93wxfHtiOXEsm4fk91H2ig4	2020-12-25 04:00:59.878372+00
5onnojkj9s20xatp774j9bms7qefggjj	NGQ4MTIzMjQ0YzY0M2UxY2JiZTc1MzdiZDZkMjVhMDJjZjg1MzY5Yjp7Il9hdXRoX3VzZXJfaWQiOiIxIiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoicmVmbG93X2NybS5sb2dpbi5tb2RlbHMuRW1haWxCYWNrZW5kIiwiX2F1dGhfdXNlcl9oYXNoIjoiODIzMDlhYjExYTU3N2UwMmNjNzE3ODA3ZWIzYzAzZjI1ZmYyNmMxNCJ9	2020-01-09 14:56:07.47976+00
ptgnynnycmzckk4elcvdoevwc0k9tumb	.eJxVjM0KwjAQhN8lZwmSn-3Wo-BzhO1mQ4K1hbTVg_juptCDzvH7ZuatAm1rDtsiNZSoLsqgOv3Cgfgu026qpHF-hQafUvXekGktTGuZJ33UFn17UBmvx-jvKdOS202PYlo6EPTcy4CO6YwgAj5Z63xkw5gQIg0xkmWCDqxj4Oika059vrcbPPc:1kNOx6:J7wXgXB8Ibi5Ghgrj3sO0KaPj3s23TDgtjHMDsU5ErI	2020-10-13 23:22:32.686781+00
b5n6fs8osltqiv5fh0mx6qt4da4que3d	.eJxVjMsOwiAQRf-FtSFQebo08TvIADOBWGlSWl0Y_9026UK355573izAupSwdpxDzezCJDv9sgjpjm0fZqRxeoUNPnHmu4FtqQmWOjV-aJ3fHlDH63H6KxXoZcs4ks4qnY2MZI1LHoYkMkE6K21BS5sQolU0aOMcoUALPnunALQyngT7fAGNkjw4:1knkg6:z0Tr1dD7fUGqhI4DHpjT1e-Nar2VnRY13UIS-KIqJdU	2020-12-25 15:49:54.885333+00
tn7jmf7laxpk9a8x6rrvk3pmvkv15wdx	NGQ4MTIzMjQ0YzY0M2UxY2JiZTc1MzdiZDZkMjVhMDJjZjg1MzY5Yjp7Il9hdXRoX3VzZXJfaWQiOiIxIiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoicmVmbG93X2NybS5sb2dpbi5tb2RlbHMuRW1haWxCYWNrZW5kIiwiX2F1dGhfdXNlcl9oYXNoIjoiODIzMDlhYjExYTU3N2UwMmNjNzE3ODA3ZWIzYzAzZjI1ZmYyNmMxNCJ9	2019-09-04 23:46:55.528198+00
hwhvgle67ftge2bgjwfn78z5age3qm6r	NGQ4MTIzMjQ0YzY0M2UxY2JiZTc1MzdiZDZkMjVhMDJjZjg1MzY5Yjp7Il9hdXRoX3VzZXJfaWQiOiIxIiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoicmVmbG93X2NybS5sb2dpbi5tb2RlbHMuRW1haWxCYWNrZW5kIiwiX2F1dGhfdXNlcl9oYXNoIjoiODIzMDlhYjExYTU3N2UwMmNjNzE3ODA3ZWIzYzAzZjI1ZmYyNmMxNCJ9	2020-01-27 16:51:38.649226+00
1oql4u7t8agvr9ry6zfvxftxjli4jmjm	NGQ4MTIzMjQ0YzY0M2UxY2JiZTc1MzdiZDZkMjVhMDJjZjg1MzY5Yjp7Il9hdXRoX3VzZXJfaWQiOiIxIiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoicmVmbG93X2NybS5sb2dpbi5tb2RlbHMuRW1haWxCYWNrZW5kIiwiX2F1dGhfdXNlcl9oYXNoIjoiODIzMDlhYjExYTU3N2UwMmNjNzE3ODA3ZWIzYzAzZjI1ZmYyNmMxNCJ9	2020-04-04 16:47:46.588983+00
555lmsgxt70zdz7f0aoeidn88yvz9cnc	.eJxVjEEOgyAQRe_CujHgiAxdNvEcZIAhkFpNRNtF07tXExft9v3331s42tbstsqLK1FchRKXX-Yp3Hk6hoXTOL_cDp-8NIfB01oCrWWemlOrzfCgMt7O018pU817JibVIoGR3vQge98lZVvlg4kdIURmr4LFNqAGVgYYvUwcIkrSSVvoxecLhTU8HA:1koVZx:40kQV2nmS2yPvUQegqT0z3CPxTvB8TbHDmYymK2kql0	2020-12-27 17:54:41.937805+00
uaw1yxh0ham9uz8nzu7r9t2xz8ts3rij	NGQ4MTIzMjQ0YzY0M2UxY2JiZTc1MzdiZDZkMjVhMDJjZjg1MzY5Yjp7Il9hdXRoX3VzZXJfaWQiOiIxIiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoicmVmbG93X2NybS5sb2dpbi5tb2RlbHMuRW1haWxCYWNrZW5kIiwiX2F1dGhfdXNlcl9oYXNoIjoiODIzMDlhYjExYTU3N2UwMmNjNzE3ODA3ZWIzYzAzZjI1ZmYyNmMxNCJ9	2019-09-04 23:50:08.660696+00
7h8soui9y9n8iajhj3lsw8kl3wtst966	NGQ4MTIzMjQ0YzY0M2UxY2JiZTc1MzdiZDZkMjVhMDJjZjg1MzY5Yjp7Il9hdXRoX3VzZXJfaWQiOiIxIiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoicmVmbG93X2NybS5sb2dpbi5tb2RlbHMuRW1haWxCYWNrZW5kIiwiX2F1dGhfdXNlcl9oYXNoIjoiODIzMDlhYjExYTU3N2UwMmNjNzE3ODA3ZWIzYzAzZjI1ZmYyNmMxNCJ9	2020-02-11 21:52:04.838318+00
fenvf8m7gkbq129ryd26kd3wau3ciox9	NGQ4MTIzMjQ0YzY0M2UxY2JiZTc1MzdiZDZkMjVhMDJjZjg1MzY5Yjp7Il9hdXRoX3VzZXJfaWQiOiIxIiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoicmVmbG93X2NybS5sb2dpbi5tb2RlbHMuRW1haWxCYWNrZW5kIiwiX2F1dGhfdXNlcl9oYXNoIjoiODIzMDlhYjExYTU3N2UwMmNjNzE3ODA3ZWIzYzAzZjI1ZmYyNmMxNCJ9	2020-04-15 14:28:02.157452+00
i7i7u202gc0k0d621f3wixlj1yl3gvuq	.eJxVjMsOwiAQRf-FtSFQebo08TvIADOBWGlSWl0Y_9026UK355573izAupSwdpxDzezCJDv9sgjpjm0fZqRxeoUNPnHmu4FtqQmWOjV-aJ3fHlDH63H6KxXoZcs4ks4qnY2MZI1LHoYkMkE6K21BS5sQolU0aOMcoUALPnunALQyngT7fAGNkjw4:1koujX:cmOb-9qxEDNMdSiTs5INNnrYVXCApTg6q_6NXAHBQtM	2020-12-28 20:46:15.246854+00
zhqzi0bst01a5fvgdt6gez7slnq63v14	NGQ4MTIzMjQ0YzY0M2UxY2JiZTc1MzdiZDZkMjVhMDJjZjg1MzY5Yjp7Il9hdXRoX3VzZXJfaWQiOiIxIiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoicmVmbG93X2NybS5sb2dpbi5tb2RlbHMuRW1haWxCYWNrZW5kIiwiX2F1dGhfdXNlcl9oYXNoIjoiODIzMDlhYjExYTU3N2UwMmNjNzE3ODA3ZWIzYzAzZjI1ZmYyNmMxNCJ9	2019-09-05 00:40:28.864719+00
xd5uv4amhnnmv7fvvcxgy7hvyi60ga8f	NGQ4MTIzMjQ0YzY0M2UxY2JiZTc1MzdiZDZkMjVhMDJjZjg1MzY5Yjp7Il9hdXRoX3VzZXJfaWQiOiIxIiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoicmVmbG93X2NybS5sb2dpbi5tb2RlbHMuRW1haWxCYWNrZW5kIiwiX2F1dGhfdXNlcl9oYXNoIjoiODIzMDlhYjExYTU3N2UwMmNjNzE3ODA3ZWIzYzAzZjI1ZmYyNmMxNCJ9	2020-02-19 00:41:47.78945+00
nrlg95u0dg8spjgxr4ka4i60hym8bhly	.eJxVjMsOwiAQRf-FtSFQebo08TvIADOBWGlSWl0Y_9026UK355573izAupSwdpxDzezCJDv9sgjpjm0fZqRxeoUNPnHmu4FtqQmWOjV-aJ3fHlDH63H6KxXoZcs4ks4qnY2MZI1LHoYkMkE6K21BS5sQolU0aOMcoUALPnunALQyngT7fAGNkjw4:1koujc:c6dy-1bqoK9dNUnlE9BWeA9zwu-fsjfXFVotWXQ2dg4	2020-12-28 20:46:20.450461+00
uohi2eyhd8z59s7wdhnx8rjd2hd4y8fr	NGQ4MTIzMjQ0YzY0M2UxY2JiZTc1MzdiZDZkMjVhMDJjZjg1MzY5Yjp7Il9hdXRoX3VzZXJfaWQiOiIxIiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoicmVmbG93X2NybS5sb2dpbi5tb2RlbHMuRW1haWxCYWNrZW5kIiwiX2F1dGhfdXNlcl9oYXNoIjoiODIzMDlhYjExYTU3N2UwMmNjNzE3ODA3ZWIzYzAzZjI1ZmYyNmMxNCJ9	2019-09-15 17:16:12.33353+00
b4u33wrxzzrt3eick05iep5ekd5gbvf2	NGQ4MTIzMjQ0YzY0M2UxY2JiZTc1MzdiZDZkMjVhMDJjZjg1MzY5Yjp7Il9hdXRoX3VzZXJfaWQiOiIxIiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoicmVmbG93X2NybS5sb2dpbi5tb2RlbHMuRW1haWxCYWNrZW5kIiwiX2F1dGhfdXNlcl9oYXNoIjoiODIzMDlhYjExYTU3N2UwMmNjNzE3ODA3ZWIzYzAzZjI1ZmYyNmMxNCJ9	2020-04-20 17:45:37.852571+00
p11jdmxicrqss8kahm94bl73yb33u9z8	.eJxVjMsOwiAQRf-FtSFQebo08TvIADOBWGlSWl0Y_9026UK355573izAupSwdpxDzezCJDv9sgjpjm0fZqRxeoUNPnHmu4FtqQmWOjV-aJ3fHlDH63H6KxXoZcs4ks4qnY2MZI1LHoYkMkE6K21BS5sQolU0aOMcoUALPnunALQyngT7fAGNkjw4:1kqmnP:GgSDe9HqxygDG_ir6ue4VdXT80SyqcUrTRhS-gAcn_c	2021-01-03 00:41:59.650153+00
64jjydsssg6ix88vzkywisll7vzoul6y	NGQ4MTIzMjQ0YzY0M2UxY2JiZTc1MzdiZDZkMjVhMDJjZjg1MzY5Yjp7Il9hdXRoX3VzZXJfaWQiOiIxIiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoicmVmbG93X2NybS5sb2dpbi5tb2RlbHMuRW1haWxCYWNrZW5kIiwiX2F1dGhfdXNlcl9oYXNoIjoiODIzMDlhYjExYTU3N2UwMmNjNzE3ODA3ZWIzYzAzZjI1ZmYyNmMxNCJ9	2019-09-19 17:26:02.354088+00
geli4fj5n97yuzfby2uw7hvkobv23ps4	NGQ4MTIzMjQ0YzY0M2UxY2JiZTc1MzdiZDZkMjVhMDJjZjg1MzY5Yjp7Il9hdXRoX3VzZXJfaWQiOiIxIiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoicmVmbG93X2NybS5sb2dpbi5tb2RlbHMuRW1haWxCYWNrZW5kIiwiX2F1dGhfdXNlcl9oYXNoIjoiODIzMDlhYjExYTU3N2UwMmNjNzE3ODA3ZWIzYzAzZjI1ZmYyNmMxNCJ9	2020-04-29 16:00:16.31834+00
bnziqs0xzrcj4hlw79e515a7n4kxv454	.eJxVjMsOwiAQRf-FtSFQebo08TvIADOBWGlSWl0Y_9026UK355573izAupSwdpxDzezCJDv9sgjpjm0fZqRxeoUNPnHmu4FtqQmWOjV-aJ3fHlDH63H6KxXoZcs4ks4qnY2MZI1LHoYkMkE6K21BS5sQolU0aOMcoUALPnunALQyngT7fAGNkjw4:1ktjJT:jM1rx0Fd1X_MJ9ChjdtOGREbE3CK93dwuN3YKp12OGc	2021-01-11 03:35:15.706876+00
a67uln6fmx821x4dzqdekeb3v67klguu	NGQ4MTIzMjQ0YzY0M2UxY2JiZTc1MzdiZDZkMjVhMDJjZjg1MzY5Yjp7Il9hdXRoX3VzZXJfaWQiOiIxIiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoicmVmbG93X2NybS5sb2dpbi5tb2RlbHMuRW1haWxCYWNrZW5kIiwiX2F1dGhfdXNlcl9oYXNoIjoiODIzMDlhYjExYTU3N2UwMmNjNzE3ODA3ZWIzYzAzZjI1ZmYyNmMxNCJ9	2019-10-06 21:39:42.669513+00
7jc0govulddpzd4k10cgtu3x59m1y97n	NGQ4MTIzMjQ0YzY0M2UxY2JiZTc1MzdiZDZkMjVhMDJjZjg1MzY5Yjp7Il9hdXRoX3VzZXJfaWQiOiIxIiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoicmVmbG93X2NybS5sb2dpbi5tb2RlbHMuRW1haWxCYWNrZW5kIiwiX2F1dGhfdXNlcl9oYXNoIjoiODIzMDlhYjExYTU3N2UwMmNjNzE3ODA3ZWIzYzAzZjI1ZmYyNmMxNCJ9	2020-05-11 05:06:48.634116+00
klvfuj8e7lajpwqkpg8o4pl53zj8jq0t	.eJxVjMsOwiAQRf-FtSFQebo08TvIADOBWGlSWl0Y_9026UK355573izAupSwdpxDzezCJDv9sgjpjm0fZqRxeoUNPnHmu4FtqQmWOjV-aJ3fHlDH63H6KxXoZcs4ks4qnY2MZI1LHoYkMkE6K21BS5sQolU0aOMcoUALPnunALQyngT7fAGNkjw4:1ktjJU:-r6NXb0lt_DtMPg1OqJL2sKCDCwYm6p8ghEKJcQxfRc	2021-01-11 03:35:16.93932+00
2xr7i8pio66djemgh2ftj7wh3ekkqle0	.eJxVjEEOgyAQRe_CujHgiAxdNvEcZIAhkFpNRNtF07tXExft9v3331s42tbstsqLK1FchRKXX-Yp3Hk6hoXTOL_cDp-8NIfB01oCrWWemlOrzfCgMt7O018pU817JibVIoGR3vQge98lZVvlg4kdIURmr4LFNqAGVgYYvUwcIkrSSVvoxecLhTU8HA:1l57vh:8apMsXEcOWawY5vquT48mBEzQZZI45_wBm7zDAPFHtU	2021-02-11 14:05:49.582643+00
b2c9vv8nan94avj5cfjab0zpjuzc5163	NGQ4MTIzMjQ0YzY0M2UxY2JiZTc1MzdiZDZkMjVhMDJjZjg1MzY5Yjp7Il9hdXRoX3VzZXJfaWQiOiIxIiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoicmVmbG93X2NybS5sb2dpbi5tb2RlbHMuRW1haWxCYWNrZW5kIiwiX2F1dGhfdXNlcl9oYXNoIjoiODIzMDlhYjExYTU3N2UwMmNjNzE3ODA3ZWIzYzAzZjI1ZmYyNmMxNCJ9	2020-05-31 01:39:00.453705+00
u10lyu5nv0i0wiy0ekpkpsauxd0qgk5j	.eJxVjMsOwiAQRf-FtSFQebo08TvIADOBWGlSWl0Y_9026UK355573izAupSwdpxDzezCJDv9sgjpjm0fZqRxeoUNPnHmu4FtqQmWOjV-aJ3fHlDH63H6KxXoZcs4ks4qnY2MZI1LHoYkMkE6K21BS5sQolU0aOMcoUALPnunALQyngT7fAGNkjw4:1l58Om:7-HcVTJm9AWJ7L_zjlGGfFySOZexARh5ZuGJqtZDkgo	2021-02-11 14:35:52.691978+00
nw1brx4uucjolg1bwqkj4u2mten2mirl	NGQ4MTIzMjQ0YzY0M2UxY2JiZTc1MzdiZDZkMjVhMDJjZjg1MzY5Yjp7Il9hdXRoX3VzZXJfaWQiOiIxIiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoicmVmbG93X2NybS5sb2dpbi5tb2RlbHMuRW1haWxCYWNrZW5kIiwiX2F1dGhfdXNlcl9oYXNoIjoiODIzMDlhYjExYTU3N2UwMmNjNzE3ODA3ZWIzYzAzZjI1ZmYyNmMxNCJ9	2019-11-01 21:45:54.812639+00
vhuwgm0uks44f933n2pbn4eiegtkqzvk	YzQ0YmNjODg1ZmU3YTk1YWFiYWExN2JiM2MxMDJiYzMwZDQzMjBlOTp7Il9hdXRoX3VzZXJfaWQiOiIxIiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoicmVmbG93X3NlcnZlci5hdXRoZW50aWNhdGlvbi5iYWNrZW5kcy5FbWFpbEJhY2tlbmQiLCJfYXV0aF91c2VyX2hhc2giOiI1MzA3MjA4ODk1NjNhOWY1YTgyNjFmYzNiNzk4OGRlOWNiNGE5NGE4In0=	2020-06-29 20:35:10.504085+00
c65n8mzs4cswq4pol0c3weuj25ubna57	.eJxVjMsOwiAQRf-FtSFQebo08TvIADOBWGlSWl0Y_9026UK355573izAupSwdpxDzezCJDv9sgjpjm0fZqRxeoUNPnHmu4FtqQmWOjV-aJ3fHlDH63H6KxXoZcs4ks4qnY2MZI1LHoYkMkE6K21BS5sQolU0aOMcoUALPnunALQyngT7fAGNkjw4:1l5CBS:gRrONarETEX1-RKsr1LFLz6zm4FwTApF9gJdUzR98RY	2021-02-11 18:38:22.33985+00
u0ycrnddynltg35ydwul8vne8jlq3ofc	NGQ4MTIzMjQ0YzY0M2UxY2JiZTc1MzdiZDZkMjVhMDJjZjg1MzY5Yjp7Il9hdXRoX3VzZXJfaWQiOiIxIiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoicmVmbG93X2NybS5sb2dpbi5tb2RlbHMuRW1haWxCYWNrZW5kIiwiX2F1dGhfdXNlcl9oYXNoIjoiODIzMDlhYjExYTU3N2UwMmNjNzE3ODA3ZWIzYzAzZjI1ZmYyNmMxNCJ9	2019-11-02 00:08:01.558023+00
f9vbpqi7nzccg0o4gp8slqvb49dwz0oy	M2IyZjY2OGY2NzRhMzI0M2YwY2Q2MDNkZTM2ZDg4MjlkM2NhNzM0ODp7Il9hdXRoX3VzZXJfaWQiOiIxIiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoicmVmbG93X3NlcnZlci5hdXRoZW50aWNhdGlvbi5iYWNrZW5kcy5FbWFpbEJhY2tlbmQiLCJfYXV0aF91c2VyX2hhc2giOiI0ZjBkOTk3NTA5ZWIwMmQ4N2RkZDdjNTUyYmNjNTE1OTI1NGM1OGMxIn0=	2020-07-03 07:55:02.75641+00
fc0orim50lf7rakj3orii6fy0fg9ghjw	.eJxVjMsOwiAQRf-FtSFQebo08TvIADOBWGlSWl0Y_9026UK355573izAupSwdpxDzezCJDv9sgjpjm0fZqRxeoUNPnHmu4FtqQmWOjV-aJ3fHlDH63H6KxXoZcs4ks4qnY2MZI1LHoYkMkE6K21BS5sQolU0aOMcoUALPnunALQyngT7fAGNkjw4:1l5D1P:VwKxWqHvG8N4jFDWRG-wpQvsREAJwXbNarivOc3ZWfM	2021-02-11 19:32:03.106135+00
msxcgfooayw6k88b12nhbsmyvwc8xpcn	M2IyZjY2OGY2NzRhMzI0M2YwY2Q2MDNkZTM2ZDg4MjlkM2NhNzM0ODp7Il9hdXRoX3VzZXJfaWQiOiIxIiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoicmVmbG93X3NlcnZlci5hdXRoZW50aWNhdGlvbi5iYWNrZW5kcy5FbWFpbEJhY2tlbmQiLCJfYXV0aF91c2VyX2hhc2giOiI0ZjBkOTk3NTA5ZWIwMmQ4N2RkZDdjNTUyYmNjNTE1OTI1NGM1OGMxIn0=	2020-07-08 15:12:52.059518+00
eky6zjm3boptewq4sdfntim56o1vo4j1	.eJxVjMsOwiAQRf-FtSFQebo08TvIADOBWGlSWl0Y_9026UK355573izAupSwdpxDzezCJDv9sgjpjm0fZqRxeoUNPnHmu4FtqQmWOjV-aJ3fHlDH63H6KxXoZcs4ks4qnY2MZI1LHoYkMkE6K21BS5sQolU0aOMcoUALPnunALQyngT7fAGNkjw4:1l5DFQ:0pB3J770MKRlpYnSIkmR23au1njwSPEo4SQU-kgsqLU	2021-02-11 19:46:32.254096+00
lxbl6plfrnnqsf6ixovm14lwvxfc88fv	NjEzMjFhNDY5Yjg2MTZlZGEyZDQ4NGE3MjQ1YTI5MTgwMzRmMzFmMzp7Il9hdXRoX3VzZXJfaWQiOiIxIiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoicmVmbG93X3NlcnZlci5hdXRoZW50aWNhdGlvbi5iYWNrZW5kcy5FbWFpbEJhY2tlbmQiLCJfYXV0aF91c2VyX2hhc2giOiI0MTI1OGZiMmE5OTk0MzA5YWI1Nzc2MmY4NDI3ZTU0YzM2NGU1ZTEwIn0=	2020-07-17 23:42:33.102032+00
0by2wqvo5ufq3jacb50xuvf8qg61mwyl	.eJxVjMsOwiAQRf-FtSFQebo08TvIADOBWGlSWl0Y_9026UK355573izAupSwdpxDzezCJDv9sgjpjm0fZqRxeoUNPnHmu4FtqQmWOjV-aJ3fHlDH63H6KxXoZcs4ks4qnY2MZI1LHoYkMkE6K21BS5sQolU0aOMcoUALPnunALQyngT7fAGNkjw4:1l5TgW:d0VxROKTlSnJjVWCVJHTbCtTvuzsT2S14lAyrPsfRvA	2021-02-12 13:19:36.760096+00
2w9owb459kzgxfdyiefaqz9z4tfkqiuk	NjEzMjFhNDY5Yjg2MTZlZGEyZDQ4NGE3MjQ1YTI5MTgwMzRmMzFmMzp7Il9hdXRoX3VzZXJfaWQiOiIxIiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoicmVmbG93X3NlcnZlci5hdXRoZW50aWNhdGlvbi5iYWNrZW5kcy5FbWFpbEJhY2tlbmQiLCJfYXV0aF91c2VyX2hhc2giOiI0MTI1OGZiMmE5OTk0MzA5YWI1Nzc2MmY4NDI3ZTU0YzM2NGU1ZTEwIn0=	2020-07-28 22:27:22.321445+00
xfdmzws7wsjcqud4qeky89a8v4ow0sxr	NGQ4MTIzMjQ0YzY0M2UxY2JiZTc1MzdiZDZkMjVhMDJjZjg1MzY5Yjp7Il9hdXRoX3VzZXJfaWQiOiIxIiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoicmVmbG93X2NybS5sb2dpbi5tb2RlbHMuRW1haWxCYWNrZW5kIiwiX2F1dGhfdXNlcl9oYXNoIjoiODIzMDlhYjExYTU3N2UwMmNjNzE3ODA3ZWIzYzAzZjI1ZmYyNmMxNCJ9	2019-11-08 14:12:17.255722+00
z912cclyxuigp2ihvzxpd7c9btltxjpb	NjEzMjFhNDY5Yjg2MTZlZGEyZDQ4NGE3MjQ1YTI5MTgwMzRmMzFmMzp7Il9hdXRoX3VzZXJfaWQiOiIxIiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoicmVmbG93X3NlcnZlci5hdXRoZW50aWNhdGlvbi5iYWNrZW5kcy5FbWFpbEJhY2tlbmQiLCJfYXV0aF91c2VyX2hhc2giOiI0MTI1OGZiMmE5OTk0MzA5YWI1Nzc2MmY4NDI3ZTU0YzM2NGU1ZTEwIn0=	2020-07-28 22:27:42.276343+00
jkg76ql7vci87opqopra4bqvx7nib8rn	NGQ4MTIzMjQ0YzY0M2UxY2JiZTc1MzdiZDZkMjVhMDJjZjg1MzY5Yjp7Il9hdXRoX3VzZXJfaWQiOiIxIiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoicmVmbG93X2NybS5sb2dpbi5tb2RlbHMuRW1haWxCYWNrZW5kIiwiX2F1dGhfdXNlcl9oYXNoIjoiODIzMDlhYjExYTU3N2UwMmNjNzE3ODA3ZWIzYzAzZjI1ZmYyNmMxNCJ9	2019-11-14 02:36:29.738193+00
bh31yb52i65b909vi8rwr4yvx8fx1bs2	NjEzMjFhNDY5Yjg2MTZlZGEyZDQ4NGE3MjQ1YTI5MTgwMzRmMzFmMzp7Il9hdXRoX3VzZXJfaWQiOiIxIiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoicmVmbG93X3NlcnZlci5hdXRoZW50aWNhdGlvbi5iYWNrZW5kcy5FbWFpbEJhY2tlbmQiLCJfYXV0aF91c2VyX2hhc2giOiI0MTI1OGZiMmE5OTk0MzA5YWI1Nzc2MmY4NDI3ZTU0YzM2NGU1ZTEwIn0=	2020-07-29 03:01:50.085958+00
ryms23l7uygutj80o8th82ilfy6facrw	NjEzMjFhNDY5Yjg2MTZlZGEyZDQ4NGE3MjQ1YTI5MTgwMzRmMzFmMzp7Il9hdXRoX3VzZXJfaWQiOiIxIiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoicmVmbG93X3NlcnZlci5hdXRoZW50aWNhdGlvbi5iYWNrZW5kcy5FbWFpbEJhY2tlbmQiLCJfYXV0aF91c2VyX2hhc2giOiI0MTI1OGZiMmE5OTk0MzA5YWI1Nzc2MmY4NDI3ZTU0YzM2NGU1ZTEwIn0=	2020-07-29 16:44:10.283621+00
hg6o4zo677hh19mtscx73d0cywm7t2qn	NjEzMjFhNDY5Yjg2MTZlZGEyZDQ4NGE3MjQ1YTI5MTgwMzRmMzFmMzp7Il9hdXRoX3VzZXJfaWQiOiIxIiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoicmVmbG93X3NlcnZlci5hdXRoZW50aWNhdGlvbi5iYWNrZW5kcy5FbWFpbEJhY2tlbmQiLCJfYXV0aF91c2VyX2hhc2giOiI0MTI1OGZiMmE5OTk0MzA5YWI1Nzc2MmY4NDI3ZTU0YzM2NGU1ZTEwIn0=	2020-08-06 14:10:29.789678+00
tp510qufep87pct99u8u8g6ebstnqisp	NGQ4MTIzMjQ0YzY0M2UxY2JiZTc1MzdiZDZkMjVhMDJjZjg1MzY5Yjp7Il9hdXRoX3VzZXJfaWQiOiIxIiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoicmVmbG93X2NybS5sb2dpbi5tb2RlbHMuRW1haWxCYWNrZW5kIiwiX2F1dGhfdXNlcl9oYXNoIjoiODIzMDlhYjExYTU3N2UwMmNjNzE3ODA3ZWIzYzAzZjI1ZmYyNmMxNCJ9	2019-11-21 04:49:02.866861+00
e6sxh81c9xlb6w7a1ubi6qwrwl6fvxch	ZGU0ZDRmN2U1NDk5ZTI1YTczMWMwYmFlMmJmM2QwNDRkNjJlOTlhNzp7Il9hdXRoX3VzZXJfaWQiOiIxIiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoicmVmbG93X3NlcnZlci5hdXRoZW50aWNhdGlvbi5iYWNrZW5kcy5FbWFpbEJhY2tlbmQiLCJfYXV0aF91c2VyX2hhc2giOiI2NWEwOTAxNmY4Y2JjMDc2ZjVkN2YyYTBmYWI4YWZiZGFkNTc3MTExIn0=	2020-08-07 21:44:57.514337+00
qp1j5a332rs64ryju31r7zis3v79jr3q	NGQ4MTIzMjQ0YzY0M2UxY2JiZTc1MzdiZDZkMjVhMDJjZjg1MzY5Yjp7Il9hdXRoX3VzZXJfaWQiOiIxIiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoicmVmbG93X2NybS5sb2dpbi5tb2RlbHMuRW1haWxCYWNrZW5kIiwiX2F1dGhfdXNlcl9oYXNoIjoiODIzMDlhYjExYTU3N2UwMmNjNzE3ODA3ZWIzYzAzZjI1ZmYyNmMxNCJ9	2019-11-24 21:16:07.760136+00
k2odwc27vqzvl6oa9xadfgl5twottbh1	ZGU0ZDRmN2U1NDk5ZTI1YTczMWMwYmFlMmJmM2QwNDRkNjJlOTlhNzp7Il9hdXRoX3VzZXJfaWQiOiIxIiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoicmVmbG93X3NlcnZlci5hdXRoZW50aWNhdGlvbi5iYWNrZW5kcy5FbWFpbEJhY2tlbmQiLCJfYXV0aF91c2VyX2hhc2giOiI2NWEwOTAxNmY4Y2JjMDc2ZjVkN2YyYTBmYWI4YWZiZGFkNTc3MTExIn0=	2020-08-16 05:58:36.951982+00
7io3pr31s4vby2fxvluk060kouf925yf	.eJxVjEEOgjAQRe_StSGFSmfi0sRzNNOZTtqIkEDBhfHuSsJCt--__14m0FpzWJc0hyLmYlpz-mWR-J7GfZiTDtMzfOGW5mY30lgLUy3T2Bza0tweVIbrcforZVry3m89g2DkHlEcw1k9eMcWQPqEFm3EKKCeBRmpj51TZSZxXjurgOb9AYvMPJQ:1k9Guj:11CUI2RzsYfFIxYoDe1ZVXoFW9Cbe2PRCKRAw4S00rM	2020-09-04 23:57:41.00177+00
3phhofoqru48iwec0mw92q4flx2g67lq	NGQ4MTIzMjQ0YzY0M2UxY2JiZTc1MzdiZDZkMjVhMDJjZjg1MzY5Yjp7Il9hdXRoX3VzZXJfaWQiOiIxIiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoicmVmbG93X2NybS5sb2dpbi5tb2RlbHMuRW1haWxCYWNrZW5kIiwiX2F1dGhfdXNlcl9oYXNoIjoiODIzMDlhYjExYTU3N2UwMmNjNzE3ODA3ZWIzYzAzZjI1ZmYyNmMxNCJ9	2019-12-05 03:54:27.316741+00
1cwpwpbl2yf8c0aoclhoxk867odhkbvw	.eJxVjEEOgjAQRe_StSGFSmfi0sRzNNOZTtqIkEDBhfHuSsJCt--__14m0FpzWJc0hyLmYlpz-mWR-J7GfZiTDtMzfOGW5mY30lgLUy3T2Bza0tweVIbrcforZVry3m89g2DkHlEcw1k9eMcWQPqEFm3EKKCeBRmpj51TZSZxXjurgOb9AYvMPJQ:1k9IKx:lpeYpmnNRo2_79DAhJRdGgmAjbskMyrbgE3BXK8cGHM	2020-09-05 01:28:51.231526+00
hmgz984vghgc6ygih3atbem3d35ij0rs	.eJxVjEEOgyAQRe_CujHgiAxdNvEcZIAhkFpNRNtF07tXExft9v3331s42tbstsqLK1FchRKXX-Yp3Hk6hoXTOL_cDp-8NIfB01oCrWWemlOrzfCgMt7O018pU817JibVIoGR3vQge98lZVvlg4kdIURmr4LFNqAGVgYYvUwcIkrSSVvoxecLhTU8HA:1lkUC8:Cwl7_ttaEEZPYR-Di70cbnFIuiQUDjrwQS9etaQVIf8	2021-06-05 16:09:44.682185+00
w38u6w6666hhyhaaos54d4hsfih0co6h	.eJxVjEEOgyAQRe_CujHgiAxdNvEcZIAhkFpNRNtF07tXExft9v3331s42tbstsqLK1FchRKXX-Yp3Hk6hoXTOL_cDp-8NIfB01oCrWWemlOrzfCgMt7O018pU817JibVIoGR3vQge98lZVvlg4kdIURmr4LFNqAGVgYYvUwcIkrSSVvoxecLhTU8HA:1lkUDv:wg7xHyNWTZH2leR-P6MLizIYA3uyrUsJ38XXPAp20aI	2021-06-05 16:11:35.637786+00
dws5eds8sk1yaq2ymphxuxhnr3keb8cp	.eJxVjEEOgyAQRe_CujHgiAxdNvEcZIAhkFpNRNtF07tXExft9v3331s42tbstsqLK1FchRKXX-Yp3Hk6hoXTOL_cDp-8NIfB01oCrWWemlOrzfCgMt7O018pU817JibVIoGR3vQge98lZVvlg4kdIURmr4LFNqAGVgYYvUwcIkrSSVvoxecLhTU8HA:1lkUEs:Di9XGMrdzukfusjBuMeDdjIUXBAgmWIPlSf0JnJI4Ik	2021-06-05 16:12:34.548599+00
u5cwz4ga6bwm136k3s9r2rqynnl2y4hn	.eJxVjEEOgyAQRe_CujHgiAxdNvEcZIAhkFpNRNtF07tXExft9v3331s42tbstsqLK1FchRKXX-Yp3Hk6hoXTOL_cDp-8NIfB01oCrWWemlOrzfCgMt7O018pU817JibVIoGR3vQge98lZVvlg4kdIURmr4LFNqAGVgYYvUwcIkrSSVvoxecLhTU8HA:1lmGvQ:H8ehiF6hcjk6gvm3PS4KTR-nfJ1BG8SbBFolaarzH-w	2021-06-10 14:23:52.668415+00
firme6mtcbnb7hp2g2t0onh6i679v9en	.eJxVjEEOgyAQRe_CujHgiAxdNvEcZIAhkFpNRNtF07tXExft9v3331s42tbstsqLK1FchRKXX-Yp3Hk6hoXTOL_cDp-8NIfB01oCrWWemlOrzfCgMt7O018pU817JibVIoGR3vQge98lZVvlg4kdIURmr4LFNqAGVgYYvUwcIkrSSVvoxecLhTU8HA:1lmeX9:bGCuiUi58sMfbU1bFKERoTrVydj8RVXVxz8ktNATtZI	2021-06-11 15:36:23.249528+00
b02tz8135uamvdiqwzjy1b1jqr7izhe2	.eJxVjEEOgyAQRe_CujHgiAxdNvEcZIAhkFpNRNtF07tXExft9v3331s42tbstsqLK1FchRKXX-Yp3Hk6hoXTOL_cDp-8NIfB01oCrWWemlOrzfCgMt7O018pU817JibVIoGR3vQge98lZVvlg4kdIURmr4LFNqAGVgYYvUwcIkrSSVvoxecLhTU8HA:1lnjVT:iPshb-r-psh9TCMl8TClKrELR5gxGrezafcHsJ06uMg	2021-06-14 15:07:07.323607+00
e0pvohtdp5763bts9csrrltxogt0btt5	.eJxVjEEOgyAQRe_CujHgiAxdNvEcZIAhkFpNRNtF07tXExft9v3331s42tbstsqLK1FchRKXX-Yp3Hk6hoXTOL_cDp-8NIfB01oCrWWemlOrzfCgMt7O018pU817JibVIoGR3vQge98lZVvlg4kdIURmr4LFNqAGVgYYvUwcIkrSSVvoxecLhTU8HA:1lqJUY:b7Cv_SpibZtkeIwOooG2HrW_fajWVWyHYzQCqYOAsQg	2021-06-21 17:56:50.046011+00
\.


--
-- Data for Name: draft; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.draft (id, created_at, updated_at, bucket, file_draft_path, file_url, file_size, value, company_id, draft_type_id, user_id, is_public) FROM stdin;
\.


--
-- Data for Name: draft_type; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.draft_type (id, name, "order") FROM stdin;
1	file	1
2	value	2
\.


--
-- Data for Name: dynamic_forms; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.dynamic_forms (id, created_at, updated_at, company_id, depends_on_id, form_id, user_id, uuid) FROM stdin;
2105	2021-05-26 22:29:00.510253+00	2021-05-27 21:43:57.178978+00	1	\N	332	1	00000000-0000-0000-0000-000000000835
2109	2021-05-27 14:24:58.807438+00	2021-05-27 21:43:57.182742+00	1	2105	334	1	9e853e6a-1315-4bbf-a3db-33f9e4b9d3f0
2106	2021-05-26 22:29:00.537947+00	2021-05-27 21:43:57.185823+00	1	2105	333	1	b1e89bfa-88a2-41e8-9ea0-c8fbda1f0bd8
2103	2021-05-22 20:00:58.346066+00	2021-05-26 17:05:48.191267+00	1	\N	332	1	7ed8d817-c3a4-404f-9423-e590d91b4fde
2104	2021-05-22 20:00:58.353189+00	2021-05-26 17:05:48.19609+00	1	2103	333	1	5533328c-e5a2-4501-aaa4-825721754def
2107	2021-05-26 22:29:39.139874+00	2021-05-26 22:29:39.139915+00	1	\N	332	1	00000000-0000-0000-0000-000000000835
2108	2021-05-26 22:29:39.143736+00	2021-05-26 22:29:39.143772+00	1	2107	333	1	b1e89bfa-88a2-41e8-9ea0-c8fbda1f0bd8
2101	2021-05-22 19:58:13.546297+00	2021-05-26 22:31:33.399543+00	1	\N	332	1	692ea4cb-7f0b-420c-aa1c-326b655bbcee
2102	2021-05-22 19:58:13.55194+00	2021-05-26 22:31:33.40359+00	1	2101	333	1	b1e89bfa-88a2-41e8-9ea0-c8fbda1f0bd8
\.


--
-- Data for Name: extract_file_data; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.extract_file_data (id, created_at, updated_at, file_id, file, file_format, company_id, form_id, user_id) FROM stdin;
\.


--
-- Data for Name: field; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.field (id, number_configuration_mask, formula_configuration, created_at, updated_at, name, label_name, placeholder, required, "order", is_unique, field_is_hidden, label_is_hidden, date_configuration_auto_create, date_configuration_auto_update, number_configuration_allow_negative, number_configuration_allow_zero, enabled, date_configuration_date_format_type_id, form_id, form_field_as_option_id, number_configuration_number_format_type_id, period_configuration_period_interval_type_id, type_id, uuid, is_long_text_rich_text) FROM stdin;
756	\N	\N	2021-05-22 16:12:47.950406+00	2021-06-08 14:56:14.325521+00	nomedoevento	Nome do Evento	\N	f	1	f	f	f	f	f	t	t	t	\N	333	\N	\N	\N	2	2185956d-895d-4ade-8e90-75d77faaa358	f
757	\N	\N	2021-05-22 19:56:49.128969+00	2021-06-08 14:56:14.327475+00	tipodoevento	Tipo do Evento		f	2	f	f	f	f	f	t	t	t	1	333	\N	1	4	4	ff0d0990-4d52-4de6-8361-57a0e41c4340	f
758	\N	\N	2021-05-22 19:57:11.656485+00	2021-06-08 14:56:14.328948+00	datadoevento	Data do Evento		f	3	f	f	f	f	f	t	t	t	1	333	\N	1	4	3	7287c37f-b341-46e4-b5e9-89007ab0a271	f
759	\N	\N	2021-05-22 19:57:26.599188+00	2021-06-08 14:56:14.330255+00	expectativadevalor	Expectativa de valor		f	4	f	f	f	f	f	t	t	t	1	333	\N	1	4	1	9ccd15b7-3098-4b35-bb8a-5ea2a518faa9	f
763	\N	\N	2021-05-27 14:31:18.020511+00	2021-06-08 14:56:14.331578+00	porcentagem	Porcentagem		f	6	f	f	f	f	f	t	t	t	1	333	\N	3	4	1	00060280-d80e-489c-891e-69591a6033b0	f
764	\N	\N	2021-05-31 15:43:22.558163+00	2021-06-08 14:56:14.333018+00	formula	Formula		f	7	f	f	f	f	f	t	t	t	1	333	\N	1	4	15	f7b0c74e-c22f-42a3-a1ca-7fea63ee6464	f
760	\N	763 / 10\nasdasd\n\n\tasdasdasd\nasdasd\n{{}}\n{{nomedoevento}}	2021-05-25 22:14:45.694565+00	2021-06-08 14:56:14.334723+00	calculo1	Calculo1		f	5	f	f	f	f	f	t	t	t	1	333	\N	2	4	15	0d9c8194-0a80-4780-a351-646ce85f94ef	f
761	\N	\N	2021-05-26 22:32:25.96631+00	2021-05-26 22:32:25.966348+00	nomedaempresa	Nome da Empresa		f	1	f	f	f	f	f	t	t	t	1	334	\N	1	4	2	57736f42-12e9-450d-85b3-fa1f09a5eedf	f
\.


--
-- Data for Name: field_date_format_type; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.field_date_format_type (id, type, label_name, format, "order") FROM stdin;
1	date	Data	%d/%m/%Y	1
2	datetime	Data e Hora	%d/%m/%Y %H:%M	2
\.


--
-- Data for Name: field_number_format_type; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.field_number_format_type (id, type, label_name, "precision", prefix, suffix, thousand_separator, decimal_separator, "order", base, has_to_enforce_decimal) FROM stdin;
1	number	Numero	100000000	\N	\N	\N	,	1	1	f
4	integer	Inteiro	1	\N	\N	\N	\N	2	1	f
2	currency	Moeda	100	\N	\N	.	,	3	1	t
3	percentage	Porcentagem	100	\N	 %	\N	,	4	100	t
\.


--
-- Data for Name: field_options; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.field_options (id, created_at, updated_at, option, "order", field_id, uuid) FROM stdin;
2227	2021-05-22 19:56:49.142048+00	2021-05-26 22:33:59.36351+00	Festa de Casamento	0	757	aa99a7eb-475a-448a-8607-0e0e4753889f
2228	2021-05-22 19:56:58.85194+00	2021-05-26 22:33:59.369528+00	Festa de aniversário	1	757	bcdde8d9-186c-471d-99c9-e2c5a4ba71b8
2229	2021-05-22 19:56:58.855964+00	2021-05-26 22:33:59.375657+00	Formaturas	2	757	778b7a00-01f6-4920-98f7-a42e5d17d9f6
2230	2021-05-22 19:57:01.977769+00	2021-05-26 22:33:59.382765+00	Comerciais	3	757	7391aeb7-0a7c-49b4-86de-8ae35941b920
\.


--
-- Data for Name: field_period_interval_type; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.field_period_interval_type (id, type, label_name, in_seconds, "order") FROM stdin;
1	seconds	Segundos	1	1
2	minutes	Minutos	60	1
3	hours	Horas	360	1
4	days	Dias	8640	1
5	weeks	Semanas	60480	1
6	month	Meses	259200	1
\.


--
-- Data for Name: field_type; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.field_type (id, type, label_name, "order", is_dynamic_evaluated) FROM stdin;
2	text	Texto	1	f
1	number	Número	2	f
7	long_text	Texto Longo	7	f
6	attachment	Anexo	6	f
14	period	Período	12	f
11	multi_option	Multiplas Opções	9	f
4	option	Opção	4	f
13	user	Usuários	11	f
3	date	Data	3	f
10	email	E-mail	8	f
5	form	Conexão com Formulário	5	f
12	id	ID	10	f
15	formula	Formula	13	f
\.


--
-- Data for Name: form; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.form (id, created_at, updated_at, form_name, label_name, "order", conditional_value, enabled, company_id, conditional_on_field_id, conditional_type_id, depends_on_id, group_id, type_id, uuid, conditional_excludes_data_if_not_set, show_label_name) FROM stdin;
332	2021-05-22 16:12:47.879549+00	2021-05-22 19:55:32.764471+00	eventos	Eventos	0	\N	t	1	\N	\N	\N	35	1	de82529d-bda2-434e-b5a8-56f36e37dba7	t	t
333	2021-05-22 16:12:47.917369+00	2021-05-26 22:32:18.760912+00	informacoesdoevento	Informações do Evento	1	\N	t	1	\N	\N	332	\N	1	783e079f-2c46-41ae-8c41-3dd729e1fcdc	t	f
334	2021-05-26 22:32:18.783441+00	2021-05-26 22:32:18.78349+00	festacomercial	Festa comercial	2	Comerciais	t	1	757	1	332	\N	1	d2efc2b0-d7e1-4cdf-87f1-5e25e9a4fd51	t	t
\.


--
-- Data for Name: form_accessed_by; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.form_accessed_by (id, created_at, updated_at, form_id, user_id) FROM stdin;
259	2021-05-22 16:12:47.88226+00	2021-05-22 16:12:47.882281+00	332	1
\.


--
-- Data for Name: form_type; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.form_type (id, type, label_name, "order") FROM stdin;
1	form	Único	1
2	multi-form	Múltiplo	1
\.


--
-- Data for Name: form_value; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.form_value (id, number_configuration_mask, formula_configuration, created_at, updated_at, value, company_id, date_configuration_date_format_type_id, field_id, field_type_id, form_id, form_field_as_option_id, number_configuration_number_format_type_id, period_configuration_period_interval_type_id, is_long_text_rich_text) FROM stdin;
6199	\N	\N	2021-05-26 22:29:00.556315+00	2021-05-27 21:43:57.20164+00	Festa de casamento do nicolas	1	\N	756	2	2106	\N	\N	\N	f
6200	\N	\N	2021-05-26 22:29:00.5909+00	2021-05-27 21:43:57.228355+00	Comerciais	1	1	757	4	2106	\N	1	4	f
6201	\N	\N	2021-05-26 22:29:00.613342+00	2021-05-27 21:43:57.248992+00	2021-05-28 00:00:00	1	1	758	3	2106	\N	1	4	f
6202	\N	\N	2021-05-26 22:29:00.640169+00	2021-05-27 21:43:57.26903+00	0	1	1	759	1	2106	\N	1	4	f
6212	\N	\N	2021-05-27 14:36:04.237999+00	2021-05-27 21:43:57.303823+00	200000000	1	1	763	1	2106	\N	3	4	f
6203	\N	{{763}} / 10	2021-05-26 22:29:00.662264+00	2021-05-27 21:43:58.859409+00	20000000	1	1	760	1	2106	\N	2	4	f
6192	\N	\N	2021-05-22 19:58:13.622745+00	2021-05-26 22:31:33.471158+00	1234123000000	1	1	759	1	2102	\N	1	4	f
6193	\N	\N	2021-05-22 20:00:58.367487+00	2021-05-26 17:05:48.208794+00	Festa de Formatura EACH USP	1	\N	756	2	2104	\N	\N	\N	f
6194	\N	\N	2021-05-22 20:00:58.385223+00	2021-05-26 17:05:48.224839+00	Formaturas	1	1	757	4	2104	\N	1	4	f
6195	\N	\N	2021-05-22 20:00:58.401543+00	2021-05-26 17:05:48.240999+00	2021-05-29 00:00:00	1	1	758	3	2104	\N	1	4	f
6196	\N	\N	2021-05-22 20:00:58.418182+00	2021-05-26 17:05:48.256721+00	200000000	1	1	759	1	2104	\N	1	4	f
6198	\N	1 + {{759}}	2021-05-25 22:16:00.454064+00	2021-05-26 17:05:49.305557+00	300000000	1	1	760	1	2104	\N	2	4	f
6204	\N	\N	2021-05-26 22:29:39.15739+00	2021-05-26 22:29:39.157431+00	Festa de casamento do nicolas	1	\N	756	2	2108	\N	\N	\N	f
6205	\N	\N	2021-05-26 22:29:39.176341+00	2021-05-26 22:29:39.176381+00	Festa de aniversário	1	1	757	4	2108	\N	1	4	f
6206	\N	\N	2021-05-26 22:29:39.193336+00	2021-05-26 22:29:39.193376+00	2021-05-28 00:00:00	1	1	758	3	2108	\N	1	4	f
6207	\N	\N	2021-05-26 22:29:39.210158+00	2021-05-26 22:29:39.210194+00	123412300000000	1	1	759	1	2108	\N	1	4	f
6208	\N	1 + {{759}}	2021-05-26 22:29:39.227408+00	2021-05-26 22:29:40.189235+00	123412400000000	1	1	760	1	2108	\N	2	4	f
6189	\N	\N	2021-05-22 19:58:13.572772+00	2021-05-26 22:31:33.414385+00	Festa de casamento do nicolas	1	\N	756	2	2102	\N	\N	\N	f
6190	\N	\N	2021-05-22 19:58:13.590182+00	2021-05-26 22:31:33.434593+00	Festa de aniversário	1	1	757	4	2102	\N	1	4	f
6191	\N	\N	2021-05-22 19:58:13.606557+00	2021-05-26 22:31:33.449521+00	2021-05-28 00:00:00	1	1	758	3	2102	\N	1	4	f
6209	\N	1 + {{759}}	2021-05-26 22:31:33.489542+00	2021-05-26 22:31:34.8743+00	123412400000000	1	1	760	1	2102	\N	2	4	f
\.


--
-- Data for Name: formula_attribute_type; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.formula_attribute_type (id, name, "order") FROM stdin;
1	conjunction	1
2	disjunction	2
3	inversion	3
4	block_do	4
5	block_end	5
6	null	6
7	boolean_true	7
8	boolean_false	8
9	if_if	9
10	if_else	10
11	function	11
12	decimal_point_separator	12
13	positional_argument_separator	13
\.


--
-- Data for Name: formula_context_attribute_type; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.formula_context_attribute_type (id, translation, attribute_type_id, context_type_id) FROM stdin;
1	and	1	1
2	or	2	1
3	not	3	1
4	do	4	1
5	end	5	1
6	None	6	1
7	True	7	1
8	False	8	1
9	if	9	1
10	else	10	1
11	function	11	1
12	.	12	1
13	,	13	1
14	e	1	2
15	ou	2	2
16	nao	3	2
17	faz	4	2
18	fim	5	2
19	Vazio	6	2
20	Verdadeiro	7	2
21	Falso	8	2
22	se	9	2
23	senao	10	2
24	funcao	11	2
25	,	12	2
26	;	13	2
\.


--
-- Data for Name: formula_context_for_company; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.formula_context_for_company (id, company_id, context_type_id) FROM stdin;
1	1	1
\.


--
-- Data for Name: formula_context_type; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.formula_context_type (id, language, name, "order") FROM stdin;
2	portugues	portugues	2
1	english	english	1
\.


--
-- Data for Name: formula_parameters_type; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.formula_parameters_type (id, name, formula_type_id, raw_data_type_id, is_list) FROM stdin;
\.


--
-- Data for Name: formula_variable; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.formula_variable (id, "order", field_id, variable_id) FROM stdin;
18	0	760	756
20	1	760	756
\.


--
-- Data for Name: group; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public."group" (id, name, enabled, "order", company_id) FROM stdin;
2	Novo Grupo	t	1	3
35	Gestão de Eventos	t	5	1
\.


--
-- Data for Name: individual_charge_value_type; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.individual_charge_value_type (id, name, value, default_quantity, charge_frequency_type_id, charge_type_id, "order", charge_group_name) FROM stdin;
1	per_gb	1.00	5	1	2	2	per_gb
2	per_user	40.00	1	1	2	1	per_user
3	per_chart_user	1.00	2	1	1	3	per_chart
4	per_chart_company	1.00	2	1	1	4	per_chart
5	per_pdf_download	1.00	30	1	2	5	per_pdf_download
\.


--
-- Data for Name: invoice_date_type; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.invoice_date_type (id, date, "order") FROM stdin;
1	4	1
2	1	0
3	15	2
4	25	3
\.


--
-- Data for Name: kanban_card; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.kanban_card (id, created_at, updated_at, "default", user_id, company_id, form_id) FROM stdin;
124	2021-05-26 22:26:25.784764+00	2021-05-26 22:26:25.784809+00	f	1	\N	\N
\.


--
-- Data for Name: kanban_card_field; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.kanban_card_field (id, created_at, updated_at, field_id, kanban_card_id, "order") FROM stdin;
757	2021-05-26 22:26:25.788241+00	2021-05-26 22:26:25.788277+00	756	124	0
758	2021-05-26 22:26:25.790831+00	2021-05-26 22:26:25.790865+00	757	124	1
759	2021-05-26 22:26:25.791542+00	2021-05-26 22:26:25.791645+00	758	124	2
\.


--
-- Data for Name: kanban_collapsed_option; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.kanban_collapsed_option (id, company_id, field_option_id, user_id) FROM stdin;
\.


--
-- Data for Name: kanban_default; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.kanban_default (id, company_id, form_id, kanban_card_id, kanban_dimension_id, user_id) FROM stdin;
7	1	332	124	757	1
\.


--
-- Data for Name: kanban_dimension_order; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.kanban_dimension_order (id, created_at, updated_at, options, "order", "default", dimension_id, user_id) FROM stdin;
\.


--
-- Data for Name: listing_selected_fields; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.listing_selected_fields (id, field_id, user_id, is_selected) FROM stdin;
844	118	15	t
845	119	15	t
846	120	15	t
847	121	15	t
848	122	15	t
856	102	9	t
857	101	9	t
858	103	9	t
859	104	9	t
860	107	9	t
861	118	9	t
862	119	9	t
863	120	9	t
864	121	9	t
865	122	9	t
803	102	15	t
804	101	15	t
805	103	15	t
806	104	15	t
807	107	15	t
1065	93	9	t
1066	94	9	t
1067	95	9	t
1068	105	9	t
1069	96	9	t
1070	100	9	t
1071	98	9	t
1072	99	9	t
767	93	15	t
768	94	15	t
769	95	15	t
770	105	15	t
771	96	15	t
772	98	15	t
2258	678	1	t
2259	692	1	t
2260	683	1	t
2261	687	1	t
2262	688	1	t
2263	704	1	t
2269	690	1	t
2270	691	1	t
2271	694	1	t
2272	679	1	t
2273	684	1	t
2274	693	1	t
2275	689	1	t
2276	703	1	t
2277	680	1	t
2278	685	1	t
2279	681	1	t
2280	695	1	t
2283	682	1	t
2284	698	1	t
2285	699	1	t
2286	700	1	t
2287	701	1	t
2288	702	1	t
2289	718	1	t
2297	719	1	t
2298	720	1	t
2299	721	1	t
2300	722	1	t
2301	723	1	t
2302	724	1	t
2303	725	1	t
2304	726	1	t
2305	727	1	t
2306	728	1	t
2307	729	1	t
2308	730	1	t
2309	731	1	t
2310	746	1	t
2311	747	1	t
2312	748	1	t
2313	745	1	t
2314	749	1	t
2315	750	1	t
2316	751	1	t
2317	753	1	t
2318	752	1	t
2319	755	1	t
2320	756	1	t
2321	757	1	t
2322	758	1	t
2323	759	1	t
2324	760	1	t
2325	761	1	t
2326	763	1	t
2327	764	1	t
\.


--
-- Data for Name: notification; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.notification (id, created_at, updated_at, notification, form_id, notification_configuration_id, user_id) FROM stdin;
\.


--
-- Data for Name: notification_configuration; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.notification_configuration (id, created_at, updated_at, for_company, name, text, days_diff, field_id, form_id, user_id) FROM stdin;
32	2021-02-01 20:34:07.586386+00	2021-02-01 20:34:07.586416+00	t	Lembrete de Vencimentos	A fatura do/a {{cliente_2}} irá vencer no dia {{vencimentodafatura}}!	-3	741	323	1
33	2021-03-19 17:58:45.779788+00	2021-03-19 17:58:45.779816+00	t	SLA de Negociação	A conta do cliente {{}} está parada em negociação a mais de 10 dias!	11	752	308	1
\.


--
-- Data for Name: notification_configuration_variable; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.notification_configuration_variable (id, field_id, notification_configuration_id, "order") FROM stdin;
31	733	32	1
32	741	32	2
33	679	33	1
\.


--
-- Data for Name: option_accessed_by; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.option_accessed_by (id, created_at, updated_at, field_option_id, user_id) FROM stdin;
9217	2021-05-22 19:56:49.146471+00	2021-05-22 19:56:49.146534+00	2227	20
9218	2021-05-22 19:56:49.146567+00	2021-05-22 19:56:49.146577+00	2227	25
9219	2021-05-22 19:56:49.146597+00	2021-05-22 19:56:49.146607+00	2227	27
9220	2021-05-22 19:56:49.146626+00	2021-05-22 19:56:49.146635+00	2227	1
9221	2021-05-22 19:56:58.859064+00	2021-05-22 19:56:58.859083+00	2228	20
9222	2021-05-22 19:56:58.85911+00	2021-05-22 19:56:58.85912+00	2228	25
9223	2021-05-22 19:56:58.85914+00	2021-05-22 19:56:58.859149+00	2228	27
9224	2021-05-22 19:56:58.859169+00	2021-05-22 19:56:58.859182+00	2228	1
9225	2021-05-22 19:56:58.859201+00	2021-05-22 19:56:58.859211+00	2229	20
9226	2021-05-22 19:56:58.85923+00	2021-05-22 19:56:58.859239+00	2229	25
9227	2021-05-22 19:56:58.859258+00	2021-05-22 19:56:58.859268+00	2229	27
9228	2021-05-22 19:56:58.859287+00	2021-05-22 19:56:58.859296+00	2229	1
9229	2021-05-22 19:57:01.985263+00	2021-05-22 19:57:01.985297+00	2230	20
9230	2021-05-22 19:57:01.985333+00	2021-05-22 19:57:01.985344+00	2230	25
9231	2021-05-22 19:57:01.985365+00	2021-05-22 19:57:01.985374+00	2230	27
9232	2021-05-22 19:57:01.985394+00	2021-05-22 19:57:01.985404+00	2230	1
\.


--
-- Data for Name: partner_default_and_discounts; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.partner_default_and_discounts (id, partner_name, discount_value, default_quantity, individual_charge_value_type_id) FROM stdin;
\.


--
-- Data for Name: payment_method_type; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.payment_method_type (id, name, "order") FROM stdin;
1	credit_card	1
2	invoice	1
\.


--
-- Data for Name: pdf_generated; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.pdf_generated (id, created_at, updated_at, company_id, pdf_template_id, user_id) FROM stdin;
1	2020-12-13 15:07:36.613547+00	2020-12-13 15:07:36.613573+00	1	3	1
2	2020-12-13 15:35:34.378277+00	2020-12-13 15:35:34.378302+00	1	3	1
3	2020-12-13 15:37:04.755576+00	2020-12-13 15:37:04.755601+00	1	3	1
4	2020-12-13 20:39:06.54975+00	2020-12-13 20:39:06.549778+00	1	3	1
5	2020-12-13 20:40:48.857908+00	2020-12-13 20:40:48.857935+00	1	3	1
6	2020-12-13 20:41:36.985166+00	2020-12-13 20:41:36.985193+00	1	3	1
7	2020-12-13 20:42:30.729496+00	2020-12-13 20:42:30.729522+00	1	3	1
8	2020-12-13 20:43:52.360973+00	2020-12-13 20:43:52.361+00	1	3	1
9	2020-12-13 20:56:29.847087+00	2020-12-13 20:56:29.847114+00	1	3	1
10	2020-12-14 06:42:04.035275+00	2020-12-14 06:42:04.035303+00	1	3	1
11	2020-12-14 07:09:26.372302+00	2020-12-14 07:09:26.37233+00	1	3	1
12	2020-12-14 07:11:33.40107+00	2020-12-14 07:11:33.401097+00	1	3	1
13	2020-12-14 14:11:24.480893+00	2020-12-14 14:11:24.480919+00	1	3	1
14	2020-12-14 14:12:57.182554+00	2020-12-14 14:12:57.18258+00	1	3	1
15	2020-12-14 14:13:59.274215+00	2020-12-14 14:13:59.274242+00	1	3	1
16	2020-12-14 14:14:06.292675+00	2020-12-14 14:14:06.292701+00	1	3	1
17	2020-12-14 14:16:28.94105+00	2020-12-14 14:16:28.941087+00	1	3	1
18	2020-12-14 14:22:59.866583+00	2020-12-14 14:22:59.866609+00	1	3	1
19	2020-12-14 14:24:21.18006+00	2020-12-14 14:24:21.180088+00	1	3	1
20	2020-12-14 14:27:39.71636+00	2020-12-14 14:27:39.716387+00	1	3	1
21	2020-12-14 14:30:22.13148+00	2020-12-14 14:30:22.131508+00	1	3	1
22	2020-12-14 14:31:16.83926+00	2020-12-14 14:31:16.839287+00	1	3	1
23	2020-12-14 14:32:47.467249+00	2020-12-14 14:32:47.467276+00	1	3	1
24	2020-12-14 14:33:41.221111+00	2020-12-14 14:33:41.221139+00	1	3	1
25	2020-12-14 14:46:17.413245+00	2020-12-14 14:46:17.41327+00	1	3	1
26	2020-12-14 15:29:59.496842+00	2020-12-14 15:29:59.496868+00	1	3	1
27	2020-12-14 15:31:00.625608+00	2020-12-14 15:31:00.625635+00	1	3	1
28	2020-12-14 15:31:07.523786+00	2020-12-14 15:31:07.523814+00	1	3	1
29	2020-12-19 16:16:34.710499+00	2020-12-19 16:16:34.710527+00	1	3	1
30	2021-01-01 00:30:12.313139+00	2021-01-01 00:30:12.313166+00	1	3	1
31	2021-01-01 00:30:22.090794+00	2021-01-01 00:30:22.09082+00	1	3	1
32	2021-01-01 00:48:56.29828+00	2021-01-01 00:48:56.298307+00	1	3	1
33	2021-01-01 00:49:46.956159+00	2021-01-01 00:49:46.956185+00	1	3	1
34	2021-01-01 01:22:06.428062+00	2021-01-01 01:22:06.428088+00	1	3	1
35	2021-01-01 01:29:16.990336+00	2021-01-01 01:29:16.990361+00	1	3	1
36	2021-01-01 01:29:51.748458+00	2021-01-01 01:29:51.748484+00	1	3	1
37	2021-01-28 14:36:11.262733+00	2021-01-28 14:36:11.262762+00	1	3	1
38	2021-01-28 14:40:50.341738+00	2021-01-28 14:40:50.341768+00	1	3	1
39	2021-01-28 14:44:42.232971+00	2021-01-28 14:44:42.233002+00	1	3	1
40	2021-01-28 14:45:48.961496+00	2021-01-28 14:45:48.961528+00	1	3	1
41	2021-01-28 14:45:56.267375+00	2021-01-28 14:45:56.267405+00	1	3	1
42	2021-01-28 14:46:24.284193+00	2021-01-28 14:46:24.284223+00	1	3	1
43	2021-01-28 14:58:08.253541+00	2021-01-28 14:58:08.253573+00	1	3	1
44	2021-01-28 15:06:36.454492+00	2021-01-28 15:06:36.454525+00	1	3	1
45	2021-01-28 15:32:20.276153+00	2021-01-28 15:32:20.276183+00	1	3	1
46	2021-01-28 15:34:17.688954+00	2021-01-28 15:34:17.688985+00	1	3	1
47	2021-01-28 15:36:20.146679+00	2021-01-28 15:36:20.146709+00	1	3	1
48	2021-01-28 15:37:35.067889+00	2021-01-28 15:37:35.06792+00	1	3	1
49	2021-01-28 15:39:42.553711+00	2021-01-28 15:39:42.553745+00	1	3	1
50	2021-01-28 17:33:51.17795+00	2021-01-28 17:33:51.177982+00	1	3	1
51	2021-01-28 18:38:47.317295+00	2021-01-28 18:38:47.317326+00	1	3	1
52	2021-01-28 18:46:21.360483+00	2021-01-28 18:46:21.360513+00	1	3	1
53	2021-01-28 19:20:07.159354+00	2021-01-28 19:20:07.159385+00	1	3	1
54	2021-01-28 19:20:28.931821+00	2021-01-28 19:20:28.931852+00	1	3	1
55	2021-01-28 19:32:27.619774+00	2021-01-28 19:32:27.619805+00	1	3	1
56	2021-01-28 19:34:20.485082+00	2021-01-28 19:34:20.485114+00	1	3	1
57	2021-01-28 19:34:29.811753+00	2021-01-28 19:34:29.811784+00	1	3	1
58	2021-01-28 19:35:44.628415+00	2021-01-28 19:35:44.628446+00	1	3	1
59	2021-01-28 19:36:12.178967+00	2021-01-28 19:36:12.178999+00	1	3	1
60	2021-01-28 19:50:20.073452+00	2021-01-28 19:50:20.075774+00	1	3	1
61	2021-01-28 19:53:24.288793+00	2021-01-28 19:53:24.288824+00	1	3	1
62	2021-01-28 21:59:21.046434+00	2021-01-28 21:59:21.046466+00	1	3	1
63	2021-01-28 22:16:41.623731+00	2021-01-28 22:16:41.623761+00	1	3	1
64	2021-01-29 13:21:03.944538+00	2021-01-29 13:21:03.944567+00	1	3	1
65	2021-01-31 19:38:24.735729+00	2021-01-31 19:38:24.735759+00	1	7	1
66	2021-02-01 20:23:23.994603+00	2021-02-01 20:23:23.994632+00	1	3	1
67	2021-02-01 20:30:48.501819+00	2021-02-01 20:30:48.501846+00	1	3	1
\.


--
-- Data for Name: pdf_template_allowed_text_block; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.pdf_template_allowed_text_block (id, block_id) FROM stdin;
1	1
2	2
3	4
\.


--
-- Data for Name: pdf_template_configuration; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.pdf_template_configuration (id, created_at, updated_at, name, company_id, form_id, user_id, rich_text_page_id) FROM stdin;
7	2021-01-29 18:22:44.736386+00	2021-01-31 19:34:54.739026+00	Proposta Comercial - 3 Planos	1	308	1	7
3	2020-12-12 18:01:58.011683+00	2021-01-29 18:20:01.975469+00	Proposta Comercial - 2 Planos	1	308	1	3
\.


--
-- Data for Name: pdf_template_configuration_variables; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.pdf_template_configuration_variables (id, field_id, pdf_template_id) FROM stdin;
96	691	3
97	694	3
98	693	3
109	703	3
110	699	3
111	698	3
112	700	3
113	701	3
114	679	3
115	702	3
117	718	3
118	678	3
124	695	3
125	722	3
126	723	3
127	724	3
128	725	3
129	726	3
130	722	3
131	723	3
132	724	3
133	724	3
134	679	7
135	692	7
136	691	7
137	694	7
138	718	7
139	693	7
140	695	7
141	722	7
142	723	7
143	724	7
144	725	7
145	726	7
146	727	7
147	703	7
148	699	7
149	698	7
150	700	7
151	701	7
152	702	7
\.


--
-- Data for Name: pre_notification; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.pre_notification (id, "when", notification_configuration_id, user_id, dynamic_form_id, has_sent, is_sending) FROM stdin;
\.


--
-- Data for Name: profiles; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.profiles (id, name, label_name, can_edit, "order") FROM stdin;
2	coordinator	Coordenador	t	1
3	admin	Admin	t	1
4	simple_user	Analista	t	1
1	Technician	\N	f	1
\.


--
-- Data for Name: public_access; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.public_access (id, public_key, company_id, user_id) FROM stdin;
\.


--
-- Data for Name: public_access_field; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.public_access_field (id, field_id, public_access_id, public_form_id) FROM stdin;
\.


--
-- Data for Name: public_access_form; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.public_access_form (id, form_id, public_access_id, description_message, greetings_message, is_to_submit_another_response_button) FROM stdin;
\.


--
-- Data for Name: push_notification; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.push_notification (id, token, endpoint, push_notification_tag_type_id, user_id) FROM stdin;
5	{"endpoint":"https://updates.push.services.mozilla.com/wpush/v2/gAAAAABexem06U6OKAPzQrGkDA-cbcd3Esit4nPK9-PfFl8a8MdHuRxnB0myxZPgLOh0DDXFKbDMokAZZvYh17VZu9w8MGZ896cIZaZRBHU8FqIOiDRZx7lG2NXN-DL8Pa01XHG-kJBy2q3mJ8QqeNI9HYuH70R2V9Lr9uP-Fl3Da5K6gt9DwJI","keys":{"auth":"vkhWW8DWrbihj_dU1IEdZg","p256dh":"BLqoAXD5ebOAkeTzgs4u0ACO3uivSWfyLDVUwE33Q93AXtHPCtZzh7zghRXLP7YyjBDBHi0WTzJMtapxzhJJGL4"}}	https://updates.push.services.mozilla.com/wpush/v2/gAAAAABexem06U6OKAPzQrGkDA-cbcd3Esit4nPK9-PfFl8a8MdHuRxnB0myxZPgLOh0DDXFKbDMokAZZvYh17VZu9w8MGZ896cIZaZRBHU8FqIOiDRZx7lG2NXN-DL8Pa01XHG-kJBy2q3mJ8QqeNI9HYuH70R2V9Lr9uP-Fl3Da5K6gt9DwJI	1	1
6	{"endpoint":"https://updates.push.services.mozilla.com/wpush/v2/gAAAAABfMjha-cWAJDHM6ESUvgwRssoevr29yxuAtfWAg6NLNd4Ee6xB_KgMvmnyPs6CRyMziL_DltVhueRV0w2_dFDVo9E0lAefpZlgXr2okmmCNbgKobfIZ0Vz25bNwJ-m5nDz3XUCtpkWmKiZDWXkWaeo_Elct1VNlPjWSyUYeffEprD7A4E","keys":{"auth":"dBLUZohZdNKnKPs-Y_3iVw","p256dh":"BC8myDDQ8sWSBo7KpPsXTImv4ZVbsgF5g7NrlRrzvpxjOU0Nkp8r2t2CB208a40LGBWBMNOgZ01NPmwX-9zbh_Y"}}	https://updates.push.services.mozilla.com/wpush/v2/gAAAAABfMjha-cWAJDHM6ESUvgwRssoevr29yxuAtfWAg6NLNd4Ee6xB_KgMvmnyPs6CRyMziL_DltVhueRV0w2_dFDVo9E0lAefpZlgXr2okmmCNbgKobfIZ0Vz25bNwJ-m5nDz3XUCtpkWmKiZDWXkWaeo_Elct1VNlPjWSyUYeffEprD7A4E	1	1
7	{"endpoint":"https://fcm.googleapis.com/fcm/send/c5QyLZM3NQo:APA91bGDJaGCM-csSabe61DO6A0oQ9mJ_OrNQrzwt8EE5U3Z2-rk0Q0IAymL9HdGRfAKfzgQrNAo_vMkVNt29L1lSTtrcNKScHj2ihIHhikdFCT8glOUwi2OSELCOmW7lFSfgMBTfTS7","expirationTime":null,"keys":{"p256dh":"BLTI4b7ZntfQiUZszMBz5rdGpFc6dAhXuX6CREfa7zSqekpJWlGy6NdPn6CiZbOf8VsBCOHEdNmu3xiTtOHYpXI","auth":"SQEUT2l832IeybZEVSCEKw"}}	https://fcm.googleapis.com/fcm/send/c5QyLZM3NQo:APA91bGDJaGCM-csSabe61DO6A0oQ9mJ_OrNQrzwt8EE5U3Z2-rk0Q0IAymL9HdGRfAKfzgQrNAo_vMkVNt29L1lSTtrcNKScHj2ihIHhikdFCT8glOUwi2OSELCOmW7lFSfgMBTfTS7	1	1
8	{"endpoint":"https://bn3p.notify.windows.com/w/?token=BQYAAABLpUc%2fqaAMYV7%2fbvgJnpAJFKBnNLmFdGARZxPz9%2ftEkOoF0oOcWF6hIB0fgkT6Xc3WZ42PcyQbdx%2f0Y96MXBy39kYR7V3SHNjCZWZ5s90iHJ4M%2fJQ6rneAgDdogpyMOOPYsGE0my7%2fe8Fi1UfuzLTdoyRL9JlsNCVIuG4lIqC%2bvNA4BKDDFK%2fEFOQNefYUJukYp4O4z0Ac901OlGySkoPNTKE%2bnKsvkqWkMwp5tAcq9f9SSFK8ZKJpvIsItqA1TRMSmbWr9L4xScxWgbTeYpzgIphXOrDOYSu6b3nLyzV56ARELd%2fEoDSA9zyFg75BqH29d4RVZM9tLp4U04b65%2fRc","expirationTime":null,"keys":{"p256dh":"BMVQxkP_MOqyDMfoVvxZkKYXjmytzcwcAhTGXV39ZQWiyr9_xHLl4TWjReypIfhlY8vzxsOm1jmzPWFtwXS3LiM","auth":"piRvSSeSpYjgg4HugFSS_A"}}	https://bn3p.notify.windows.com/w/?token=BQYAAABLpUc%2fqaAMYV7%2fbvgJnpAJFKBnNLmFdGARZxPz9%2ftEkOoF0oOcWF6hIB0fgkT6Xc3WZ42PcyQbdx%2f0Y96MXBy39kYR7V3SHNjCZWZ5s90iHJ4M%2fJQ6rneAgDdogpyMOOPYsGE0my7%2fe8Fi1UfuzLTdoyRL9JlsNCVIuG4lIqC%2bvNA4BKDDFK%2fEFOQNefYUJukYp4O4z0Ac901OlGySkoPNTKE%2bnKsvkqWkMwp5tAcq9f9SSFK8ZKJpvIsItqA1TRMSmbWr9L4xScxWgbTeYpzgIphXOrDOYSu6b3nLyzV56ARELd%2fEoDSA9zyFg75BqH29d4RVZM9tLp4U04b65%2fRc	1	1
\.


--
-- Data for Name: push_notification_tag_type; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.push_notification_tag_type (id, name, "order") FROM stdin;
1	web	1
\.


--
-- Data for Name: raw_data_type; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.raw_data_type (id, type) FROM stdin;
\.


--
-- Data for Name: text_alignment_type; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.text_alignment_type (id, name, "order") FROM stdin;
1	left	1
2	right	3
3	center	2
\.


--
-- Data for Name: text_block; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.text_block (id, created_at, updated_at, "order", block_type_id, depends_on_id, image_option_id, list_option_id, page_id, table_option_id, text_option_id, uuid) FROM stdin;
1	2020-12-03 14:22:54.858418+00	2020-12-03 16:23:48.785733+00	0	1	\N	\N	\N	1	\N	1	a7390f8d-6282-48ff-aa9d-c1d4417baeb1
2	2020-12-03 14:22:54.89885+00	2020-12-03 16:23:48.804374+00	1	1	\N	\N	\N	1	\N	2	46cc86d8-c236-4b2e-8dad-06caa48f2689
3	2020-12-03 14:22:54.924996+00	2020-12-03 16:23:48.826151+00	2	1	\N	\N	\N	1	\N	3	abc3863b-c1dd-4bb6-b695-6302cef17e16
4	2020-12-03 14:22:54.950276+00	2020-12-03 16:23:48.847618+00	3	1	\N	\N	\N	1	\N	4	07e95ec3-388f-4316-af50-58c555c3732d
70	2020-12-11 20:46:24.416765+00	2020-12-12 15:58:14.652163+00	2	1	\N	\N	\N	2	\N	70	ff8a6f20-4c0b-4098-b519-0afc2f989e94
5	2020-12-03 14:22:54.969487+00	2020-12-03 16:23:48.864278+00	4	1	\N	\N	\N	1	\N	5	28616452-6d93-4806-a852-82f4e72a3a8b
6	2020-12-03 14:22:54.998304+00	2020-12-03 16:23:48.886407+00	5	1	\N	\N	\N	1	\N	6	ea349b77-1a77-4cae-bcf0-c50bc02b3e66
259	2021-01-29 18:22:44.127192+00	2021-01-31 19:34:53.089198+00	0	4	\N	\N	\N	7	79	\N	d4f498e7-f2a6-4de0-b772-015ba456ff3c
7	2020-12-03 14:22:55.050597+00	2020-12-03 16:23:48.904467+00	6	1	\N	\N	\N	1	\N	7	3676a982-2845-496d-8bb4-154baae9807d
8	2020-12-03 14:22:55.076636+00	2020-12-03 16:23:48.927097+00	7	1	\N	\N	\N	1	\N	8	8e5db22f-7f2d-4d8e-8ef4-fceb8482079e
50	2020-12-11 20:26:24.004842+00	2020-12-12 15:58:14.827188+00	10	1	\N	\N	\N	2	\N	50	1201d6b8-5db3-408e-83f2-a52a12d39e35
9	2020-12-03 14:22:55.108969+00	2020-12-03 16:23:48.954251+00	8	1	\N	\N	\N	1	\N	9	0f36232d-6cbe-4e15-8a42-ac9da09d765e
10	2020-12-03 14:22:55.128415+00	2020-12-03 16:23:48.971208+00	9	1	\N	\N	\N	1	\N	10	18c92eb4-0ea8-4231-9438-d73562e8fd8e
71	2020-12-12 18:01:57.981923+00	2021-01-29 18:19:59.43758+00	0	4	\N	\N	\N	3	56	71	ad283214-dc2f-433c-84af-3cd20c4aebb6
11	2020-12-03 14:22:55.147698+00	2020-12-03 16:23:48.993882+00	10	1	\N	\N	\N	1	\N	11	44b10811-a92e-4faa-ab94-8460c75b893f
51	2020-12-11 20:26:24.024077+00	2020-12-12 15:58:14.855544+00	11	1	\N	\N	\N	2	\N	51	7e60b176-e330-49d0-92de-aba9ee1aa2fb
12	2020-12-03 14:22:55.166834+00	2020-12-03 16:23:49.011511+00	11	1	\N	\N	\N	1	\N	12	71a3fa77-21b5-4d5e-b56e-6f10b4c48a1d
260	2021-01-29 18:22:44.147245+00	2021-01-31 19:34:53.168996+00	1	2	259	13	\N	7	\N	\N	c323e7d2-4279-4566-a323-23936dd12f04
13	2020-12-03 14:22:55.186259+00	2020-12-03 16:23:49.02878+00	12	1	\N	\N	\N	1	\N	13	af1b4fb7-3aaa-482c-bb75-7a1c4b2d0185
52	2020-12-11 20:26:24.041344+00	2020-12-12 15:58:14.884339+00	12	1	\N	\N	\N	2	\N	52	2bfc0a7a-9903-4c13-8228-513c96dccc01
14	2020-12-03 14:22:55.206104+00	2020-12-03 16:23:49.045903+00	13	1	\N	\N	\N	1	\N	14	80bb991f-2a4b-4e00-b55e-bd9b213fa6a3
15	2020-12-03 14:22:55.226045+00	2020-12-03 16:23:49.062793+00	14	1	\N	\N	\N	1	\N	15	a264d50a-1737-42de-be38-6b3fe926fbeb
54	2020-12-11 20:39:54.491432+00	2020-12-12 15:58:14.948502+00	15	1	\N	\N	\N	2	\N	54	5d268f19-1306-4203-a4d7-8e9ce6e7a68d
16	2020-12-03 14:22:55.246184+00	2020-12-03 16:23:49.07959+00	15	1	\N	\N	\N	1	\N	16	2ac549a9-0773-42a6-acf6-07bff1cae1a3
170	2020-12-14 14:12:38.937267+00	2021-01-29 18:19:59.583601+00	5	1	\N	\N	\N	3	\N	170	84abe775-5ce9-4f48-8c14-c5efbd18b885
17	2020-12-03 14:22:55.26567+00	2020-12-03 16:23:49.096701+00	16	1	\N	\N	\N	1	\N	17	24113f84-6c16-4729-8aee-eba9e356e8d0
55	2020-12-11 20:39:54.522364+00	2020-12-12 15:58:14.975624+00	16	1	\N	\N	\N	2	\N	55	7494ea6a-6a34-4c1d-8e93-689abd9ce8f3
18	2020-12-03 14:22:55.286019+00	2020-12-03 16:23:49.113775+00	17	1	\N	\N	\N	1	\N	18	8325b9ae-3ea7-488b-92ff-c93e329d21ef
261	2021-01-29 18:22:44.644666+00	2021-01-31 19:34:53.185682+00	2	1	259	\N	\N	7	\N	250	bb8911f5-b51e-4579-b616-0db05e1e24a4
19	2020-12-03 14:22:55.305202+00	2020-12-03 16:23:49.131433+00	18	1	\N	\N	\N	1	\N	19	b1f734de-d39f-4fd6-bd8c-16a14bb6e948
56	2020-12-11 20:39:54.557682+00	2020-12-12 15:58:15.039915+00	17	1	\N	\N	\N	2	\N	56	243f6fe6-2d23-40b6-89d3-e09a33368c93
20	2020-12-03 14:22:55.32482+00	2020-12-03 16:23:49.14941+00	19	1	\N	\N	\N	1	\N	20	067b2b48-684c-40cb-9740-ac4a080803b6
237	2021-01-28 14:40:14.719989+00	2021-01-29 18:19:59.668388+00	10	1	\N	\N	\N	3	\N	233	c59454d2-dadf-453f-9841-5a438474d9f2
21	2020-12-03 14:22:55.344206+00	2020-12-03 16:23:49.167045+00	20	1	\N	\N	\N	1	\N	21	8d95794b-3bb6-4e6f-9b7d-0aaadcb2ce6c
57	2020-12-11 20:39:54.592947+00	2020-12-12 15:58:15.069771+00	18	1	\N	\N	\N	2	\N	57	7759bf21-2940-4d6d-bdec-b3464c7f8dab
22	2020-12-03 14:22:55.369958+00	2020-12-03 16:23:49.184424+00	21	1	\N	\N	\N	1	\N	22	331430bc-1ccb-40c1-82b0-abcd4fda4b42
58	2020-12-11 20:39:54.6288+00	2020-12-12 15:58:15.098928+00	19	1	\N	\N	\N	2	\N	58	71baeafe-1c05-49a6-b851-499615b8e974
247	2021-01-28 19:50:03.521325+00	2021-01-29 18:19:59.952397+00	14	2	\N	11	\N	3	\N	\N	8b3db02d-bbb1-4734-b8c7-810b99dda1ee
23	2020-12-03 14:22:55.388862+00	2020-12-03 16:23:49.201077+00	22	1	\N	\N	\N	1	\N	23	b1d6f166-9f67-4c72-b6fa-00d38c5d90e6
59	2020-12-11 20:39:54.666442+00	2020-12-12 15:58:15.127757+00	20	1	\N	\N	\N	2	\N	59	6034bda5-92e1-4021-93d5-0c1166ba509d
60	2020-12-11 20:39:54.684689+00	2020-12-12 15:58:15.144561+00	21	1	\N	\N	\N	2	\N	60	44d98fa0-060f-4c4f-b1d6-db3959be50a6
262	2021-01-29 18:22:44.661998+00	2021-01-31 19:34:53.202681+00	3	1	259	\N	\N	7	\N	251	f565ceab-9bb1-4c41-ad8a-e9397eb55247
61	2020-12-11 20:39:54.721018+00	2020-12-12 15:58:15.173467+00	22	1	\N	\N	\N	2	\N	61	11bfa4ae-ad48-4ccb-8f58-77777be701a8
183	2020-12-14 14:43:26.062024+00	2021-01-29 18:20:00.076337+00	17	1	\N	\N	\N	3	\N	183	598c72e8-3cd3-4d13-a014-26db426701a8
62	2020-12-11 20:39:54.759523+00	2020-12-12 15:58:15.202551+00	23	1	\N	\N	\N	2	\N	62	31800fa3-baf4-4311-8dd9-1116d579f16e
263	2021-01-29 18:22:44.678692+00	2021-01-31 19:34:53.218881+00	4	1	259	\N	\N	7	\N	252	44a1db02-73cd-499d-a864-e84b74fc2224
63	2020-12-11 20:39:54.789716+00	2020-12-12 15:58:15.227866+00	24	1	\N	\N	\N	2	\N	63	013a04b4-c477-44bf-b32d-c6bb4659f9a8
64	2020-12-11 20:39:54.820336+00	2020-12-12 15:58:15.252413+00	25	1	\N	\N	\N	2	\N	64	8f2bc490-992b-4721-ada5-e21de188e715
65	2020-12-11 20:39:54.857704+00	2020-12-12 15:58:15.281087+00	26	1	\N	\N	\N	2	\N	65	2385c985-cf42-4880-996e-d3b7b5fa9998
264	2021-01-29 18:22:44.697273+00	2021-01-31 19:34:53.235612+00	5	1	\N	\N	\N	7	\N	253	e35390f4-29b1-4e52-b4b6-c49ebabddd7e
66	2020-12-11 20:39:54.876906+00	2020-12-12 15:58:15.296654+00	27	1	\N	\N	\N	2	\N	66	c26c97c0-a4db-4d47-a1c7-5f2a93094c22
67	2020-12-11 20:39:55.056198+00	2020-12-12 15:58:15.421303+00	34	1	\N	\N	\N	2	\N	67	756dd468-c245-49fd-9572-12af88090b9b
265	2021-01-29 18:22:44.714146+00	2021-01-31 19:34:53.406959+00	11	1	\N	\N	\N	7	\N	254	e44be90a-22d0-4aa0-bf88-ddf63392f39d
305	2021-01-31 19:15:41.472184+00	2021-01-31 19:34:53.917191+00	34	1	294	\N	\N	7	\N	291	07e4aad8-2ebf-41a9-ae26-f7adb6007fde
249	2021-01-29 18:06:20.128786+00	2021-01-29 18:20:00.587595+00	42	1	86	\N	\N	3	\N	240	df6430fc-1775-4baa-ba90-5022cd2fe965
250	2021-01-29 18:06:20.147174+00	2021-01-29 18:20:00.602568+00	43	1	86	\N	\N	3	\N	241	c3286877-cfe4-4606-82c5-12f0467d400f
251	2021-01-29 18:06:20.163909+00	2021-01-29 18:20:00.617539+00	44	1	86	\N	\N	3	\N	242	9473a4b0-9644-489d-94db-62c17e055b22
252	2021-01-29 18:06:20.180598+00	2021-01-29 18:20:00.632621+00	45	1	86	\N	\N	3	\N	243	f9ad35a7-6cdc-44fb-9ece-d94fa6c8d426
253	2021-01-29 18:06:20.197706+00	2021-01-29 18:20:00.647458+00	46	1	86	\N	\N	3	\N	244	9075001b-ff60-4659-9812-dc14fbf6477c
254	2021-01-29 18:06:20.217069+00	2021-01-29 18:20:00.672276+00	47	1	86	\N	\N	3	\N	245	3041d775-e2aa-4e7a-83a7-37de3c40ae7e
255	2021-01-29 18:06:20.235144+00	2021-01-29 18:20:00.688704+00	48	1	86	\N	\N	3	\N	246	cda075b7-5a30-4fe9-b410-92dedc260910
68	2020-12-11 20:39:55.092184+00	2020-12-12 15:58:15.450648+00	35	1	\N	\N	\N	2	\N	68	a1235b3e-a9e5-4762-a66b-46a2e9150a3b
69	2020-12-11 20:39:55.127587+00	2020-12-12 15:58:15.475561+00	36	1	\N	\N	\N	2	\N	69	fb79e38b-ba06-402b-9f2a-56068ba47e33
74	2020-12-12 18:15:23.780476+00	2021-01-29 18:19:59.993865+00	16	1	\N	\N	\N	3	\N	74	668dd41f-2513-427a-a34a-d048c2073de7
227	2021-01-28 13:11:49.170655+00	2021-01-29 18:20:00.868326+00	59	1	114	\N	\N	3	\N	223	be4eb467-715e-4bfb-b777-84b5e9f7c14e
266	2021-01-29 18:25:40.552994+00	2021-01-31 19:34:53.251999+00	6	1	\N	\N	\N	7	\N	255	4ab97521-5e61-4d47-8410-c1177228c0d3
76	2020-12-12 18:15:23.836065+00	2021-01-29 18:20:00.105833+00	18	1	\N	\N	\N	3	\N	76	27bd5078-a8f1-43b2-8bcf-5649c1e5afa6
228	2021-01-28 13:11:49.195924+00	2021-01-29 18:20:00.883194+00	60	1	114	\N	\N	3	\N	224	f6972417-8db5-4985-b314-716321903a40
267	2021-01-29 18:25:40.571468+00	2021-01-31 19:34:53.267625+00	7	1	\N	\N	\N	7	\N	256	7f561708-481b-48c8-9d69-948976f6d334
77	2020-12-12 18:15:23.853937+00	2021-01-29 18:20:00.121325+00	19	1	\N	\N	\N	3	\N	77	c74a4ac2-242f-41f8-abc9-26f719f53ecb
268	2021-01-29 18:25:40.596073+00	2021-01-31 19:34:53.288736+00	8	1	\N	\N	\N	7	\N	257	6250e454-5070-40ee-9b72-8e8a2a09efae
78	2020-12-12 18:15:23.877946+00	2021-01-29 18:20:00.140694+00	20	1	\N	\N	\N	3	\N	78	f14dbfe2-0339-4052-8594-631735ce0a39
269	2021-01-29 18:25:40.619482+00	2021-01-31 19:34:53.310014+00	9	1	\N	\N	\N	7	\N	258	4abc8563-5ab5-41c3-9721-1b1dffe8a7d3
79	2020-12-12 18:15:23.913665+00	2021-01-29 18:20:00.168256+00	21	1	\N	\N	\N	3	\N	79	f23f2406-e1a2-4286-b563-961d08f73655
270	2021-01-29 18:25:40.636958+00	2021-01-31 19:34:53.391131+00	10	2	\N	14	\N	7	\N	\N	8de182af-79ef-499c-90f7-70cefbd7724b
229	2021-01-28 13:11:49.221159+00	2021-01-29 18:20:00.898175+00	61	1	114	\N	\N	3	\N	225	c4d48504-e06f-4204-b130-407b88025e7f
271	2021-01-29 18:25:41.19904+00	2021-01-31 19:34:53.485025+00	12	2	\N	15	\N	7	\N	\N	4051c3a7-3d4f-4bfe-a8ea-93cb30696e74
80	2020-12-12 18:15:23.949868+00	2021-01-29 18:20:00.197462+00	22	1	\N	\N	\N	3	\N	80	7c975c68-c77a-4670-93cb-d9244c08400d
81	2020-12-12 18:15:23.968285+00	2021-01-29 18:20:00.212487+00	23	1	\N	\N	\N	3	\N	81	00fb74b0-265f-4176-a376-ce02add54b3e
272	2021-01-29 18:25:41.644515+00	2021-01-31 19:34:53.501872+00	13	1	\N	\N	\N	7	\N	259	ac625959-7ac8-485c-b244-ff6b37f1d9d4
142	2020-12-13 20:56:01.1286+00	2021-01-29 18:20:00.227596+00	24	1	\N	\N	\N	3	\N	142	e9555f90-aa38-4a9a-a73c-fad278a65db9
307	2021-01-31 19:15:41.510581+00	2021-01-31 19:34:53.958498+00	36	1	294	\N	\N	7	\N	293	a1b42bf3-f907-480a-9935-23efb106841c
308	2021-01-31 19:15:41.529354+00	2021-01-31 19:34:53.978792+00	37	1	294	\N	\N	7	\N	294	b1793ea0-be0f-4c34-8a6e-7ffa0ff2199e
309	2021-01-31 19:15:41.547119+00	2021-01-31 19:34:53.99832+00	38	1	294	\N	\N	7	\N	295	7bcc4770-16b6-4bf8-b782-e986e8567f5d
84	2020-12-12 18:15:24.060262+00	2021-01-29 18:20:00.247187+00	25	4	\N	\N	\N	3	57	84	5a537839-9d18-4d93-8fa8-685918510a15
310	2021-01-31 19:15:41.564385+00	2021-01-31 19:34:54.022666+00	39	1	294	\N	\N	7	\N	296	c6314fb8-5952-4e55-9c93-f0aaf203610a
311	2021-01-31 19:15:41.582168+00	2021-01-31 19:34:54.042932+00	40	1	294	\N	\N	7	\N	297	85599da3-4f61-468a-bbdf-30c2c983afc4
312	2021-01-31 19:15:41.599303+00	2021-01-31 19:34:54.065973+00	41	1	294	\N	\N	7	\N	298	addfdfb2-ed63-4c6a-aa69-a3f30089e065
86	2020-12-12 18:15:24.149847+00	2021-01-29 18:20:00.571351+00	41	4	\N	\N	\N	3	58	86	ccdfa9a0-57a8-4fd8-b19c-2f2465e47d14
313	2021-01-31 19:15:41.617489+00	2021-01-31 19:34:54.085557+00	42	1	294	\N	\N	7	\N	299	563c46f0-f79d-4530-a765-3f9682a32ced
314	2021-01-31 19:15:41.637678+00	2021-01-31 19:34:54.105796+00	43	1	294	\N	\N	7	\N	300	2a708891-465d-4121-a56a-86d4d6cd4449
256	2021-01-29 18:06:20.253171+00	2021-01-29 18:20:00.704056+00	49	1	86	\N	\N	3	\N	247	00c47b4e-e3fc-4105-9e14-bf89dd46e4b1
317	2021-01-31 19:30:35.336407+00	2021-01-31 19:34:54.229308+00	50	1	316	\N	\N	7	\N	303	b6c103ea-9755-44b4-aa7c-2f8046346e9d
257	2021-01-29 18:06:20.270582+00	2021-01-29 18:20:00.719609+00	50	1	86	\N	\N	3	\N	248	c9953e06-edeb-424d-873c-fa8db6aaa5a7
318	2021-01-31 19:30:35.353553+00	2021-01-31 19:34:54.245206+00	51	1	316	\N	\N	7	\N	304	27d743fb-5fba-4774-9132-78f95bb92e88
258	2021-01-29 18:06:20.28888+00	2021-01-29 18:20:00.735133+00	51	1	86	\N	\N	3	\N	249	1357efe4-7def-4d4e-a546-b5631d43bed5
319	2021-01-31 19:30:35.370911+00	2021-01-31 19:34:54.261309+00	52	1	316	\N	\N	7	\N	305	c709225f-9fd1-42ad-a83c-5f44f6be2fbe
110	2020-12-13 15:03:21.710665+00	2021-01-29 18:20:00.770072+00	53	1	\N	\N	\N	3	\N	110	b3442cc4-8509-4cc4-8e53-c8de1b957d4f
111	2020-12-13 15:03:21.734095+00	2021-01-29 18:20:00.789441+00	54	1	\N	\N	\N	3	\N	111	d5b1fa22-b46d-40d2-8fd8-79684e5864fd
113	2020-12-13 15:03:21.768194+00	2021-01-29 18:20:00.804523+00	55	1	\N	\N	\N	3	\N	113	284decb4-6b0c-41e7-8913-6f92511ab47a
114	2020-12-13 15:03:21.785396+00	2021-01-29 18:20:00.822274+00	56	4	\N	\N	\N	3	59	114	26e21459-0b94-4c2a-91ae-89f8891b79a1
226	2021-01-28 13:11:49.144728+00	2021-01-29 18:20:00.853441+00	58	1	114	\N	\N	3	\N	222	f9de57f0-7851-4147-aabd-27aee23c4611
24	2020-12-03 19:46:10.481746+00	2020-12-12 15:58:14.62127+00	0	1	\N	\N	\N	2	\N	24	99492e3a-fcd6-4b3c-9c95-624fa10d7241
25	2020-12-03 19:46:10.505032+00	2020-12-12 15:58:14.637018+00	1	1	\N	\N	\N	2	\N	25	cd4a205a-e0e2-47ff-860e-fb6783777f4e
27	2020-12-03 19:46:10.56584+00	2020-12-12 15:58:14.672284+00	3	1	\N	\N	\N	2	\N	27	a6e30de4-1945-4048-bb52-a107acef4bbf
277	2021-01-29 18:27:43.54601+00	2021-01-31 19:34:53.518662+00	14	1	\N	\N	\N	7	\N	264	6ec01925-9ab8-4af4-bee4-04cab8c70987
28	2020-12-03 19:46:10.585286+00	2020-12-12 15:58:14.701911+00	4	1	\N	\N	\N	2	\N	28	f25508a9-b3e6-449f-98dd-7349cb9adc01
144	2020-12-13 21:01:18.115923+00	2021-01-29 18:19:59.599417+00	6	1	\N	\N	\N	3	\N	144	582742b5-0e5d-4d27-95d1-c12d54ff6712
29	2020-12-03 19:46:10.614757+00	2020-12-12 15:58:14.723013+00	5	1	\N	\N	\N	2	\N	29	f2ea53fa-ece7-40eb-bd9d-1421c39e66b8
31	2020-12-03 19:46:10.668405+00	2020-12-12 15:58:14.747438+00	6	1	\N	\N	\N	2	\N	31	fc8acb8c-46e2-40ad-ac85-c0eeca2dfe82
32	2020-12-03 19:46:10.708798+00	2020-12-12 15:58:14.772117+00	7	1	\N	\N	\N	2	\N	32	d4d07fc8-0332-4f09-a387-a66850e65202
146	2020-12-13 21:01:18.151488+00	2021-01-29 18:19:59.614569+00	7	1	\N	\N	\N	3	\N	146	3d400b26-a927-43b9-b7c4-c63d89a6973b
34	2020-12-03 19:46:10.75369+00	2020-12-12 15:58:14.787162+00	8	1	\N	\N	\N	2	\N	34	877796bb-5791-47cb-80bb-6fa20145e520
35	2020-12-03 19:46:10.775699+00	2020-12-12 15:58:14.802527+00	9	1	\N	\N	\N	2	\N	35	355bb936-7be9-46e4-bbfc-e9ec0b28b44e
39	2020-12-03 19:46:10.882436+00	2020-12-12 15:58:14.904401+00	13	1	\N	\N	\N	2	\N	39	3b206652-1c84-4626-8bc5-2077a45d8c08
147	2020-12-13 21:01:18.174739+00	2021-01-29 18:19:59.633907+00	8	1	\N	\N	\N	3	\N	147	82716af0-e6aa-421e-bcfa-e91278da21e6
40	2020-12-03 19:46:10.902498+00	2020-12-12 15:58:14.933288+00	14	1	\N	\N	\N	2	\N	40	55e00ecd-3beb-4da8-829a-76f0f8a29e95
41	2020-12-03 19:46:10.92237+00	2020-12-12 15:58:15.312377+00	28	1	\N	\N	\N	2	\N	41	10033245-6572-4042-97ce-7f8dcbc9f1f7
278	2021-01-29 18:27:43.573553+00	2021-01-31 19:34:53.545164+00	15	1	\N	\N	\N	7	\N	265	a12feb14-2a5e-4149-9f0a-75869cbfd00a
149	2020-12-13 21:01:18.211054+00	2021-01-29 18:19:59.843531+00	11	2	\N	4	\N	3	\N	149	acbe0137-793c-4de5-935d-50f05cd58fa8
150	2020-12-13 21:01:18.229531+00	2021-01-29 18:19:59.860124+00	12	1	\N	\N	\N	3	\N	150	a6f2e490-a88d-4959-ac97-1bd59219e1e6
246	2021-01-28 15:35:41.345836+00	2021-01-29 18:19:59.875551+00	13	1	\N	\N	\N	3	\N	238	2b17de2b-9c7d-4306-86a6-154b7087581b
279	2021-01-29 18:27:43.601832+00	2021-01-31 19:34:53.570699+00	16	1	\N	\N	\N	7	\N	266	7a3f0bff-e538-4ac9-8e6a-de3301ca905d
225	2021-01-28 13:11:49.119738+00	2021-01-29 18:20:00.837988+00	57	1	114	\N	\N	3	\N	221	663e6d2f-b498-43a2-88e4-c526a59bdfb9
281	2021-01-29 18:27:43.642149+00	2021-01-31 19:34:53.70184+00	22	1	\N	\N	\N	7	\N	268	8b81f9dd-436f-4ce8-845a-ec71edc35e1e
230	2021-01-28 13:11:49.246329+00	2021-01-29 18:20:00.913206+00	62	1	114	\N	\N	3	\N	226	7a8318b8-c947-4378-8981-27c63b1fca4a
306	2021-01-31 19:15:41.492521+00	2021-01-31 19:34:53.937813+00	35	1	294	\N	\N	7	\N	292	512aeeea-ced8-4df6-9f02-5517213b1aaa
231	2021-01-28 13:11:49.289208+00	2021-01-29 18:20:00.937362+00	63	1	114	\N	\N	3	\N	227	c5335eb3-df3b-4b87-a222-91ef7148e644
282	2021-01-29 18:27:43.659386+00	2021-01-31 19:34:54.12541+00	44	1	\N	\N	\N	7	\N	269	7a1b2388-a502-41d2-8ff6-d927cd31bda6
232	2021-01-28 13:11:49.330835+00	2021-01-29 18:20:00.961454+00	64	1	114	\N	\N	3	\N	228	ecee5e15-fc00-4153-9d3d-38a3a13962da
233	2021-01-28 13:11:49.371854+00	2021-01-29 18:20:00.985853+00	65	1	114	\N	\N	3	\N	229	d589f2b2-6bab-4d01-b7fa-8272c68ad6a1
283	2021-01-29 18:27:43.676021+00	2021-01-31 19:34:54.140643+00	45	1	\N	\N	\N	7	\N	270	1afa5b0c-2613-4579-b4a0-47c8efd3b2cd
234	2021-01-28 13:11:49.414333+00	2021-01-29 18:20:01.010426+00	66	1	114	\N	\N	3	\N	230	f29e130b-1e22-4d8e-90af-d28bac81a325
284	2021-01-29 18:27:43.692964+00	2021-01-31 19:34:54.156143+00	46	1	\N	\N	\N	7	\N	271	02bf76ce-56a7-4db4-bbc7-6c61df2e4c3c
235	2021-01-28 13:11:49.450378+00	2021-01-29 18:20:01.031121+00	67	1	\N	\N	\N	3	\N	231	fd2652ea-6e93-413c-89b8-1ab707e469b6
182	2020-12-14 14:16:13.073843+00	2021-01-29 18:20:01.112967+00	68	2	\N	12	\N	3	\N	182	d90bc220-411a-4b65-a93f-37137090dc72
285	2021-01-29 18:27:43.709731+00	2021-01-31 19:34:54.176645+00	47	1	\N	\N	\N	7	\N	272	a668e6fb-1bf7-4d05-b235-27f8ebb0454e
248	2021-01-28 19:53:11.866982+00	2021-01-29 18:20:01.13781+00	69	1	\N	\N	\N	3	\N	239	ee487184-ff74-4042-9e79-1123fb69bbf6
127	2020-12-13 20:29:02.659139+00	2021-01-29 18:20:01.162365+00	70	1	\N	\N	\N	3	\N	127	6900db99-ee4b-42c0-9f19-c7fdedf00e59
321	2021-01-31 19:30:35.406666+00	2021-01-31 19:34:54.291998+00	54	1	316	\N	\N	7	\N	307	0cbbc699-4f1f-491f-9b34-8eae19ee40f8
108	2020-12-12 18:15:24.673556+00	2021-01-29 18:20:01.224359+00	71	1	\N	\N	\N	3	\N	108	8fabb33f-eaca-49d6-a7dc-ed45cb55f646
128	2020-12-13 20:29:02.694836+00	2021-01-29 18:20:01.29987+00	72	1	\N	\N	\N	3	\N	128	b2fca47f-f93b-4d15-b00c-5814f113fc13
322	2021-01-31 19:30:35.424956+00	2021-01-31 19:34:54.307943+00	55	1	316	\N	\N	7	\N	308	af77ef10-e19e-4482-9ce6-4af86c4a50db
129	2020-12-13 20:29:02.714178+00	2021-01-29 18:20:01.374431+00	73	1	\N	\N	\N	3	\N	129	84759b94-e515-45dc-bbe9-519fad8fb891
130	2020-12-13 20:29:02.733159+00	2021-01-29 18:20:01.424896+00	74	1	\N	\N	\N	3	\N	130	a8709398-d9ee-4a78-9c1b-020a164a6844
323	2021-01-31 19:30:35.450752+00	2021-01-31 19:34:54.328678+00	56	1	316	\N	\N	7	\N	309	293b2323-e471-4ef8-a8d5-24dba4c964ac
131	2020-12-13 20:29:02.751761+00	2021-01-29 18:20:01.476096+00	75	1	\N	\N	\N	3	\N	131	49dc2fa2-950c-44c7-85fb-8d2cfe4d3ed3
324	2021-01-31 19:30:35.47341+00	2021-01-31 19:34:54.350457+00	57	1	316	\N	\N	7	\N	310	d0d0d39b-ee81-4adc-b01b-3d0e77726ac8
325	2021-01-31 19:30:35.496693+00	2021-01-31 19:34:54.372748+00	58	1	316	\N	\N	7	\N	311	f7c21cb7-a975-47ca-b080-62193bba7675
42	2020-12-03 19:46:10.944759+00	2020-12-12 15:58:15.327485+00	29	1	\N	\N	\N	2	\N	42	f50b0564-cd96-4efd-803b-6e40698d0114
204	2021-01-28 13:11:46.709773+00	2021-01-29 18:19:59.517261+00	1	2	71	3	\N	3	\N	\N	a56ab735-5385-44bd-9883-f1093c800101
43	2020-12-03 19:46:10.972542+00	2020-12-12 15:58:15.342622+00	30	1	\N	\N	\N	2	\N	43	2598c23b-8499-4df9-a08c-dc57b5534c95
44	2020-12-03 19:46:10.996261+00	2020-12-12 15:58:15.357859+00	31	1	\N	\N	\N	2	\N	44	28b26d4b-28e9-43ab-bc9f-2f2445a3d9d1
289	2021-01-31 19:11:54.914124+00	2021-01-31 19:34:53.586999+00	17	1	\N	\N	\N	7	\N	276	10da57be-32a0-4c65-9fed-961d421925f0
45	2020-12-03 19:46:11.018445+00	2020-12-12 15:58:15.376267+00	32	1	\N	\N	\N	2	\N	45	405ccbd3-acdc-4c86-a610-5cd284e3b971
205	2021-01-28 13:11:47.26571+00	2021-01-29 18:19:59.533978+00	2	1	71	\N	\N	3	\N	201	805c1f04-429e-4c6f-9637-61954580dc58
46	2020-12-03 19:46:11.038835+00	2020-12-12 15:58:15.392238+00	33	1	\N	\N	\N	2	\N	46	b5a4f357-5581-4d0f-a5fd-6d0c10b1c52f
48	2020-12-03 19:46:11.157762+00	2020-12-12 15:58:15.504914+00	37	1	\N	\N	\N	2	\N	48	5ade5099-fb8c-45d1-a15d-68beda6d469f
49	2020-12-03 19:46:11.178421+00	2020-12-12 15:58:15.520513+00	38	1	\N	\N	\N	2	\N	49	742a6ec1-2858-4f26-b51f-4bcbf2245395
206	2021-01-28 13:11:47.293846+00	2021-01-29 18:19:59.54939+00	3	1	71	\N	\N	3	\N	202	f5502cb6-8073-4205-826f-7f3d4e909e81
207	2021-01-28 13:11:47.320423+00	2021-01-29 18:19:59.566908+00	4	1	71	\N	\N	3	\N	203	f05eb625-b7de-4637-8ed5-b11f454d0f74
290	2021-01-31 19:11:54.940289+00	2021-01-31 19:34:53.607922+00	18	1	\N	\N	\N	7	\N	277	b7a71c1c-d950-4662-b90d-8bee1853e74a
208	2021-01-28 13:11:47.478303+00	2021-01-29 18:19:59.653266+00	9	1	\N	\N	\N	3	\N	204	f32b8587-9cf1-4c28-af1f-2980fc74647e
245	2021-01-28 15:34:00.728058+00	2021-01-29 18:19:59.968417+00	15	1	\N	\N	\N	3	\N	237	4b5189e1-24ee-44a7-9b55-38bdeed7b8e5
291	2021-01-31 19:11:54.975041+00	2021-01-31 19:34:53.638188+00	19	1	\N	\N	\N	7	\N	278	f67d7464-9b1d-4386-b862-ee808f961a50
209	2021-01-28 13:11:48.542736+00	2021-01-29 18:20:00.263159+00	26	1	84	\N	\N	3	\N	205	692a5c03-1cfb-4646-b6fe-5d01b7f0290d
210	2021-01-28 13:11:48.569397+00	2021-01-29 18:20:00.278566+00	27	1	84	\N	\N	3	\N	206	9f6914e7-8f81-4904-8281-2ff5fb62eefa
211	2021-01-28 13:11:48.594981+00	2021-01-29 18:20:00.294017+00	28	1	84	\N	\N	3	\N	207	d7e13024-10b8-4d2e-bb70-286e2ddabd76
292	2021-01-31 19:11:55.054488+00	2021-01-31 19:34:53.667869+00	20	1	\N	\N	\N	7	\N	279	b44f3056-9084-4ff0-81cd-eae5b7261624
212	2021-01-28 13:11:48.620104+00	2021-01-29 18:20:00.309621+00	29	1	84	\N	\N	3	\N	208	f934ed40-011b-4eb7-8e85-60b7c1351bcd
213	2021-01-28 13:11:48.64422+00	2021-01-29 18:20:00.324735+00	30	1	84	\N	\N	3	\N	209	32601a48-8b12-4c50-8774-dbcf156a0c32
293	2021-01-31 19:11:55.072672+00	2021-01-31 19:34:53.683741+00	21	1	\N	\N	\N	7	\N	280	b696f7c3-8405-42b2-aa42-6c4365b4f33c
214	2021-01-28 13:11:48.670145+00	2021-01-29 18:20:00.340261+00	31	1	84	\N	\N	3	\N	210	ea91eb10-74d9-42ae-9239-487b40e4b2bf
215	2021-01-28 13:11:48.696451+00	2021-01-29 18:20:00.361291+00	32	1	84	\N	\N	3	\N	211	5d9111d9-0efe-49ff-b8c0-cbf5a527a25b
216	2021-01-28 13:11:48.722155+00	2021-01-29 18:20:00.3811+00	33	1	84	\N	\N	3	\N	212	9ab99192-6bd1-41ff-9b36-f2da8ccac427
294	2021-01-31 19:11:55.110443+00	2021-01-31 19:34:53.719549+00	23	4	\N	\N	\N	7	80	\N	1ac76851-8d36-41db-9c4c-8e14b9df90aa
217	2021-01-28 13:11:48.747619+00	2021-01-29 18:20:00.406229+00	34	1	84	\N	\N	3	\N	213	a1afaea3-82d8-4780-9503-a01f39d85735
218	2021-01-28 13:11:48.772804+00	2021-01-29 18:20:00.430514+00	35	1	84	\N	\N	3	\N	214	b099414f-41c1-457e-b071-31c453b2ace8
295	2021-01-31 19:11:55.131111+00	2021-01-31 19:34:53.736204+00	24	1	294	\N	\N	7	\N	281	6a370973-5abe-4f35-8fb9-3037e34cd61a
219	2021-01-28 13:11:48.797859+00	2021-01-29 18:20:00.454293+00	36	1	84	\N	\N	3	\N	215	59574d9c-69a5-4d95-b592-a76f92aa995c
296	2021-01-31 19:11:55.148984+00	2021-01-31 19:34:53.751185+00	25	1	294	\N	\N	7	\N	282	317b8e3f-dc5a-4a08-9daa-b4d9f68e6743
220	2021-01-28 13:11:48.824623+00	2021-01-29 18:20:00.474189+00	37	1	84	\N	\N	3	\N	216	b16bca1c-3e3f-40c6-b6f3-8fbf26623f11
221	2021-01-28 13:11:48.849132+00	2021-01-29 18:20:00.494852+00	38	1	84	\N	\N	3	\N	217	32b207b7-387d-4598-a8e1-0eb46939f26d
297	2021-01-31 19:11:55.16669+00	2021-01-31 19:34:53.766501+00	26	1	294	\N	\N	7	\N	283	7f7e690b-9aed-4968-8ddc-48d1b7746f71
222	2021-01-28 13:11:48.875057+00	2021-01-29 18:20:00.52007+00	39	1	84	\N	\N	3	\N	218	0c5886c8-d1dd-450b-9262-8e39fa2e1fad
298	2021-01-31 19:11:55.184445+00	2021-01-31 19:34:53.782604+00	27	1	294	\N	\N	7	\N	284	57ec9dba-179d-4ac3-8fe3-725a317a9b90
223	2021-01-28 13:11:48.901458+00	2021-01-29 18:20:00.544973+00	40	1	84	\N	\N	3	\N	219	abc5ddfe-7a5a-4e01-a61e-65c43e4a3395
299	2021-01-31 19:11:55.201977+00	2021-01-31 19:34:53.797669+00	28	1	294	\N	\N	7	\N	285	9dc23814-5cfd-41d8-b2e6-c5a594a9a165
107	2020-12-12 18:15:24.655217+00	2021-01-29 18:20:00.750497+00	52	1	\N	\N	\N	3	\N	107	f98fc4a7-419c-4a2a-8044-46c349f332ed
236	2021-01-28 13:11:49.696041+00	2021-01-29 18:20:01.825533+00	79	1	\N	\N	\N	3	\N	232	3055d6fd-7e7a-4f43-a8d4-debdb09e21ff
300	2021-01-31 19:11:55.220533+00	2021-01-31 19:34:53.813089+00	29	1	294	\N	\N	7	\N	286	1312a3fe-4dde-47fe-bae1-5d8c7b01e47a
238	2021-01-28 15:06:21.29347+00	2021-01-29 18:20:01.865295+00	80	1	\N	\N	\N	3	\N	234	cc474083-4f62-4abe-aed4-0555819251ef
301	2021-01-31 19:11:55.2441+00	2021-01-31 19:34:53.834669+00	30	1	294	\N	\N	7	\N	287	acf0c046-47b2-4a87-850e-1e4accfe90a8
302	2021-01-31 19:11:55.267654+00	2021-01-31 19:34:53.855455+00	31	1	294	\N	\N	7	\N	288	cb75a766-792f-424b-ad4b-29ae59f68615
303	2021-01-31 19:11:55.286112+00	2021-01-31 19:34:53.875938+00	32	1	294	\N	\N	7	\N	289	c9bb5c32-a756-4ed9-b688-e5ea1e1c8ab3
304	2021-01-31 19:11:55.303984+00	2021-01-31 19:34:53.89621+00	33	1	294	\N	\N	7	\N	290	7950db56-dfd1-4369-beb7-0fdbef540811
315	2021-01-31 19:26:53.752945+00	2021-01-31 19:34:54.19419+00	48	1	\N	\N	\N	7	\N	301	1196f1e8-5455-4482-844b-fb95cc532b68
316	2021-01-31 19:26:53.770582+00	2021-01-31 19:34:54.212811+00	49	4	\N	\N	\N	7	81	302	ecb721fc-723d-4303-859e-8a2e17c1361e
132	2020-12-13 20:29:02.77105+00	2021-01-29 18:20:01.576687+00	76	1	\N	\N	\N	3	\N	132	fc5e2fa5-c6af-40df-abba-1e7119ab0cf7
320	2021-01-31 19:30:35.387776+00	2021-01-31 19:34:54.276837+00	53	1	316	\N	\N	7	\N	306	d14fdc5e-1886-4337-ad62-349dfaa0d590
133	2020-12-13 20:29:02.791521+00	2021-01-29 18:20:01.664447+00	77	1	\N	\N	\N	3	\N	133	2c349efb-b524-438c-83da-39c1f2c2ec36
134	2020-12-13 20:29:02.81161+00	2021-01-29 18:20:01.737936+00	78	1	\N	\N	\N	3	\N	134	1bc9b365-f810-49a5-96a6-8dcfe037d35c
243	2021-01-28 15:06:23.331771+00	2021-01-29 18:20:01.945743+00	81	1	\N	\N	\N	3	\N	235	f1b2e7e2-1595-4cdb-b582-9cf5dcecc167
326	2021-01-31 19:30:35.52128+00	2021-01-31 19:34:54.393502+00	59	1	316	\N	\N	7	\N	312	a431f1b7-73eb-4c9d-8e01-9f1185dcc83e
286	2021-01-29 18:27:43.726694+00	2021-01-31 19:34:54.4138+00	60	1	\N	\N	\N	7	\N	273	da4678d7-631c-4149-aaa0-c2f4ed8d37df
327	2021-01-31 19:30:35.563144+00	2021-01-31 19:34:54.493541+00	61	2	\N	16	\N	7	\N	\N	91f9ab10-4b8e-43c8-a5e6-afe3dcdec56e
287	2021-01-29 18:27:43.74396+00	2021-01-31 19:34:54.509745+00	62	1	\N	\N	\N	7	\N	274	5a0e2e13-5ed2-4a41-9314-b82f12eb55d4
288	2021-01-29 18:27:43.76164+00	2021-01-31 19:34:54.526428+00	63	1	\N	\N	\N	7	\N	275	7fb346f5-b75f-4114-b1ca-162860cabeb4
274	2021-01-29 18:25:41.68238+00	2021-01-31 19:34:54.543563+00	64	1	\N	\N	\N	7	\N	261	fde6f55a-4346-431f-b43c-1b90ab39f728
328	2021-01-31 19:33:12.082079+00	2021-01-31 19:34:54.560176+00	65	1	\N	\N	\N	7	\N	313	539526e4-291a-4e20-8a84-c7da800180c2
329	2021-01-31 19:33:12.099679+00	2021-01-31 19:34:54.577139+00	66	1	\N	\N	\N	7	\N	314	db05413a-6286-4ad9-ac94-f36a9c2d78db
330	2021-01-31 19:33:12.117845+00	2021-01-31 19:34:54.593704+00	67	1	\N	\N	\N	7	\N	315	3d5cf27e-56c7-4a3b-a5ba-7f2a51e1bbaa
331	2021-01-31 19:33:12.135681+00	2021-01-31 19:34:54.609457+00	68	1	\N	\N	\N	7	\N	316	c4b01805-7542-439f-86ad-b99d430db9cc
332	2021-01-31 19:33:12.153508+00	2021-01-31 19:34:54.625321+00	69	1	\N	\N	\N	7	\N	317	64cb86fa-9239-4de6-9e5a-ac8b1e8272f0
333	2021-01-31 19:33:12.171314+00	2021-01-31 19:34:54.641431+00	70	1	\N	\N	\N	7	\N	318	2e3b902f-0c2c-494b-931c-933ad12b1f34
334	2021-01-31 19:33:12.18828+00	2021-01-31 19:34:54.656849+00	71	1	\N	\N	\N	7	\N	319	37370433-3775-4583-9cf8-87992b98872a
335	2021-01-31 19:33:12.205786+00	2021-01-31 19:34:54.67238+00	72	1	\N	\N	\N	7	\N	320	3ef2a79d-26d0-4490-a973-10ca5b8b5222
336	2021-01-31 19:33:12.223658+00	2021-01-31 19:34:54.688144+00	73	1	\N	\N	\N	7	\N	321	297ceefa-5aa3-4780-a73b-e1c88b18fd02
275	2021-01-29 18:25:41.700809+00	2021-01-31 19:34:54.704305+00	74	1	\N	\N	\N	7	\N	262	16f7ad50-5950-4096-86ff-82347c106a7a
276	2021-01-29 18:25:41.718624+00	2021-01-31 19:34:54.720791+00	75	1	\N	\N	\N	7	\N	263	9a2b711d-7736-4f71-8b4e-7fcf548cf387
\.


--
-- Data for Name: text_block_type; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.text_block_type (id, name, is_primitive, "order") FROM stdin;
4	table	f	4
1	text	t	1
2	image	t	2
3	table	f	3
\.


--
-- Data for Name: text_block_type_can_contain_type; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.text_block_type_can_contain_type (id, block_id, contain_id) FROM stdin;
1	3	2
2	3	1
\.


--
-- Data for Name: text_content; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.text_content (id, created_at, updated_at, "order", text, is_bold, is_italic, is_underline, is_code, latex_equation, marker_color, text_color, block_id, link, uuid, custom_value, is_custom, text_size) FROM stdin;
257	2020-12-11 20:46:24.410452+00	2020-12-12 15:58:14.640861+00	0		f	f	f	f	\N	\N		25	\N	a7d3ac00-c22e-4cc6-b5c7-bb9468e0705e	\N	f	12
258	2020-12-11 20:46:24.428994+00	2020-12-12 15:58:14.655834+00	0	Data de Atualização	f	f	f	f	\N	\N		70	\N	40e1b0b8-5409-42d9-9851-a5c4e3a68da0	691	t	12
259	2020-12-11 20:46:24.434828+00	2020-12-12 15:58:14.660285+00	1	  \n	f	f	f	f	\N	\N		70	\N	1d322dd9-a5ca-4b37-922f-63fdf4f9dcf3	\N	f	12
260	2020-12-11 20:46:24.452565+00	2020-12-12 15:58:14.676223+00	0	Número da Proposta: 	t	f	f	f	\N	\N	#0086c0	27	\N	79b3547e-b6cb-46f3-acf1-d7937301c2b6	\N	f	12
261	2020-12-11 20:46:24.458844+00	2020-12-12 15:58:14.680694+00	1	Id do Negócio	f	f	f	f	\N	\N		27	\N	dbb5c2f0-46db-4bf2-8dd7-137f0910731a	694	t	12
31	2020-12-03 16:23:48.791024+00	2020-12-03 16:23:48.791055+00	0	Proposta Comercial 	t	f	f	f	\N	\N	#0086c0	1	\N	23695d39-347e-4bad-bc95-8bf3911eb5e0	\N	f	12
2	2020-12-03 14:22:54.912374+00	2020-12-03 16:23:48.808504+00	0	Nome do Cliente	f	f	f	f	\N	\N		2	\N	0ad182b0-eef3-4236-8db5-bbc6ca66d604	638	t	12
3	2020-12-03 14:22:54.918798+00	2020-12-03 16:23:48.813482+00	1	 	f	f	f	f	\N	\N		2	\N	84f41c61-4de0-45da-bc97-abad39b98e7e	\N	f	12
4	2020-12-03 14:22:54.937921+00	2020-12-03 16:23:48.830245+00	0	CNPJ/ CPF	f	f	f	f	\N	\N		3	\N	8c666e37-d94b-43e8-9415-dc99f782d62c	639	t	12
5	2020-12-03 14:22:54.94391+00	2020-12-03 16:23:48.835132+00	1	 	f	f	f	f	\N	\N		3	\N	5721af6e-f6ad-4ce0-8076-82a0856d24c3	\N	f	12
6	2020-12-03 14:22:54.963432+00	2020-12-03 16:23:48.851706+00	0		f	f	f	f	\N	\N		4	\N	b04bf95a-15d5-471f-904b-34c42baa6f44	\N	f	12
7	2020-12-03 14:22:54.986176+00	2020-12-03 16:23:48.868359+00	0	Data do Registro	f	f	f	f	\N	#0086c050		5	\N	c8ea32d8-eace-48ff-837a-fc017f4c2f3d	662	t	12
8	2020-12-03 14:22:54.992337+00	2020-12-03 16:23:48.87338+00	1	 	f	f	f	f	\N	\N		5	\N	b8fea643-4ea6-4c72-b2a1-aa4f47a9041f	\N	f	12
9	2020-12-03 14:22:55.044219+00	2020-12-03 16:23:48.890822+00	0		f	f	f	f	\N	\N		6	\N	662225d6-cf3a-4e1d-a869-cc8f6547306e	\N	f	12
10	2020-12-03 14:22:55.064001+00	2020-12-03 16:23:48.908615+00	0	Nome do Cliente	f	f	f	f	\N	\N		7	\N	7d731055-0cf5-4201-8f8d-32176d940cf0	638	t	12
11	2020-12-03 14:22:55.070477+00	2020-12-03 16:23:48.913713+00	1	 	f	f	f	f	\N	\N		7	\N	00ce213e-308b-4a18-8c31-7335febdbfab	\N	f	12
12	2020-12-03 14:22:55.090192+00	2020-12-03 16:23:48.931212+00	0	A/C: 	f	f	f	f	\N	\N		8	\N	088a52f6-9561-44fa-9872-d72514b589d2	\N	f	12
13	2020-12-03 14:22:55.096553+00	2020-12-03 16:23:48.936195+00	1	Nome do Contato	f	f	f	f	\N	\N		8	\N	1c7848d3-5f5b-4fb5-a94b-9068c8e4e4c6	641	t	12
14	2020-12-03 14:22:55.102697+00	2020-12-03 16:23:48.941328+00	2	 	f	f	f	f	\N	\N		8	\N	d9ca51b2-73a3-4dd0-bc5c-9dcc59acdfe9	\N	f	12
15	2020-12-03 14:22:55.122147+00	2020-12-03 16:23:48.958338+00	0	Plano:	f	f	f	f	\N	\N		9	\N	515db0a7-c791-40d5-b112-dc9c583ed74e	\N	f	12
16	2020-12-03 14:22:55.141439+00	2020-12-03 16:23:48.975381+00	0	Negociação: 	f	f	f	f	\N	\N		10	\N	c9ddb6df-e269-495e-801a-3ee05425edb2	\N	f	12
17	2020-12-03 14:22:55.160676+00	2020-12-03 16:23:48.998081+00	0		f	f	f	f	\N	\N		11	\N	bb73ff59-a107-42cc-90da-28a2821f707d	\N	f	12
18	2020-12-03 14:22:55.179846+00	2020-12-03 16:23:49.015795+00	0		f	f	f	f	\N	\N		12	\N	4526c782-11fb-425f-80c8-3ed95bd9ca6c	\N	f	12
19	2020-12-03 14:22:55.199617+00	2020-12-03 16:23:49.032858+00	0	Seguem abaixo os detalhes do plano sugerido pela Consulting	f	f	f	f	\N	\N		13	\N	7f63060b-ad60-4f85-8cbb-8a3a6913bd60	\N	f	12
20	2020-12-03 14:22:55.219751+00	2020-12-03 16:23:49.049928+00	0	Plano	f	f	f	f	\N	\N		14	\N	d878cb97-e7c9-425c-8359-22e0e0d9a3ff	\N	f	12
21	2020-12-03 14:22:55.240079+00	2020-12-03 16:23:49.066803+00	0		f	f	f	f	\N	\N		15	\N	1da2395b-2278-4d75-9f82-c8e7f456b6d3	\N	f	12
22	2020-12-03 14:22:55.259379+00	2020-12-03 16:23:49.083929+00	0		f	f	f	f	\N	\N		16	\N	2dd71611-ee2f-4498-af94-8a5441a08c56	\N	f	12
23	2020-12-03 14:22:55.27984+00	2020-12-03 16:23:49.101032+00	0		f	f	f	f	\N	\N		17	\N	fec7bdd8-b481-4b1d-b44f-9a3b89b6cf5f	\N	f	12
24	2020-12-03 14:22:55.299097+00	2020-12-03 16:23:49.118103+00	0		f	f	f	f	\N	\N		18	\N	7def0ea9-f3e8-4cfa-969d-820a13effaf1	\N	f	12
25	2020-12-03 14:22:55.318371+00	2020-12-03 16:23:49.135631+00	0		f	f	f	f	\N	\N		19	\N	d2784b52-6051-4022-8abf-21de2b43e556	\N	f	12
26	2020-12-03 14:22:55.338252+00	2020-12-03 16:23:49.153496+00	0		f	f	f	f	\N	\N		20	\N	a675b7f1-30fd-4385-b5e3-535b5018dc88	\N	f	12
27	2020-12-03 14:22:55.36368+00	2020-12-03 16:23:49.171243+00	0		f	f	f	f	\N	\N		21	\N	3f87cc77-f4dd-4ba2-aca2-e416c8e0fead	\N	f	12
28	2020-12-03 14:22:55.382876+00	2020-12-03 16:23:49.188504+00	0		f	f	f	f	\N	\N		22	\N	9a9f49a7-685c-4862-9eee-f7222a63597e	\N	f	12
29	2020-12-03 14:22:55.402282+00	2020-12-03 16:23:49.205133+00	0	\n	f	f	f	f	\N	\N		23	\N	534fd396-342f-417e-aa06-b55a58818582	\N	f	12
262	2020-12-11 20:46:24.464956+00	2020-12-12 15:58:14.685286+00	2	 	f	f	f	f	\N	\N		27	\N	8ce7402b-24c4-417f-b692-aab42ece23c1	\N	f	12
263	2020-12-11 20:46:24.470909+00	2020-12-12 15:58:14.689853+00	3	\n	t	f	f	f	\N	\N	#0086c0	27	\N	482d6102-8bb7-4ce7-ac7c-81c32b08d866	\N	f	12
787	2021-01-28 14:40:14.635481+00	2021-01-29 18:19:59.603242+00	0		f	f	f	f	\N	\N		144	\N	ac5dd4b0-d8e5-4b7a-b938-190a068e3dd3	\N	f	12
788	2021-01-28 14:40:14.712117+00	2021-01-29 18:19:59.657098+00	0		f	f	f	f	\N	\N		208	\N	8a919b75-d9f1-42e7-af12-d0b9043615f1	\N	f	12
264	2020-12-11 20:46:24.564087+00	2020-12-12 15:58:14.775738+00	0		f	f	f	f	\N	\N		32	\N	88b0e49b-802a-468f-beef-8cc972e66150	\N	f	12
789	2021-01-28 14:40:14.736526+00	2021-01-29 18:19:59.672126+00	0		f	f	f	f	\N	\N		237	\N	9422509f-7426-4d6b-b0b1-1175a7f49fb7	\N	f	12
811	2021-01-28 15:35:41.337389+00	2021-01-29 18:19:59.863929+00	0		f	f	f	f	\N	\N		150	\N	88789178-1f48-45a4-bc6b-dc30d8cff97c	\N	f	12
813	2021-01-28 19:50:03.512852+00	2021-01-29 18:19:59.879253+00	0		f	f	f	f	\N	\N		246	\N	5227b2a7-f4c1-4895-8d9f-737fb35ea1aa	\N	f	12
267	2020-12-12 15:28:07.145229+00	2020-12-12 15:58:14.806543+00	0	Plano I: 	t	f	f	f	\N	\N	#0086c0	35	\N	4358a4b8-9ba1-4a06-ac3c-b73b2e8c5fa3	\N	f	12
268	2020-12-12 15:28:07.152498+00	2020-12-12 15:58:14.81103+00	1	Plano I	f	f	f	f	\N	\N		35	\N	5fb9e3a4-fac8-4ffb-a42d-b871013433d5	695	t	12
180	2020-12-11 20:32:09.362987+00	2020-12-12 15:58:14.830902+00	0	Quantidade: 	t	f	f	f	\N	\N	#0086c0	50	\N	a3b5e50d-e3d5-45a6-b6c4-fee0f6a77ca3	\N	f	12
181	2020-12-11 20:32:09.368817+00	2020-12-12 15:58:14.83538+00	1	Quantidade	f	f	f	f	\N	\N		50	\N	7ec2aeb7-3860-4ef4-af6e-fca656cb5ef0	705	t	12
182	2020-12-11 20:32:09.374517+00	2020-12-12 15:58:14.839866+00	2	 	f	f	f	f	\N	\N		50	\N	051c85d8-3242-49db-8a8f-99325d45a944	\N	f	12
183	2020-12-11 20:32:09.380085+00	2020-12-12 15:58:14.844279+00	3	          \n	t	f	f	f	\N	\N	#0086c0	50	\N	fecd8a43-8a59-4045-ac92-87c49de54595	\N	f	12
184	2020-12-11 20:32:09.396823+00	2020-12-12 15:58:14.859171+00	0	Valor Unitário : 	t	f	f	f	\N	\N	#0086c0	51	\N	0aa7715f-5708-4e6f-9502-65a50de71215	\N	f	12
186	2020-12-11 20:32:09.409396+00	2020-12-12 15:58:14.868079+00	2	 	f	f	f	f	\N	\N		51	\N	9bf660b8-b90b-4635-ad4b-dee43704ec70	\N	f	12
271	2020-12-12 15:28:07.748179+00	2020-12-12 15:58:15.396302+00	0	Custo Atual : 	t	f	f	f	\N	\N		46	\N	8084dd41-5805-4222-ba58-77ff9157aea4	\N	f	12
272	2020-12-12 15:28:07.754198+00	2020-12-12 15:58:15.400922+00	1	Custo Atual	f	f	f	f	\N	\N		46	\N	1e3927e1-c925-4186-b3d2-95ec6bbd3c17	699	t	12
814	2021-01-28 19:50:04.083724+00	2021-01-29 18:19:59.956491+00	0	/\n	f	f	f	f	\N	\N		247	\N	58561d95-bd7b-48c5-bd20-60dd1966647f	\N	f	12
828	2021-01-29 18:00:07.340168+00	2021-01-29 18:20:00.344242+00	0	Plano I	f	f	f	f	\N	\N		214	\N	0cc3a0e6-9262-4c39-9419-d2b1635d2720	fieldVariable-695 fromConnectedField-	t	10
400	2020-12-13 15:03:21.779828+00	2021-01-29 18:20:00.808353+00	0	Comparativo - Plano Atual vs Novo Plano                                                                                                     \n	t	f	f	f	\N	#579cfc50	#0086c0	113	\N	526b21a8-833e-40cd-98cc-672e6d0fb9f2	\N	f	12
772	2021-01-28 13:11:49.281185+00	2021-01-29 18:20:00.926079+00	2	 	f	f	f	f	\N	\N		230	\N	43363e10-4921-46a5-be31-2d7f747aa22b	\N	f	10
773	2021-01-28 13:11:49.306399+00	2021-01-29 18:20:00.941014+00	0	R$ 	f	f	f	f	\N	\N		231	\N	2b193d9f-8c85-4985-a169-5af084c09521	\N	f	10
774	2021-01-28 13:11:49.314929+00	2021-01-29 18:20:00.945692+00	1	Valor do Negócio	f	f	f	f	\N	\N		231	\N	77871cf1-59ed-4f85-aacd-82cb3255c7f1	fieldVariable-698 fromConnectedField-	t	10
775	2021-01-28 13:11:49.322865+00	2021-01-29 18:20:00.950017+00	2	 	f	f	f	f	\N	\N		231	\N	cdcec448-72f6-42e6-91cd-03ccf5b4ed46	\N	f	10
776	2021-01-28 13:11:49.34765+00	2021-01-29 18:20:00.9658+00	0	R$ 	f	f	f	f	\N	\N		232	\N	da2d1a9d-9515-47a9-9f99-fedc5a2ed498	\N	f	10
777	2021-01-28 13:11:49.355949+00	2021-01-29 18:20:00.970255+00	1	Economia Mensal	f	f	f	f	\N	\N		232	\N	62816f35-949b-469e-8d4d-a0db6580cddd	fieldVariable-700 fromConnectedField-	t	10
290	2020-12-12 18:15:23.889927+00	2021-01-29 18:20:00.144286+00	0	A/C	t	f	f	f	\N	\N	#0086c0	78	\N	41814471-4f28-4c81-90ce-a44832245297	\N	f	12
659	2020-12-14 14:22:43.05167+00	2021-01-29 18:20:00.148803+00	1	: 	f	f	f	f	\N	\N		78	\N	2ca6826e-2cfd-4176-baed-23bd48bbb463	\N	f	12
660	2020-12-14 14:22:43.057818+00	2021-01-29 18:20:00.153075+00	2	Contato	f	f	f	f	\N	\N		78	\N	5b920281-9a6e-4476-bc47-efd5ab7d9c88	fieldVariable-718 fromConnectedField-679	t	12
45	2020-12-03 19:46:10.682504+00	2020-12-12 15:58:14.751254+00	0	Negociação: 	f	f	f	f	\N	\N		31	\N	3fdbf9f3-9878-44a5-a946-8bee2357c288	\N	f	12
46	2020-12-03 19:46:10.689174+00	2020-12-12 15:58:14.755866+00	1	Negociação	f	f	f	f	\N	\N		31	\N	37bf3e73-dcd0-484f-8298-cdddb0f77d59	693	t	12
47	2020-12-03 19:46:10.701595+00	2020-12-12 15:58:14.760497+00	2	 	f	f	f	f	\N	\N		31	\N	7d25d6a6-0893-4be8-aaa9-27299d5a17e0	\N	f	12
50	2020-12-03 19:46:10.768941+00	2020-12-12 15:58:14.790991+00	0	Seguem abaixo os detalhes do plano sugerido pela Consulting:	t	f	f	f	\N	\N		34	\N	e17018ee-491a-4938-8c86-758527c792c9	\N	f	12
275	2020-12-12 15:56:05.764381+00	2020-12-12 15:58:14.815829+00	2	 \n	f	f	f	f	\N	\N		35	\N	fa9ee873-0cb5-4f53-82d5-e4ce98b558c7	\N	f	12
185	2020-12-11 20:32:09.402509+00	2020-12-12 15:58:14.863538+00	1	Valor Unitário	f	f	f	f	\N	\N		51	\N	5ad02437-08ae-4c40-9973-0ed1638a9351	706	t	12
187	2020-12-11 20:32:09.415199+00	2020-12-12 15:58:14.872462+00	3	\n	t	f	f	f	\N	\N	#0086c0	51	\N	f172c9ae-8f6b-4d03-ae2e-e419a102f5ee	\N	f	12
188	2020-12-11 20:32:09.432083+00	2020-12-12 15:58:14.888162+00	0	Desconto: 	t	f	f	f	\N	\N	#0086c0	52	\N	e2db88be-fb5e-4873-8680-71f877c07476	\N	f	12
189	2020-12-11 20:32:09.438923+00	2020-12-12 15:58:14.892738+00	1	Desconto	f	f	f	f	\N	\N		52	\N	01433fc7-d184-4e10-802f-7a295654aeee	708	t	12
191	2020-12-11 20:39:54.450747+00	2020-12-12 15:58:14.908018+00	0	Total: 	t	f	f	f	\N	\N	#0086c0	39	\N	af2bd6bc-d422-40f6-84cd-b11f70869dbb	\N	f	12
207	2020-12-11 20:39:54.604919+00	2020-12-12 15:58:15.073464+00	0	Desconto:	t	f	f	f	\N	\N	#0086c0	57	\N	ce109267-b957-47a2-a58c-be7a375ff8e8	\N	f	12
208	2020-12-11 20:39:54.610879+00	2020-12-12 15:58:15.078141+00	1	 	f	f	f	f	\N	\N		57	\N	24e72f46-28ae-4877-9b0d-6efb5666fc99	\N	f	12
209	2020-12-11 20:39:54.616771+00	2020-12-12 15:58:15.082711+00	2	Desconto	f	f	f	f	\N	\N		57	\N	ba99d1cb-0ade-4d05-bf9b-420f9603e4c2	708	t	12
210	2020-12-11 20:39:54.622748+00	2020-12-12 15:58:15.087386+00	3	 	f	f	f	f	\N	\N		57	\N	a122aef2-025f-49c9-9336-8326a5f64463	\N	f	12
661	2020-12-14 14:22:43.06365+00	2021-01-29 18:20:00.157331+00	3	 \n	f	f	f	f	\N	\N		78	\N	fa448c77-8b96-4a66-965b-2c6e532beace	\N	f	12
294	2020-12-12 18:15:23.926626+00	2021-01-29 18:20:00.17219+00	0	Negociação:	t	f	f	f	\N	\N	#0086c0	79	\N	8fd81c5f-3f19-434d-9c27-e3c96e2a18e7	\N	f	12
575	2020-12-14 06:40:55.46316+00	2021-01-29 18:20:00.176602+00	1	 	f	f	f	f	\N	\N		79	\N	ddd30537-2206-4659-9796-1dbdc2564fb2	\N	f	12
576	2020-12-14 06:40:55.472062+00	2021-01-29 18:20:00.181398+00	2	Negociação	f	f	f	f	\N	\N		79	\N	d258f17b-5624-4a96-8add-834ef9c41349	fieldVariable-693 fromConnectedField-	t	12
577	2020-12-14 06:40:55.480756+00	2021-01-29 18:20:00.18585+00	3	 \n	f	f	f	f	\N	\N		79	\N	a92fc6c2-7f0f-4340-99e0-41a99111b26c	\N	f	12
298	2020-12-12 18:15:23.962378+00	2021-01-29 18:20:00.201195+00	0		f	f	f	f	\N	\N		80	\N	8a0c1590-9e33-4f0b-acd1-29b231d91deb	\N	f	12
211	2020-12-11 20:39:54.642343+00	2020-12-12 15:58:15.10273+00	0	Total:	t	f	f	f	\N	\N	#0086c0	58	\N	79dae228-6abe-41f9-96a5-af6df502f2a7	\N	f	12
212	2020-12-11 20:39:54.648315+00	2020-12-12 15:58:15.10713+00	1	 	f	f	f	f	\N	\N		58	\N	7b377c30-d56c-437c-b815-ac1059a68fcf	\N	f	12
221	2020-12-11 20:39:54.741336+00	2020-12-12 15:58:15.181881+00	1	 	t	f	f	f	\N	\N		61	\N	a37d8243-11e5-4c11-be7b-debdec9a6019	\N	f	12
222	2020-12-11 20:39:54.747396+00	2020-12-12 15:58:15.18641+00	2	Quantidade	f	f	f	f	\N	\N		61	\N	aa3efde2-b471-4b82-bc9b-f810c8969aca	705	t	12
223	2020-12-11 20:39:54.75337+00	2020-12-12 15:58:15.190917+00	3	 	f	f	f	f	\N	\N		61	\N	2a6f2c11-6f8a-414e-bbcb-9e6768301efd	\N	f	12
224	2020-12-11 20:39:54.771956+00	2020-12-12 15:58:15.206307+00	0	Valor Unitário: 	t	f	f	f	\N	\N	#0086c0	62	\N	a71ce469-51f6-4ddc-9a9f-a67c710797e0	\N	f	12
225	2020-12-11 20:39:54.777928+00	2020-12-12 15:58:15.211461+00	1	Valor Unitário	f	f	f	f	\N	\N		62	\N	606cfc42-5a1f-4c0f-ad83-d61a174c5353	706	t	12
226	2020-12-11 20:39:54.783839+00	2020-12-12 15:58:15.215972+00	2	 	f	f	f	f	\N	\N		62	\N	50fd9684-4fc2-448c-9963-5a09f11a169a	\N	f	12
227	2020-12-11 20:39:54.802066+00	2020-12-12 15:58:15.231783+00	0	Desconto: 	t	f	f	f	\N	\N	#0086c0	63	\N	785632dd-f6e1-4e82-9923-8df1deef1af9	\N	f	12
228	2020-12-11 20:39:54.808182+00	2020-12-12 15:58:15.236262+00	1	Desconto	f	f	f	f	\N	\N		63	\N	415cb7db-a02c-4e25-8300-a5add94491f8	708	t	12
229	2020-12-11 20:39:54.814217+00	2020-12-12 15:58:15.240893+00	2	 	f	f	f	f	\N	\N		63	\N	935a692c-3dde-414f-88de-ef235825eaee	\N	f	12
230	2020-12-11 20:39:54.832655+00	2020-12-12 15:58:15.256098+00	0	Total:	t	f	f	f	\N	\N	#0086c0	64	\N	8a281733-9cbc-4ba1-b2af-fba679cca1c9	\N	f	12
265	2020-12-11 20:46:25.172586+00	2020-12-12 15:58:15.331187+00	0	Benefícios	f	f	f	f	\N	\N		42	\N	9cb25c5b-99cc-46dc-b1f8-f9c803a12af4	703	t	12
273	2020-12-12 15:28:07.759995+00	2020-12-12 15:58:15.405338+00	2	 	f	f	f	f	\N	\N		46	\N	53dcb3b6-12ec-4903-ad15-6779d367cb41	\N	f	12
274	2020-12-12 15:28:07.767574+00	2020-12-12 15:58:15.409985+00	3	\n	t	f	f	f	\N	\N		46	\N	fb7f61a7-c765-4380-9448-d5ad1a030f09	\N	f	12
250	2020-12-11 20:39:55.154176+00	2020-12-12 15:58:15.488475+00	2	 	f	f	f	f	\N	\N		69	\N	351ee696-8e73-4ee5-87a9-636f692f35fc	\N	f	12
299	2020-12-12 18:15:23.980627+00	2021-01-29 18:20:00.216192+00	0	Seguem abaixo os detalhes  do plano sugerido pela Consulting:	t	f	f	f	\N	\N		81	\N	013b4b3e-251c-4ab9-9a5a-3902bbe4e9c4	\N	f	12
744	2021-01-28 13:11:48.507623+00	2021-01-29 18:20:00.231276+00	0	\n	f	f	f	f	\N	\N		142	\N	cc69d894-0b22-4c31-b1fa-b142c00cebf7	\N	f	12
745	2021-01-28 13:11:48.534547+00	2021-01-29 18:20:00.251254+00	0	/\n	f	f	f	f	\N	\N		84	\N	69214231-d16d-4db1-8197-d305976eeb53	\N	f	12
251	2020-12-11 20:39:55.15999+00	2020-12-12 15:58:15.493309+00	3	\n	t	f	f	f	\N	\N		69	\N	1ef0baa9-9698-4bbc-aaef-a78bd7b3dc22	\N	f	12
829	2021-01-29 18:00:07.351906+00	2021-01-29 18:20:00.349524+00	1	 	f	f	f	f	\N	\N		214	\N	befc8bf9-0642-43f6-b5c3-9227553d4d5b	\N	f	12
830	2021-01-29 18:00:07.394616+00	2021-01-29 18:20:00.365002+00	0	Quantidade	f	f	f	f	\N	\N		215	\N	686f8578-b37d-498a-b242-da3ecc159120	fieldVariable-722 fromConnectedField-695	t	10
778	2021-01-28 13:11:49.363995+00	2021-01-29 18:20:00.974563+00	2	 	f	f	f	f	\N	\N		232	\N	3c9bad31-f2d9-4bb2-aea4-fd8f2bcfb256	\N	f	10
880	2021-01-29 18:22:44.141716+00	2021-01-31 19:34:53.093611+00	0	/\n	f	f	f	f	\N	\N		259	\N	e452f1b9-b9ad-4e2b-97bb-5c9dad39ec4f	\N	f	12
881	2021-01-29 18:22:44.639121+00	2021-01-31 19:34:53.172982+00	0	/\n	f	f	f	f	\N	\N		260	\N	23946d06-e818-4d82-a34c-111aa05c6655	\N	f	12
892	2021-01-29 18:25:40.61365+00	2021-01-31 19:34:53.297273+00	1	 	f	f	f	f	\N	\N		268	\N	043e8168-4aec-4830-b60f-0c9b6d80257a	\N	f	12
203	2020-12-11 20:39:54.569894+00	2020-12-12 15:58:15.043961+00	0	Valor Unitário:	t	f	f	f	\N	\N	#0086c0	56	\N	12338223-8455-40c7-b4b5-4a11d59d64b7	\N	f	12
790	2021-01-28 14:42:49.585566+00	2021-01-29 18:19:59.587531+00	0	Proposta Comercial 	t	f	f	f	\N	\N	#0086c0	170	\N	51270a11-92f0-41c5-b1df-a26be54950f0	\N	f	48
204	2020-12-11 20:39:54.575622+00	2020-12-12 15:58:15.04846+00	1	 	f	f	f	f	\N	\N		56	\N	6ee709bd-c4e8-47d5-a98a-79dd714752bb	\N	f	12
205	2020-12-11 20:39:54.581377+00	2020-12-12 15:58:15.053227+00	2	Valor Unitário	f	f	f	f	\N	\N		56	\N	bec2b3ed-79c7-4094-aa78-e96be36c97de	706	t	12
206	2020-12-11 20:39:54.587114+00	2020-12-12 15:58:15.057943+00	3	 	f	f	f	f	\N	\N		56	\N	7a3d354d-1f07-4c38-bb31-f3c2b58a0126	\N	f	12
791	2021-01-28 14:42:49.633615+00	2021-01-29 18:19:59.618199+00	0	Cliente	t	f	f	f	\N	\N	#bfbfbf	146	\N	088ba68b-a75b-4195-822a-1b151d7f3c15	fieldVariable-679 fromConnectedField-	t	20
550	2020-12-13 21:01:18.223524+00	2021-01-29 18:19:59.847684+00	0	/\n	f	f	f	f	\N	\N		149	\N	c1a0511e-923e-4cdd-a156-2e5f5b1335db	\N	f	12
831	2021-01-29 18:00:07.403155+00	2021-01-29 18:20:00.36958+00	1	 	f	f	f	f	\N	\N		215	\N	739aca41-f106-4811-9330-eb407c9ca46e	\N	f	12
213	2020-12-11 20:39:54.654538+00	2020-12-12 15:58:15.111752+00	2	Total	f	f	f	f	\N	\N		58	\N	57234687-fe6d-4eb0-9c8a-b97cfb20b7a7	709	t	12
214	2020-12-11 20:39:54.660416+00	2020-12-12 15:58:15.116219+00	3	 	f	f	f	f	\N	\N		58	\N	60f4ddc1-6050-40e2-8090-0cb34493301c	\N	f	12
215	2020-12-11 20:39:54.67872+00	2020-12-12 15:58:15.131634+00	0		f	f	f	f	\N	\N		59	\N	b0f4f648-d596-4eaa-9dc2-1a22a698c046	\N	f	12
216	2020-12-11 20:39:54.697561+00	2020-12-12 15:58:15.148379+00	0	Plano III:	t	f	f	f	\N	\N	#0086c0	60	\N	9519cd7f-a3c8-4d6a-90ec-4ee28b4b27f6	\N	f	12
217	2020-12-11 20:39:54.703394+00	2020-12-12 15:58:15.15321+00	1	 	f	f	f	f	\N	\N		60	\N	8280e5a1-7b8e-4226-8fb0-dc147157d4e6	\N	f	12
218	2020-12-11 20:39:54.709187+00	2020-12-12 15:58:15.157655+00	2	Plano III	f	f	f	f	\N	\N		60	\N	a2a1babc-cee9-430b-a8b1-dd4813f0ba2e	697	t	12
219	2020-12-11 20:39:54.715165+00	2020-12-12 15:58:15.162076+00	3	 	f	f	f	f	\N	\N		60	\N	335d2ce8-d568-4498-9800-3e5a909d8015	\N	f	12
220	2020-12-11 20:39:54.735359+00	2020-12-12 15:58:15.177293+00	0	Quantidade:	t	f	f	f	\N	\N	#0086c0	61	\N	fc22d5e2-e768-4220-b7d6-4a112ddcb1bb	\N	f	12
231	2020-12-11 20:39:54.838944+00	2020-12-12 15:58:15.260529+00	1	 	f	f	f	f	\N	\N		64	\N	862fd51d-7c51-4d25-9e64-d9ee90c3538a	\N	f	12
232	2020-12-11 20:39:54.845433+00	2020-12-12 15:58:15.265028+00	2	Desconto	f	f	f	f	\N	\N		64	\N	6cf8aa66-31f2-4bc6-b00d-225c0093083a	708	t	12
233	2020-12-11 20:39:54.851494+00	2020-12-12 15:58:15.269496+00	3	 	f	f	f	f	\N	\N		64	\N	8aafd1d3-14ae-4687-bde2-1204e66561f1	\N	f	12
234	2020-12-11 20:39:54.870889+00	2020-12-12 15:58:15.284887+00	0		f	f	f	f	\N	\N		65	\N	d766867b-2db6-4ab2-a4be-3d26c0344346	\N	f	12
235	2020-12-11 20:39:54.889669+00	2020-12-12 15:58:15.300444+00	0		f	f	f	f	\N	\N		66	\N	d136c09d-6d37-4ba0-be4f-c82d97dddb70	\N	f	12
832	2021-01-29 18:00:07.445559+00	2021-01-29 18:20:00.385724+00	0	R$ 	f	f	f	f	\N	\N		216	\N	226ea9d7-2300-4aea-a257-3ef7e865f48c	\N	f	10
833	2021-01-29 18:00:07.470062+00	2021-01-29 18:20:00.390256+00	1	Valor Unitário	f	f	f	f	\N	\N		216	\N	8059f4f6-d788-4472-854e-25bb17491c35	fieldVariable-723 fromConnectedField-695	t	10
834	2021-01-29 18:00:07.485227+00	2021-01-29 18:20:00.394812+00	2	 	f	f	f	f	\N	\N		216	\N	ad3902db-5325-4027-8243-46a57d61030c	\N	f	10
835	2021-01-29 18:00:07.555947+00	2021-01-29 18:20:00.410083+00	0	R$ 	f	f	f	f	\N	\N		217	\N	f9fe8224-3628-418e-a36e-4bdb9d3ca187	\N	f	10
836	2021-01-29 18:00:07.585178+00	2021-01-29 18:20:00.414717+00	1	Desconto	f	f	f	f	\N	\N		217	\N	d8cf6d5a-7c96-4aa8-bf95-b1d167532e4d	fieldVariable-724 fromConnectedField-695	t	10
837	2021-01-29 18:00:07.614577+00	2021-01-29 18:20:00.419235+00	2	 	f	f	f	f	\N	\N		217	\N	20cf190b-9c30-450c-9a60-f46a6fe14675	\N	f	12
101	2020-12-03 19:57:09.383669+00	2020-12-12 15:58:15.316041+00	0	Benefícios do Plano                                                                                                                \n	t	f	f	f	\N	#579cfc50	#0086c0	41	\N	eb621e97-46ed-4d22-a5f4-e9e2d4963065	\N	f	12
240	2020-12-11 20:39:55.068454+00	2020-12-12 15:58:15.425+00	0	Custo Sugerido: 	t	f	f	f	\N	\N		67	\N	cf8f0407-b221-4a1d-8bf1-aedfd470503a	\N	f	12
241	2020-12-11 20:39:55.074236+00	2020-12-12 15:58:15.429506+00	1	Valor do Negócio	f	f	f	f	\N	\N		67	\N	759092ee-18c7-49b8-806f-17ac94abc800	698	t	12
242	2020-12-11 20:39:55.080041+00	2020-12-12 15:58:15.434038+00	2	 	f	f	f	f	\N	\N		67	\N	3b10e1b4-03e7-448f-893d-70d7abc7ecdd	\N	f	12
243	2020-12-11 20:39:55.086012+00	2020-12-12 15:58:15.439053+00	3	\n	t	f	f	f	\N	\N		67	\N	c46640f4-7264-45d9-a770-1e07789d5415	\N	f	12
244	2020-12-11 20:39:55.10442+00	2020-12-12 15:58:15.45443+00	0	Economia Mensal: 	t	f	f	f	\N	\N		68	\N	f42e3595-5656-4560-a048-9cd357c1f6cd	\N	f	12
245	2020-12-11 20:39:55.110166+00	2020-12-12 15:58:15.45886+00	1	Economia Mensal	f	f	f	f	\N	\N		68	\N	541e96f1-2600-44f4-9122-7a17521dca8c	700	t	12
246	2020-12-11 20:39:55.115994+00	2020-12-12 15:58:15.463263+00	2	 \n	f	f	f	f	\N	\N		68	\N	d61a6978-c2f4-4e5f-9f3f-04bbe0d15115	\N	f	12
248	2020-12-11 20:39:55.142066+00	2020-12-12 15:58:15.479333+00	0	Economia Anual: 	t	f	f	f	\N	\N		69	\N	b9466bc8-807a-410a-a2da-2400ba8c685c	\N	f	12
249	2020-12-11 20:39:55.148037+00	2020-12-12 15:58:15.483882+00	1	Economia Anual	f	f	f	f	\N	\N		69	\N	97cb7be4-be52-4713-9fb5-293b5ae3cd61	701	t	12
922	2021-01-31 19:11:54.93455+00	2021-01-31 19:34:53.595597+00	1	 	f	f	f	f	\N	\N		289	\N	178f5537-205e-48de-b165-a17b5fc6412c	\N	f	12
252	2020-12-11 20:41:34.916296+00	2020-12-12 15:58:14.705738+00	0	Cliente	f	f	f	f	\N	\N		28	\N	bd9aad48-0c9b-4b76-a339-648bb5d134ff	679	t	12
253	2020-12-11 20:41:34.922583+00	2020-12-12 15:58:14.711121+00	1	  \n	f	f	f	f	\N	\N		28	\N	18e8fb4a-011f-4502-9a9f-fab5ab4a43bc	\N	f	12
254	2020-12-11 20:41:34.938832+00	2020-12-12 15:58:14.7268+00	0	A/C: 	f	f	f	f	\N	\N		29	\N	60fb81a1-5e35-4491-bdcc-08a1359c60de	\N	f	12
255	2020-12-11 20:41:34.944421+00	2020-12-12 15:58:14.731407+00	1	Cliente	f	f	f	f	\N	\N		29	\N	6a5ea024-d899-4062-beb0-27dad308db4d	679	t	12
256	2020-12-11 20:41:34.949883+00	2020-12-12 15:58:14.735875+00	2	 \n	f	f	f	f	\N	\N		29	\N	17669dbf-c000-4df1-9667-1f19398a0675	\N	f	12
192	2020-12-11 20:39:54.456784+00	2020-12-12 15:58:14.912726+00	1	Total	f	f	f	f	\N	\N		39	\N	4d9e6201-8608-4fbc-aa9a-b8f373844133	709	t	12
193	2020-12-11 20:39:54.462703+00	2020-12-12 15:58:14.917272+00	2	 	f	f	f	f	\N	\N		39	\N	899e73c1-84be-405d-90f4-1896412e5144	\N	f	12
194	2020-12-11 20:39:54.468565+00	2020-12-12 15:58:14.921743+00	3	\n	t	f	f	f	\N	\N	#0086c0	39	\N	fc59b774-f7f0-4287-a331-7d27d55b9e13	\N	f	12
195	2020-12-11 20:39:54.485688+00	2020-12-12 15:58:14.937024+00	0		f	f	f	f	\N	\N		40	\N	10b886d9-54f8-4601-82d9-b83f8b1fb94c	\N	f	12
196	2020-12-11 20:39:54.503734+00	2020-12-12 15:58:14.952439+00	0	Plano II: 	t	f	f	f	\N	\N	#0086c0	54	\N	999358cf-67e3-46ba-b606-736619c83852	\N	f	12
197	2020-12-11 20:39:54.510101+00	2020-12-12 15:58:14.956948+00	1	Plano II	f	f	f	f	\N	\N		54	\N	981af104-a503-4225-b172-7bf303b07a48	696	t	12
198	2020-12-11 20:39:54.516169+00	2020-12-12 15:58:14.961667+00	2	 	f	f	f	f	\N	\N		54	\N	e499537b-0b27-4100-925c-b0435bf26fd1	\N	f	12
199	2020-12-11 20:39:54.534537+00	2020-12-12 15:58:14.97961+00	0	Quantidade:	t	f	f	f	\N	\N	#0086c0	55	\N	a334c6b2-ab2f-4e23-9d3b-b241c20c4a34	\N	f	12
200	2020-12-11 20:39:54.540247+00	2020-12-12 15:58:14.986168+00	1	 	f	f	f	f	\N	\N		55	\N	6251a2d4-a7ab-4168-bcd9-41b0102a12a3	\N	f	12
201	2020-12-11 20:39:54.546061+00	2020-12-12 15:58:14.990766+00	2	Quantidade	f	f	f	f	\N	\N		55	\N	96b1b772-abc7-4a37-8c6d-91fd51947dc3	705	t	12
202	2020-12-11 20:39:54.5519+00	2020-12-12 15:58:14.995191+00	3	 	f	f	f	f	\N	\N		55	\N	d5f55d19-b102-44e2-82b9-a59e4eac42bf	\N	f	12
730	2021-01-28 13:11:46.70162+00	2021-01-29 18:19:59.441783+00	0	/\n	f	f	f	f	\N	\N		71	\N	b68ae4db-f704-416e-aa96-ca86f7d2b5d1	\N	f	12
967	2021-01-31 19:16:29.882257+00	2021-01-31 19:34:53.962272+00	0	Valor Unitário	f	f	f	f	\N	\N		307	\N	ccb55f53-1e2f-4353-8e81-6404cdbd052b	fieldVariable-723 fromConnectedField-726	t	10
731	2021-01-28 13:11:47.255704+00	2021-01-29 18:19:59.521023+00	0	/\n	f	f	f	f	\N	\N		204	\N	15a7bfed-f3dc-4733-b9ae-93867b89442b	\N	f	12
968	2021-01-31 19:16:29.887924+00	2021-01-31 19:34:53.967066+00	1	 	f	f	f	f	\N	\N		307	\N	bb1976c7-d92d-400f-b1c9-afb52e849ba1	\N	f	12
732	2021-01-28 13:11:47.285259+00	2021-01-29 18:19:59.537821+00	0		f	f	f	f	\N	\N		205	\N	818c8843-2a4d-4bbd-8fa3-d0268ca59b90	\N	f	12
733	2021-01-28 13:11:47.311632+00	2021-01-29 18:19:59.554865+00	0		f	f	f	f	\N	\N		206	\N	8f9a80bb-3af9-417b-bea1-b664e37991d5	\N	f	12
734	2021-01-28 13:11:47.337867+00	2021-01-29 18:19:59.571058+00	0		f	f	f	f	\N	\N		207	\N	3ad44ced-c9e3-40ef-b6c5-3ddb307044e0	\N	f	12
737	2021-01-28 13:11:47.437592+00	2021-01-29 18:19:59.622536+00	1	 	f	f	f	f	\N	\N	#bfbfbf	146	\N	1ddfad83-ffe4-479b-8f3a-7c8aea5ab6f4	\N	f	12
738	2021-01-28 13:11:47.461323+00	2021-01-29 18:19:59.637538+00	0	10.234.902/0001-92	t	f	f	f	\N	\N	#bfbfbf	147	\N	93687796-560e-4bed-9327-133f2475d968	\N	f	18
739	2021-01-28 13:11:47.469794+00	2021-01-29 18:19:59.641917+00	1		f	f	f	f	\N	\N		147	\N	e182a545-2806-4715-ac9d-ab309fdd7ab4	\N	f	12
822	2021-01-28 19:53:10.126535+00	2021-01-29 18:19:59.99795+00	0	Data da Proposta: 	t	f	f	f	\N	\N	#0086c0	74	\N	ba1b39b9-6c14-4871-b449-78d88e07ffdd	\N	f	12
823	2021-01-28 19:53:10.135169+00	2021-01-29 18:20:00.054348+00	1	Data de Atualização	t	f	f	f	\N	\N	#0086c0	74	\N	22994e31-0c58-4790-b6f6-eb46a982eb29	fieldVariable-691 fromConnectedField-	t	12
824	2021-01-28 19:53:10.145659+00	2021-01-29 18:20:00.060152+00	2	     	t	f	f	f	\N	\N	#0086c0	74	\N	dc190443-51a9-4d62-95f4-6a6548d92c6e	\N	f	12
825	2021-01-28 19:53:10.154313+00	2021-01-29 18:20:00.064751+00	3	                                                                                                	f	f	f	f	\N	\N	#0086c0	74	\N	9a58fa90-0a66-4aff-8f4c-9d4a6217723e	\N	f	12
838	2021-01-29 18:00:07.689145+00	2021-01-29 18:20:00.434232+00	0	R$ 	f	f	f	f	\N	\N		218	\N	511a3491-02ec-4d70-a9b1-085fa9f6c7b0	\N	f	10
839	2021-01-29 18:00:07.703727+00	2021-01-29 18:20:00.438727+00	1	Total	f	f	f	f	\N	\N		218	\N	8eca5ad3-3a73-489e-ba43-b4371d912cbe	fieldVariable-725 fromConnectedField-695	t	10
840	2021-01-29 18:00:07.719401+00	2021-01-29 18:20:00.443065+00	2	 	f	f	f	f	\N	\N		218	\N	4160849a-ca5f-4e70-a6a7-bf7926f9486a	\N	f	12
842	2021-01-29 18:00:07.792939+00	2021-01-29 18:20:00.462534+00	1	 	f	f	f	f	\N	\N		219	\N	42e2c9fd-2d62-4845-9d08-7e3ce9f0cc4b	\N	f	12
969	2021-01-31 19:16:29.905045+00	2021-01-31 19:34:53.982583+00	0	Desconto	f	f	f	f	\N	\N		308	\N	fd164850-08d7-45fc-8dd8-224701ffe489	fieldVariable-724 fromConnectedField-726	t	10
970	2021-01-31 19:16:29.910969+00	2021-01-31 19:34:53.987001+00	1	 	f	f	f	f	\N	\N		308	\N	ff46a4eb-97d9-41d9-90ed-e176026f9cd9	\N	f	12
971	2021-01-31 19:16:29.92847+00	2021-01-31 19:34:54.005833+00	0	Total	f	f	f	f	\N	\N		309	\N	ddcbad23-bd7f-4b81-9bd2-5f6f088794e2	fieldVariable-725 fromConnectedField-726	t	10
972	2021-01-31 19:16:29.93435+00	2021-01-31 19:34:54.010902+00	1	 	f	f	f	f	\N	\N		309	\N	f1f79736-c5d2-4259-a255-df3fd1d3b332	\N	f	12
977	2021-01-31 19:18:54.323764+00	2021-01-31 19:34:54.069724+00	0	Valor Unitário	f	f	f	f	\N	\N		312	\N	a8c4815a-a207-40ee-98a7-600df3513863	fieldVariable-723 fromConnectedField-727	t	10
978	2021-01-31 19:18:54.329713+00	2021-01-31 19:34:54.074077+00	1	 	f	f	f	f	\N	\N		312	\N	2d2ec488-4dd8-48ac-8bc5-5d555254849c	\N	f	12
979	2021-01-31 19:18:54.346741+00	2021-01-31 19:34:54.089228+00	0	Desconto	f	f	f	f	\N	\N		313	\N	f5900ee0-d340-4526-8d73-52171724bd8d	fieldVariable-724 fromConnectedField-727	t	10
980	2021-01-31 19:18:54.352589+00	2021-01-31 19:34:54.093829+00	1	 	f	f	f	f	\N	\N		313	\N	e8a69984-a1a4-4ef2-8ee6-f5c0564fe71e	\N	f	12
981	2021-01-31 19:18:54.368936+00	2021-01-31 19:34:54.109506+00	0	Total	f	f	f	f	\N	\N		314	\N	a16b1c01-412a-46ff-b96b-89d1a9cec03b	fieldVariable-725 fromConnectedField-727	t	10
808	2021-01-28 15:34:00.74497+00	2021-01-29 18:19:59.972241+00	0		f	f	f	f	\N	\N		245	\N	f40a3769-2e82-4cc7-98e1-39ccc761ac5b	\N	f	12
809	2021-01-28 15:34:00.752903+00	2021-01-29 18:19:59.977107+00	1		t	f	f	f	\N	\N	#0086c0	245	\N	6f919bd5-8cd6-49a2-85e5-ca88eb74274a	\N	f	51
810	2021-01-28 15:34:00.761128+00	2021-01-29 18:19:59.981543+00	2		f	f	f	f	\N	\N		245	\N	71b54b57-36d0-4f4c-b3c0-3275c28ff784	\N	f	12
686	2020-12-14 14:43:26.073743+00	2021-01-29 18:20:00.08028+00	0		f	f	f	f	\N	\N	#444444	183	\N	4efa59ff-d702-4dbd-a767-248317125c37	\N	f	12
687	2020-12-14 14:43:26.079193+00	2021-01-29 18:20:00.084898+00	1	Número da Proposta: 	t	f	f	f	\N	\N		183	\N	ada14291-d28e-4eac-975a-113815d03a74	\N	f	12
688	2020-12-14 14:43:26.088426+00	2021-01-29 18:20:00.089503+00	2	Id do Negócio	f	f	f	f	\N	\N		183	\N	28fc6fbd-f632-4d53-bea3-f8eb1aef8f9b	fieldVariable-694 fromConnectedField-	t	12
689	2020-12-14 14:43:26.094031+00	2021-01-29 18:20:00.09411+00	3	 	f	f	f	f	\N	\N		183	\N	8a607cfd-6f69-4320-b9df-5c4c24c9e98e	\N	f	12
287	2020-12-12 18:15:23.848278+00	2021-01-29 18:20:00.109692+00	0		f	f	f	f	\N	\N		76	\N	fa8f29a9-14f0-450a-9f6c-d3c627cade26	\N	f	12
690	2020-12-14 14:43:26.127728+00	2021-01-29 18:20:00.125038+00	0	Nome do Cliente	t	f	f	f	\N	\N		77	\N	2e5e1ea8-4745-43b6-a964-ab43cc2b3221	fieldVariable-678 fromConnectedField-679	t	12
691	2020-12-14 14:43:26.133502+00	2021-01-29 18:20:00.12944+00	1	 	t	f	f	f	\N	\N		77	\N	10e16ca7-77c1-4c6a-851e-54c0350e3041	\N	f	12
792	2021-01-28 14:44:25.755026+00	2021-01-29 18:20:00.266897+00	0	Plano	t	f	f	f	\N	\N	#0086c0	209	\N	a6e03faf-3351-40b0-82b7-7f1047386af3	\N	f	10
793	2021-01-28 14:44:25.778357+00	2021-01-29 18:20:00.282414+00	0	Quantidade	t	f	f	f	\N	\N	#0086c0	210	\N	5bd4f052-986d-425a-9581-1aebccf0416d	\N	f	10
794	2021-01-28 14:44:25.801339+00	2021-01-29 18:20:00.297861+00	0	Valor Unitário	t	f	f	f	\N	\N	#0086c0	211	\N	622fa114-f03e-49ec-a101-ec49130a0ea3	\N	f	10
795	2021-01-28 14:44:25.825344+00	2021-01-29 18:20:00.313322+00	0	Desconto	t	f	f	f	\N	\N	#0086c0	212	\N	3c035455-e13d-40c9-8630-afac7d474fab	\N	f	10
796	2021-01-28 14:44:25.848308+00	2021-01-29 18:20:00.328587+00	0	Total	t	f	f	f	\N	\N	#0086c0	213	\N	2a74ec00-322e-41c7-8ace-2252599ca69d	\N	f	10
866	2021-01-29 18:06:20.229385+00	2021-01-29 18:20:00.67674+00	0		f	f	f	f	\N	\N		254	\N	dc41fbde-406c-4f09-a970-41fcc2909c43	\N	f	12
867	2021-01-29 18:06:20.247481+00	2021-01-29 18:20:00.692499+00	0		f	f	f	f	\N	\N		255	\N	92edd554-af7f-4de1-a9cc-7efa86bdc104	\N	f	12
868	2021-01-29 18:06:20.264947+00	2021-01-29 18:20:00.70798+00	0		f	f	f	f	\N	\N		256	\N	b8c26d50-c2e2-44b3-9821-83b120534db0	\N	f	12
764	2021-01-28 13:11:49.111511+00	2021-01-29 18:20:00.826279+00	0	/\n	f	f	f	f	\N	\N		114	\N	8c98d26d-7a6a-4c5f-9a39-e9a7db62770d	\N	f	12
765	2021-01-28 13:11:49.136805+00	2021-01-29 18:20:00.841861+00	0	Custo Atual	t	f	f	f	\N	\N	#0086c0	225	\N	d90c2dc4-0499-4549-860a-aa8a482619be	\N	f	10
766	2021-01-28 13:11:49.162564+00	2021-01-29 18:20:00.857157+00	0	Custo Sugerido	t	f	f	f	\N	\N	#0086c0	226	\N	1e56e730-5b53-42ad-bb05-d5b1bb57776d	\N	f	10
767	2021-01-28 13:11:49.188081+00	2021-01-29 18:20:00.871919+00	0	Economia Mensal	t	f	f	f	\N	\N	#0086c0	227	\N	2281c0e3-00c4-402a-a30c-58bf42cbd73f	\N	f	10
768	2021-01-28 13:11:49.213206+00	2021-01-29 18:20:00.886898+00	0	Economia Anual	t	f	f	f	\N	\N	#0086c0	228	\N	1e025153-67cd-4774-98af-2944b204293a	\N	f	10
769	2021-01-28 13:11:49.237947+00	2021-01-29 18:20:00.901733+00	0	Redução	t	f	f	f	\N	\N	#0086c0	229	\N	6feac0bd-6af1-448d-8291-9a9babf8ae52	\N	f	10
770	2021-01-28 13:11:49.263967+00	2021-01-29 18:20:00.916904+00	0	R$ 	f	f	f	f	\N	\N		230	\N	2b0ba0a8-b99f-48e8-aa97-61e219e3b510	\N	f	10
771	2021-01-28 13:11:49.272416+00	2021-01-29 18:20:00.921551+00	1	Custo Atual	f	f	f	f	\N	\N		230	\N	c95762f3-3a28-4607-aee5-442591819caa	fieldVariable-699 fromConnectedField-	t	10
820	2021-01-28 19:50:05.275845+00	2021-01-29 18:20:01.01435+00	0	Percentual de Redução	t	f	f	f	\N	\N	#0dbf7e	234	\N	85d342a7-e730-411f-a6df-3ddf72ec9fd9	fieldVariable-702 fromConnectedField-	t	10
882	2021-01-29 18:22:44.65647+00	2021-01-31 19:34:53.189524+00	0		f	f	f	f	\N	\N		261	\N	0c95630d-a8dd-4aec-a348-ae13e36efd8c	\N	f	12
965	2021-01-31 19:16:29.85903+00	2021-01-31 19:34:53.941586+00	0	Quantidade	f	f	f	f	\N	\N		306	\N	ff48b98c-9631-4b4e-b327-b7b5bd047689	fieldVariable-722 fromConnectedField-726	t	10
966	2021-01-31 19:16:29.864721+00	2021-01-31 19:34:53.946362+00	1	 	f	f	f	f	\N	\N		306	\N	ab7cb408-1066-4eea-96b4-7ee7bf27c4b6	\N	f	12
973	2021-01-31 19:18:54.277833+00	2021-01-31 19:34:54.026777+00	0	Plano III	f	f	f	f	\N	\N		310	\N	5f07e91c-5151-4ef1-94a4-c4a917252f54	fieldVariable-727 fromConnectedField-	t	10
974	2021-01-31 19:18:54.283496+00	2021-01-31 19:34:54.031292+00	1	 	f	f	f	f	\N	\N		310	\N	630c09ba-197b-4abe-818a-a43820436850	\N	f	12
1016	2021-01-31 19:34:54.048019+00	2021-01-31 19:34:54.04804+00	0	Quantidade	f	f	f	f	\N	\N		311	\N	470a0d91-6449-4ed4-b6d7-d67c3b1eeeb5	fieldVariable-722 fromConnectedField-727	t	10
1017	2021-01-31 19:34:54.054124+00	2021-01-31 19:34:54.054144+00	1	  	f	f	f	f	\N	\N		311	\N	9fa30ad4-dc2d-4a66-b2f9-317683afd865	\N	f	12
982	2021-01-31 19:18:54.374443+00	2021-01-31 19:34:54.114071+00	1	 	f	f	f	f	\N	\N		314	\N	bb254cb6-37d5-44b0-9ca7-85b4db45896b	\N	f	12
913	2021-01-29 18:27:43.67066+00	2021-01-31 19:34:54.12928+00	0		f	f	f	f	\N	\N		282	\N	3aea0219-33f2-40ba-943e-e66de1509039	\N	f	12
983	2021-01-31 19:26:53.708623+00	2021-01-31 19:34:54.144418+00	0	Benefícios do Plano                                                                                                                                     \n	t	f	f	f	\N	#579cfc50	#0086c0	283	\N	da8a59d0-6279-4aaf-a716-749fa535a9e2	\N	f	12
984	2021-01-31 19:26:53.7253+00	2021-01-31 19:34:54.160179+00	0	Benefícios	f	f	f	f	\N	\N		284	\N	d342d894-2cb6-40ae-b332-b2e4cf95a286	fieldVariable-703 fromConnectedField-	t	12
985	2021-01-31 19:26:53.730888+00	2021-01-31 19:34:54.164776+00	1	 \n	f	f	f	f	\N	\N		284	\N	e486c568-239a-45d8-afc3-5bcd49a35c22	\N	f	12
986	2021-01-31 19:26:53.747174+00	2021-01-31 19:34:54.181063+00	0		f	f	f	f	\N	\N		285	\N	26a6f723-ebf5-48d6-9041-412361cbd383	\N	f	12
987	2021-01-31 19:26:53.764913+00	2021-01-31 19:34:54.198441+00	0	Comparativo - Plano Atual vs Novo Plano                                                                                                \n	t	f	f	f	\N	#579cfc50	#0086c0	315	\N	ea909fc2-10f1-4463-8601-b779fcb08869	\N	f	12
988	2021-01-31 19:26:53.782473+00	2021-01-31 19:34:54.216763+00	0	/\n	f	f	f	f	\N	\N		316	\N	f5659d45-644f-4530-98e8-40e0d3ec7de9	\N	f	12
989	2021-01-31 19:30:35.347977+00	2021-01-31 19:34:54.23309+00	0	Custo Atual	t	f	f	f	\N	\N	#0086c0	317	\N	95dd4140-9ff3-46eb-9cfa-10902849612f	\N	f	10
990	2021-01-31 19:30:35.365386+00	2021-01-31 19:34:54.24932+00	0	Custo Sugerido	t	f	f	f	\N	\N	#0086c0	318	\N	6e57e792-98dc-4a3e-8f5e-0bfa457c8adb	\N	f	10
991	2021-01-31 19:30:35.382428+00	2021-01-31 19:34:54.265325+00	0	Economia Mensal	t	f	f	f	\N	\N	#0086c0	319	\N	b171711a-b4ce-4404-a5e1-922c7aa62d7d	\N	f	10
992	2021-01-31 19:30:35.400741+00	2021-01-31 19:34:54.280398+00	0	Economia Anual	t	f	f	f	\N	\N	#0086c0	320	\N	29377520-4f1c-472d-b82f-42937cae3d80	\N	f	10
993	2021-01-31 19:30:35.418776+00	2021-01-31 19:34:54.295812+00	0	Redução	t	f	f	f	\N	\N	#0086c0	321	\N	ae45dcec-2332-479e-aef7-2fc5cc67bcf8	\N	f	10
994	2021-01-31 19:30:35.439149+00	2021-01-31 19:34:54.311904+00	0	Custo Atual	f	f	f	f	\N	\N		322	\N	ff860711-03b2-43f6-9c6f-6ecc9c624781	fieldVariable-699 fromConnectedField-	t	10
995	2021-01-31 19:30:35.445027+00	2021-01-31 19:34:54.316531+00	1	 	f	f	f	f	\N	\N		322	\N	d7e80cb4-8592-4ed5-a65d-8585e6cf1c99	\N	f	12
1009	2021-01-31 19:33:12.129806+00	2021-01-31 19:34:54.597403+00	0		f	f	f	f	\N	\N		330	\N	70efef24-e7fd-412a-9361-feab2df687d8	\N	f	12
841	2021-01-29 18:00:07.773978+00	2021-01-29 18:20:00.458108+00	0	Plano II	f	f	f	f	\N	\N		219	\N	d557d569-2426-40fc-9e58-381471d11d6a	fieldVariable-726 fromConnectedField-	t	10
843	2021-01-29 18:00:07.85874+00	2021-01-29 18:20:00.477973+00	0	Quantidade	f	f	f	f	\N	\N		220	\N	83d06ee9-9391-4b89-a3cb-fd35d2b3e68d	fieldVariable-722 fromConnectedField-726	t	10
844	2021-01-29 18:00:07.880963+00	2021-01-29 18:20:00.482445+00	1	 	f	f	f	f	\N	\N		220	\N	8863f3d7-09af-4305-ac48-ce41d8448d8e	\N	f	12
845	2021-01-29 18:00:07.946001+00	2021-01-29 18:20:00.499342+00	0	R$ 	f	f	f	f	\N	\N		221	\N	4463cbb8-1976-4fad-86ff-c8b432ee6dba	\N	f	10
846	2021-01-29 18:00:07.96403+00	2021-01-29 18:20:00.503883+00	1	Valor Unitário	f	f	f	f	\N	\N		221	\N	6173b962-2a4c-47a5-8fac-e93480b1c171	fieldVariable-723 fromConnectedField-726	t	10
847	2021-01-29 18:00:07.982596+00	2021-01-29 18:20:00.508288+00	2	 	f	f	f	f	\N	\N		221	\N	e6ea9635-2855-4ac8-9607-e75f4baf85bc	\N	f	10
848	2021-01-29 18:00:08.043037+00	2021-01-29 18:20:00.523719+00	0	R$ 	f	f	f	f	\N	\N		222	\N	cd5f6c21-1fa9-4da5-8656-fc623bb17d43	\N	f	10
849	2021-01-29 18:00:08.061448+00	2021-01-29 18:20:00.528386+00	1	Desconto	f	f	f	f	\N	\N		222	\N	43a3dbe9-ef7b-4760-a0b7-5826108e587e	fieldVariable-724 fromConnectedField-726	t	10
850	2021-01-29 18:00:08.080916+00	2021-01-29 18:20:00.532916+00	2	 	f	f	f	f	\N	\N		222	\N	19df7fb4-4e79-438e-9ef9-016138279b34	\N	f	10
857	2021-01-29 18:06:20.093098+00	2021-01-29 18:20:00.548881+00	0	R$ 	f	f	f	f	\N	\N		223	\N	87a77b75-85b2-4c66-abdf-789e21f4814f	\N	f	10
858	2021-01-29 18:06:20.098739+00	2021-01-29 18:20:00.553389+00	1	Total	f	f	f	f	\N	\N		223	\N	3a124584-3f37-4a8b-a052-f10901f99c80	fieldVariable-725 fromConnectedField-726	t	10
859	2021-01-29 18:06:20.104113+00	2021-01-29 18:20:00.557932+00	2	 	f	f	f	f	\N	\N		223	\N	7a110579-b64c-4b63-a995-bc525e45945f	\N	f	12
874	2021-01-29 18:07:28.088743+00	2021-01-29 18:20:00.575524+00	0	/\n	f	f	f	f	\N	\N		86	\N	0525357e-cd10-4576-816c-4c09dcdca936	\N	f	12
861	2021-01-29 18:06:20.141488+00	2021-01-29 18:20:00.591319+00	0		f	f	f	f	\N	\N		249	\N	0dd8ec27-7afa-4321-af33-ed65e3cd5fae	\N	f	12
862	2021-01-29 18:06:20.158619+00	2021-01-29 18:20:00.606299+00	0		f	f	f	f	\N	\N		250	\N	d59a484f-cad2-4925-831b-f97ab49a8ab8	\N	f	12
863	2021-01-29 18:06:20.175328+00	2021-01-29 18:20:00.621313+00	0		f	f	f	f	\N	\N		251	\N	1d9f191c-02e4-42d6-9685-4c74d47dde8c	\N	f	12
864	2021-01-29 18:06:20.191962+00	2021-01-29 18:20:00.636238+00	0	Valor Total\n	t	f	f	f	\N	\N		252	\N	0dd008b3-d679-4d2e-a1cb-cf4aecba9af6	\N	f	12
875	2021-01-29 18:07:28.286768+00	2021-01-29 18:20:00.651261+00	0	R$ 	t	f	f	f	\N	\N		253	\N	9c9ede36-89f2-4d1a-a6dc-0234e4c04838	\N	f	12
876	2021-01-29 18:07:28.30373+00	2021-01-29 18:20:00.656054+00	1	Valor do Negócio	t	f	f	f	\N	\N		253	\N	608727bb-458f-406b-9f26-f4282eb7810f	fieldVariable-698 fromConnectedField-	t	12
877	2021-01-29 18:07:28.320406+00	2021-01-29 18:20:00.660618+00	2	 	t	f	f	f	\N	\N		253	\N	80bdef44-fb3a-4bb2-8c26-08f253d2892b	\N	f	12
878	2021-01-29 18:07:28.384825+00	2021-01-29 18:20:00.72334+00	0	\n	f	f	f	f	\N	\N		257	\N	89ffb9b8-06b9-4ff6-9183-0f05b8ae8ca1	\N	f	12
879	2021-01-29 18:07:28.40092+00	2021-01-29 18:20:00.739001+00	0	\n	f	f	f	f	\N	\N		258	\N	7e66b2f5-b8e9-4c77-b6cb-f6f40dd7a200	\N	f	12
394	2020-12-13 15:03:21.699698+00	2021-01-29 18:20:00.754245+00	0	Benefícios do Plano         	t	f	f	f	\N	#579cfc50	#0086c0	107	\N	83539b35-2add-48f7-abee-cfb0ad6ee8a4	\N	f	12
395	2020-12-13 15:03:21.70521+00	2021-01-29 18:20:00.758794+00	1	                                                                                                                                \n	f	f	f	f	\N	#579cfc50	#0086c0	107	\N	cdbd8e2f-febc-4dd8-bfea-fbf25a81b667	\N	f	12
609	2020-12-14 06:40:56.175736+00	2021-01-29 18:20:00.77388+00	0	Benefícios	f	f	f	f	\N	\N		110	\N	0f3f43a2-e587-44d8-9607-0ce41ad14718	fieldVariable-703 fromConnectedField-	t	12
610	2020-12-14 06:40:56.184595+00	2021-01-29 18:20:00.778248+00	1	 \n	f	f	f	f	\N	\N		110	\N	74ee4196-18fa-4a89-9b49-618f99ec3f9c	\N	f	12
535	2020-12-13 20:42:19.611992+00	2021-01-29 18:20:00.793179+00	0		f	f	f	f	\N	\N		111	\N	483ab5bc-9758-4d22-a6d4-a5b491c7399f	\N	f	12
884	2021-01-29 18:22:44.691757+00	2021-01-31 19:34:53.222998+00	0		f	f	f	f	\N	\N		263	\N	75e4bc84-1770-4f47-8680-2a6533797882	\N	f	12
887	2021-01-29 18:25:40.547547+00	2021-01-31 19:34:53.239496+00	0	Proposta Comercial	t	f	f	f	\N	\N	#0086c0	264	\N	0ca4b5f3-0486-4b9b-b137-1e99d2b2e107	\N	f	48
888	2021-01-29 18:25:40.565639+00	2021-01-31 19:34:53.255703+00	0		f	f	f	f	\N	\N		266	\N	4469e4f3-09ca-4ab6-9a7b-9115f877b4da	\N	f	12
889	2021-01-29 18:25:40.583323+00	2021-01-31 19:34:53.271794+00	0	Cliente	t	f	f	f	\N	\N	#bfbfbf	267	\N	77f707c0-454a-4f45-86db-a61cf5a3ff64	fieldVariable-679 fromConnectedField-	t	20
890	2021-01-29 18:25:40.588876+00	2021-01-31 19:34:53.276546+00	1	 	t	f	f	f	\N	\N	#bfbfbf	267	\N	e4998663-c379-4e0c-a309-6158c1e3c9ef	\N	f	20
891	2021-01-29 18:25:40.608081+00	2021-01-31 19:34:53.292489+00	0	CPF/ CNPJ	t	f	f	f	\N	\N	#bfbfbf	268	\N	16cf6d33-39c2-4061-a9fb-377e357affad	fieldVariable-692 fromConnectedField-679	t	18
893	2021-01-29 18:25:40.631255+00	2021-01-31 19:34:53.31403+00	0		f	f	f	f	\N	\N		269	\N	9ab059c4-c816-405d-89c9-d96eabf0dc61	\N	f	12
894	2021-01-29 18:25:41.176324+00	2021-01-31 19:34:53.395147+00	0	/\n	f	f	f	f	\N	\N		270	\N	0917610d-cd32-4e16-9a05-297c610023a4	\N	f	12
895	2021-01-29 18:25:41.193475+00	2021-01-31 19:34:53.411086+00	0		f	f	f	f	\N	\N		265	\N	ef0c4fff-2e34-4d60-8e11-630c10cb7063	\N	f	12
896	2021-01-29 18:25:41.639149+00	2021-01-31 19:34:53.488895+00	0	/\n	f	f	f	f	\N	\N		271	\N	2f39ecdb-afe9-49ff-a92f-9c40cad4673e	\N	f	12
938	2021-01-31 19:11:55.196402+00	2021-01-31 19:34:53.786261+00	0	Desconto	t	f	f	f	\N	\N	#0086c0	298	\N	9c2e2ab8-3c21-4225-9049-8e458d6b11b9	\N	f	10
939	2021-01-31 19:11:55.21479+00	2021-01-31 19:34:53.801377+00	0	Total	t	f	f	f	\N	\N	#0086c0	299	\N	3507c645-c796-428a-98f8-69184d3e806c	\N	f	10
940	2021-01-31 19:11:55.232296+00	2021-01-31 19:34:53.8171+00	0	Plano I	f	f	f	f	\N	\N		300	\N	70b5cc6c-c997-40f1-b5c9-29d4113f37f6	fieldVariable-695 fromConnectedField-	t	10
941	2021-01-31 19:11:55.238293+00	2021-01-31 19:34:53.821663+00	1	 	f	f	f	f	\N	\N		300	\N	c5e98337-0702-4d79-9fbe-d51b75254327	\N	f	12
942	2021-01-31 19:11:55.256103+00	2021-01-31 19:34:53.838842+00	0	Quantidade	f	f	f	f	\N	\N		301	\N	f42b28e8-56df-4c6f-b309-af920664048c	fieldVariable-722 fromConnectedField-695	t	10
943	2021-01-31 19:11:55.261903+00	2021-01-31 19:34:53.843659+00	1	 	f	f	f	f	\N	\N		301	\N	afd4eda1-d610-4741-8900-da39f047dd66	\N	f	12
947	2021-01-31 19:15:41.413075+00	2021-01-31 19:34:53.859536+00	0	Valor Unitário	f	f	f	f	\N	\N		302	\N	23da0017-0c55-4c26-b2d5-5a03389496ff	fieldVariable-723 fromConnectedField-695	t	10
948	2021-01-31 19:15:41.419218+00	2021-01-31 19:34:53.864178+00	1	 	f	f	f	f	\N	\N		302	\N	94593290-d32d-44cb-ba0e-a86609e6cdc7	\N	f	12
949	2021-01-31 19:15:41.43772+00	2021-01-31 19:34:53.879782+00	0	Desconto	f	f	f	f	\N	\N		303	\N	514c7d65-bc41-4d40-bdad-13e74057e36c	fieldVariable-724 fromConnectedField-695	t	10
902	2021-01-29 18:27:43.539776+00	2021-01-31 19:34:53.505884+00	0		f	f	f	f	\N	\N		272	\N	479324fc-6bf4-4e0b-b8ed-af1d378a993b	\N	f	12
903	2021-01-29 18:27:43.55735+00	2021-01-31 19:34:53.522638+00	0	Data da Proposta: 	t	f	f	f	\N	\N	#0086c0	277	\N	14325a09-ac27-49f9-8f07-efc3716083e7	\N	f	12
904	2021-01-29 18:27:43.562815+00	2021-01-31 19:34:53.527386+00	1	Data de Atualização	t	f	f	f	\N	\N	#0086c0	277	\N	6b7398e9-8ad4-464f-bc3d-b683580e0603	fieldVariable-691 fromConnectedField-	t	12
905	2021-01-29 18:27:43.568189+00	2021-01-31 19:34:53.53264+00	2	 	t	f	f	f	\N	\N	#0086c0	277	\N	a4e28914-d854-4742-835d-5e4c3166dce2	\N	f	12
906	2021-01-29 18:27:43.584944+00	2021-01-31 19:34:53.549095+00	0	Número da Proposta: 	t	f	f	f	\N	\N		278	\N	efb9fc8c-8a95-4a4f-b4d6-59af53b61289	\N	f	12
907	2021-01-29 18:27:43.590353+00	2021-01-31 19:34:53.553992+00	1	Id do Negócio	f	f	f	f	\N	\N		278	\N	0555f60d-6fd3-4e32-aabe-2be1eff8d64d	fieldVariable-694 fromConnectedField-	t	12
908	2021-01-29 18:27:43.595702+00	2021-01-31 19:34:53.558825+00	2	 	f	f	f	f	\N	\N		278	\N	de77065d-276b-4c57-9f90-4e74c54798aa	\N	f	12
130	2020-12-11 19:21:28.947039+00	2020-12-12 15:58:14.625373+00	0	Proposta Comercial	t	f	f	f	\N	#66ccff50	#0086c0	24	\N	72ba8add-33a7-4c39-98ee-d65e821b1c6f	\N	f	23
779	2021-01-28 13:11:49.389615+00	2021-01-29 18:20:00.989542+00	0	R$ 	f	f	f	f	\N	\N		233	\N	3cf9e1cd-4f96-4ee4-b1dd-81df0533786a	\N	f	10
780	2021-01-28 13:11:49.397709+00	2021-01-29 18:20:00.993889+00	1	Economia Anual	f	f	f	f	\N	\N		233	\N	01793dba-64f7-4bf8-9aff-ad7a4935db37	fieldVariable-701 fromConnectedField-	t	10
781	2021-01-28 13:11:49.406267+00	2021-01-29 18:20:00.998536+00	2	 	f	f	f	f	\N	\N		233	\N	3e911cfa-efc2-46c5-acce-f56d693399fa	\N	f	10
821	2021-01-28 19:50:05.283718+00	2021-01-29 18:20:01.019043+00	1	 	f	f	f	f	\N	\N		234	\N	37d86439-37b0-49ad-8c64-1d489eb4f580	\N	f	12
784	2021-01-28 13:11:49.467301+00	2021-01-29 18:20:01.035109+00	0		f	f	f	f	\N	\N		235	\N	c17f80c4-3bac-49b9-a293-eea40ea185e9	\N	f	12
826	2021-01-28 19:53:11.858094+00	2021-01-29 18:20:01.117311+00	0	/\n	f	f	f	f	\N	\N		182	\N	77ffdce9-8970-46ce-b47d-f4b4c30a64fb	\N	f	12
920	2021-01-31 19:11:54.907374+00	2021-01-31 19:34:53.57434+00	0		f	f	f	f	\N	\N		279	\N	a35d3ba0-e43b-488c-ad33-823b9263bc5c	\N	f	12
921	2021-01-31 19:11:54.928869+00	2021-01-31 19:34:53.590934+00	0	Cliente	t	f	f	f	\N	\N		289	\N	7023f654-f9df-4b94-9a66-7b71d9e0c1bb	fieldVariable-679 fromConnectedField-	t	12
923	2021-01-31 19:11:54.952068+00	2021-01-31 19:34:53.611954+00	0	A/C:	t	f	f	f	\N	\N	#0086c0	290	\N	5ff45200-0db6-4f8f-a666-8bb1a83fec5b	\N	f	12
924	2021-01-31 19:11:54.95798+00	2021-01-31 19:34:53.616779+00	1	 	f	f	f	f	\N	\N		290	\N	8914a14c-70e2-43b6-b6ee-d418b3ecc7e5	\N	f	12
827	2021-01-28 19:53:11.885598+00	2021-01-29 18:20:01.143643+00	0		f	f	f	f	\N	\N		248	\N	ad0bbefb-d650-468f-a827-cfe68f7d17b7	\N	f	12
511	2020-12-13 20:29:02.671889+00	2021-01-29 18:20:01.180581+00	0	Documentos Necessários                                                                                                                          \n	t	f	t	f	\N	\N		127	\N	6ddd0d72-4221-4ea8-8425-2a66ab47720b	\N	f	12
361	2020-12-12 18:15:24.685833+00	2021-01-29 18:20:01.236939+00	0	- Contrato Social	f	f	f	f	\N	\N		108	\N	53a2b5ed-6287-4397-b6d8-694fb151820c	\N	f	12
512	2020-12-13 20:29:02.707884+00	2021-01-29 18:20:01.318926+00	0	- RG e CPF ou CNH do sócio que assina	f	f	f	f	\N	\N		128	\N	c98c8af2-f926-46e5-9537-03bb226e0fa8	\N	f	12
513	2020-12-13 20:29:02.727109+00	2021-01-29 18:20:01.387288+00	0	- Em caso de portabilidade numérica, última conta da operadora atual	f	f	f	f	\N	\N		129	\N	04ffe39e-1de8-461d-848c-60c08aafe9f6	\N	f	12
514	2020-12-13 20:29:02.745726+00	2021-01-29 18:20:01.437017+00	0		f	f	f	f	\N	\N		130	\N	9bc8e428-0ac6-4320-90d4-3ada87c59336	\N	f	12
515	2020-12-13 20:29:02.765029+00	2021-01-29 18:20:01.518748+00	0	Estamos à disposição para os esclarecimentos que se fizerem necessários.	f	f	f	f	\N	\N		131	\N	bd5a4965-934e-4fac-a53c-1782a1de7dfb	\N	f	12
516	2020-12-13 20:29:02.784354+00	2021-01-29 18:20:01.587482+00	0		f	f	f	f	\N	\N		132	\N	e0a062bd-612a-4828-9bab-87fcd30d2456	\N	f	12
517	2020-12-13 20:29:02.805357+00	2021-01-29 18:20:01.679835+00	0	Fernando Dória	t	f	f	f	\N	\N		133	\N	5db7a026-b6d6-426a-b0ab-8e1140521cad	\N	f	12
518	2020-12-13 20:29:02.824546+00	2021-01-29 18:20:01.76986+00	0	11 99232-1281\n	f	f	f	f	\N	\N		134	\N	1fe0f062-b456-44aa-bc2f-1427950ad501	\N	f	12
798	2021-01-28 15:06:21.285556+00	2021-01-29 18:20:01.838108+00	0		f	f	f	f	\N	\N		236	\N	f4058b9f-9b3b-4bd3-8eea-04865d5c80a3	\N	f	12
799	2021-01-28 15:06:21.309931+00	2021-01-29 18:20:01.894812+00	0		f	f	f	f	\N	\N		238	\N	73d608fe-f562-4711-974e-a007a3151073	\N	f	12
804	2021-01-28 15:06:23.348429+00	2021-01-29 18:20:01.954052+00	0	\n	f	f	f	f	\N			243	\N	a40e0b61-1843-400f-9ff8-cd5cea64fb46		f	12
925	2021-01-31 19:11:54.963627+00	2021-01-31 19:34:53.621609+00	2	Contato	f	f	f	f	\N	\N		290	\N	64f97a84-52c0-4129-87c9-8ce6343e3145	fieldVariable-718 fromConnectedField-679	t	12
926	2021-01-31 19:11:54.969314+00	2021-01-31 19:34:53.626213+00	3	 	f	f	f	f	\N	\N		290	\N	3d30940d-bb47-46fb-8484-cf324e674114	\N	f	12
927	2021-01-31 19:11:54.986715+00	2021-01-31 19:34:53.641865+00	0	Negociação:	t	f	f	f	\N	\N	#0086c0	291	\N	8944254f-12fb-4415-becb-22d7111264a3	\N	f	12
928	2021-01-31 19:11:54.992808+00	2021-01-31 19:34:53.646313+00	1	 	f	f	f	f	\N	\N	#0086c0	291	\N	fed4dd4d-4b4a-4ef6-b74d-01b80c3c5dde	\N	f	12
929	2021-01-31 19:11:54.998497+00	2021-01-31 19:34:53.651011+00	2	Negociação	f	f	f	f	\N	\N		291	\N	8270de3f-6e2e-492b-a58a-48cb37836377	fieldVariable-693 fromConnectedField-	t	12
930	2021-01-31 19:11:55.038986+00	2021-01-31 19:34:53.655679+00	3	 	f	f	f	f	\N	\N		291	\N	b7b2fd1a-13cd-4409-afa3-8702be3b58f7	\N	f	12
931	2021-01-31 19:11:55.067032+00	2021-01-31 19:34:53.671536+00	0		f	f	f	f	\N	\N		292	\N	ff3ef9ef-77b6-4ac1-8880-e81e47892a93	\N	f	12
932	2021-01-31 19:11:55.087711+00	2021-01-31 19:34:53.68746+00	0	Seguem abaixo os detalhes do plano sugerido pela Consulting:	t	f	f	f	\N	\N		293	\N	0b32be38-689e-42bc-89eb-3e334626c7eb	\N	f	12
933	2021-01-31 19:11:55.104825+00	2021-01-31 19:34:53.705636+00	0		f	f	f	f	\N	\N		281	\N	c365cd7f-821b-48b9-a6f8-fdb68b79e15f	\N	f	12
934	2021-01-31 19:11:55.125296+00	2021-01-31 19:34:53.723532+00	0	/\n	f	f	f	f	\N	\N		294	\N	963f0263-a228-4145-ab35-ca6b83b3dff4	\N	f	12
935	2021-01-31 19:11:55.143456+00	2021-01-31 19:34:53.739846+00	0	Plano	t	f	f	f	\N	\N	#0086c0	295	\N	780b9401-e344-4e9a-826a-6b3c05e09d07	\N	f	10
936	2021-01-31 19:11:55.160916+00	2021-01-31 19:34:53.754918+00	0	Quantidade	t	f	f	f	\N	\N	#0086c0	296	\N	27d4255b-3a89-4b35-9fc0-368f1b1095b3	\N	f	10
937	2021-01-31 19:11:55.178773+00	2021-01-31 19:34:53.770164+00	0	Valor Unitário	t	f	f	f	\N	\N	#0086c0	297	\N	1aea1116-afde-4e16-beb5-d891d72aaada	\N	f	10
950	2021-01-31 19:15:41.443646+00	2021-01-31 19:34:53.884432+00	1	 	f	f	f	f	\N	\N		303	\N	9278760c-7611-45b1-9bd1-5f7af9ca69f3	\N	f	12
951	2021-01-31 19:15:41.460209+00	2021-01-31 19:34:53.900132+00	0	Total	f	f	f	f	\N	\N		304	\N	8a8d061b-7b52-4aea-9eb9-1cbeec5a3102	fieldVariable-725 fromConnectedField-695	t	10
952	2021-01-31 19:15:41.466011+00	2021-01-31 19:34:53.90515+00	1	 	f	f	f	f	\N	\N		304	\N	74639791-146c-4fd6-a8e2-2bb13278eb68	\N	f	12
963	2021-01-31 19:16:29.836553+00	2021-01-31 19:34:53.921404+00	0	Plano II	f	f	f	f	\N	\N		305	\N	6d5ef5e0-262f-40ef-9bfc-8496f3efe81f	fieldVariable-726 fromConnectedField-	t	10
964	2021-01-31 19:16:29.842017+00	2021-01-31 19:34:53.925984+00	1	 	f	f	f	f	\N	\N		305	\N	2932860c-2997-4b58-9a7e-a16ff8ddbaf7	\N	f	12
63	2020-12-03 19:46:10.989904+00	2020-12-12 15:58:15.346316+00	0		f	f	f	f	\N	\N		43	\N	ac870275-3958-492b-8630-8dd60abc96bf	\N	f	12
64	2020-12-03 19:46:11.011712+00	2020-12-12 15:58:15.361686+00	0		f	f	f	f	\N	\N		44	\N	5187abd6-f061-48ec-b5e8-bbad00eef036	\N	f	12
102	2020-12-03 19:57:09.461849+00	2020-12-12 15:58:15.380148+00	0	Comparativo - Plano Atual vs Novo Plano                                                                          \n	t	f	f	f	\N	#579cfc50	#0086c0	45	\N	d7ab45e0-ab94-4021-ad45-bc32159d7e3b	\N	f	12
80	2020-12-03 19:46:11.171776+00	2020-12-12 15:58:15.508559+00	0	\n	t	f	f	f	\N	#579cfc50	#0086c0	48	\N	a12a6859-cb4d-4f9e-879d-a5d851960b15	\N	f	12
81	2020-12-03 19:46:11.193131+00	2020-12-12 15:58:15.5242+00	0	\n	f	f	f	f	\N	\N		49	\N	765e3110-d233-41f9-9ce6-6ddb774907aa	\N	f	12
883	2021-01-29 18:22:44.673355+00	2021-01-31 19:34:53.206843+00	0		f	f	f	f	\N	\N		262	\N	30a87e0a-7215-4615-b4d2-42af3ba622ce	\N	f	12
996	2021-01-31 19:30:35.462448+00	2021-01-31 19:34:54.333146+00	0	Valor do Negócio	f	f	f	f	\N	\N		323	\N	7df9259f-bd8f-43dc-a066-85a18ffcd7d1	fieldVariable-698 fromConnectedField-	t	10
997	2021-01-31 19:30:35.467961+00	2021-01-31 19:34:54.338267+00	1	 	f	f	f	f	\N	\N		323	\N	8146e4ec-56c8-4149-ada3-fc7e3f63e8c1	\N	f	12
998	2021-01-31 19:30:35.484904+00	2021-01-31 19:34:54.355421+00	0	Economia Mensal	f	f	f	f	\N	\N		324	\N	e4af25d5-682d-40fd-9eb0-b93f963c9784	fieldVariable-700 fromConnectedField-	t	10
999	2021-01-31 19:30:35.490719+00	2021-01-31 19:34:54.359961+00	1	 	f	f	f	f	\N	\N		324	\N	b620239b-00d1-4f36-9742-570964a59cfe	\N	f	12
1000	2021-01-31 19:30:35.509349+00	2021-01-31 19:34:54.376521+00	0	Economia Anual	f	f	f	f	\N	\N		325	\N	f9e249b2-a7eb-409e-8342-337c831243e1	fieldVariable-701 fromConnectedField-	t	10
1001	2021-01-31 19:30:35.515424+00	2021-01-31 19:34:54.381318+00	1	 	f	f	f	f	\N	\N		325	\N	0b04113a-a3db-49f0-92fa-7fe9e572a594	\N	f	12
1002	2021-01-31 19:30:35.533353+00	2021-01-31 19:34:54.397311+00	0	Percentual de Redução	t	f	f	f	\N	\N	#0dbf7e	326	\N	2cf813ea-7cd2-4224-bed9-f1bde277e286	fieldVariable-702 fromConnectedField-	t	10
1003	2021-01-31 19:30:35.539761+00	2021-01-31 19:34:54.401748+00	1	 	f	f	f	f	\N	\N		326	\N	b24c378e-3818-431b-9e4f-221955cd0819	\N	f	12
1004	2021-01-31 19:30:35.557355+00	2021-01-31 19:34:54.417607+00	0		f	f	f	f	\N	\N		286	\N	a829da31-523e-4246-9227-6d26bab93d6e	\N	f	12
1005	2021-01-31 19:30:36.057979+00	2021-01-31 19:34:54.498179+00	0	/\n	f	f	f	f	\N	\N		327	\N	b4f4e69d-09ad-4ee9-ae8d-679ed36cb429	\N	f	12
918	2021-01-29 18:27:43.755839+00	2021-01-31 19:34:54.513546+00	0	\n	f	f	f	f	\N	\N		287	\N	b1827d99-921e-4653-ae8f-e53f8aaa69cd	\N	f	12
1006	2021-01-31 19:30:36.09186+00	2021-01-31 19:34:54.530496+00	0	Documentos Necessários                                                                                                                              \n	t	f	t	f	\N	\N		288	\N	4a729cd9-7c6f-4519-8865-9091036d199b	\N	f	12
899	2021-01-29 18:25:41.695012+00	2021-01-31 19:34:54.547832+00	0	- Contrato Social	f	f	f	f	\N	\N		274	\N	d71cd961-ef96-493b-ba7c-49273f6a82e6	\N	f	12
1007	2021-01-31 19:33:12.093912+00	2021-01-31 19:34:54.564641+00	0	- RG e CPF ou CNH do sócio que assina	f	f	f	f	\N	\N		328	\N	24249533-7c4d-4dbc-856e-9779dffa544d	\N	f	12
1008	2021-01-31 19:33:12.112272+00	2021-01-31 19:34:54.58109+00	0	- Em caso de portabilidade numérica, última conta da operadora atual	f	f	f	f	\N	\N		329	\N	b918a5c3-5300-4fc9-b231-30f9eaf81909	\N	f	12
1010	2021-01-31 19:33:12.147536+00	2021-01-31 19:34:54.613415+00	0	Estamos à disposição para esclarecimentos que se fizerem necessários.	f	f	f	f	\N	\N		331	\N	55b43e61-00dd-456f-81d5-a48932f20ebd	\N	f	12
1011	2021-01-31 19:33:12.165788+00	2021-01-31 19:34:54.629341+00	0		f	f	f	f	\N	\N		332	\N	9eee73b4-4725-476d-9b72-3de8f9fba2c9	\N	f	12
1012	2021-01-31 19:33:12.182743+00	2021-01-31 19:34:54.645194+00	0	Fernando Dória	t	f	f	f	\N	\N		333	\N	4c729a3f-df0b-4eaa-8e78-dae69ab0d9df	\N	f	12
1013	2021-01-31 19:33:12.199987+00	2021-01-31 19:34:54.660488+00	0	11 99232-1281	f	f	f	f	\N	\N		334	\N	0c60c059-4822-43d4-82f0-8b377d25c150	\N	f	12
1014	2021-01-31 19:33:12.217458+00	2021-01-31 19:34:54.676107+00	0	\n	t	f	f	f	\N	\N		335	\N	cef0fafd-1992-4f41-ac4a-9eb4a7e6d5e1	\N	f	12
1015	2021-01-31 19:33:12.236341+00	2021-01-31 19:34:54.692058+00	0	\n	f	f	f	f	\N	\N		336	\N	9ffb0cf3-b964-4ac1-bf59-8e0daace7353	\N	f	12
900	2021-01-29 18:25:41.712384+00	2021-01-31 19:34:54.708197+00	0		f	f	f	f	\N	\N		275	\N	e5220201-40dd-4024-994f-571223dde211	\N	f	12
901	2021-01-29 18:25:41.730442+00	2021-01-31 19:34:54.724825+00	0	\n	f	f	f	f	\N			276	\N	83d7bdb0-c1fd-431b-a154-bc8550b19496		f	12
\.


--
-- Data for Name: text_image_option; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.text_image_option (id, link, bucket, file_image_path, file_name, file_size, file_url, size_relative_to_view, file_image_uuid) FROM stdin;
1	\N	reflow-crm	rich-text/file-rich-text-image	\N	\N	\N	1.00000000000000000000	6c19bcb3-a4b8-4ad8-88a0-1ce8197922bc
2	\N	reflow-crm	rich-text/file-rich-text-image	complete_logo.png	64635	https://reflow-crm.s3.amazonaws.com/rich-text/file-rich-text-image/067f6a92-a148-4de9-b33e-5b60f6929796/complete_logo.png	1.00000000000000000000	6ed3f1b9-5874-499f-ab11-465a3595f180
13	\N	reflow-crm	rich-text/file-rich-text-image	LOGO-CONSULTING-ORIGINAL.png	42438	https://reflow-crm.s3.amazonaws.com/rich-text/file-rich-text-image/c323e7d2-4279-4566-a323-23936dd12f04/LOGO-CONSULTING-ORIGINAL.png	0.86999999999999990000	6d1e67a6-4c5e-441c-b483-08edad3ae451
14	\N	reflow-crm	rich-text/file-rich-text-image	Design sem nome (1).png	847356	https://reflow-crm.s3.amazonaws.com/rich-text/file-rich-text-image/8de182af-79ef-499c-90f7-70cefbd7724b/Design%20sem%20nome%20%281%29.png	1.00000000000000000000	ce738e1b-cdbb-43f8-a629-cfdf8e77a400
15	\N	reflow-crm	rich-text/file-rich-text-image	cabecalho.PNG	33895	https://reflow-crm.s3.amazonaws.com/rich-text/file-rich-text-image/4051c3a7-3d4f-4bfe-a8ea-93cb30696e74/cabecalho.PNG	1.00000000000000000000	71b747fd-eb8f-4bcd-bf4b-48feea5b40d8
16	\N	reflow-crm	rich-text/file-rich-text-image	cabecalho.PNG	33895	https://reflow-crm.s3.amazonaws.com/rich-text/file-rich-text-image/91f9ab10-4b8e-43c8-a5e6-afe3dcdec56e/cabecalho.PNG	1.00000000000000000000	f5c86326-15b0-4844-8078-4403288dd9f2
3	\N	reflow-crm	rich-text/file-rich-text-image	LOGO-CONSULTING-ORIGINAL.png	42438	https://reflow-crm.s3.amazonaws.com/rich-text/file-rich-text-image/a56ab735-5385-44bd-9883-f1093c800101/LOGO-CONSULTING-ORIGINAL.png	1.00000000000000000000	43b7b85e-7515-4c71-8d47-98f0c69fb45e
4	\N	reflow-crm	rich-text/file-rich-text-image	Design sem nome (1).png	847356	https://reflow-crm.s3.amazonaws.com/rich-text/file-rich-text-image/acbe0137-793c-4de5-935d-50f05cd58fa8/Design%20sem%20nome%20%281%29.png	1.01000000000000000000	4484cdfc-a12b-48ac-b69d-5d54df0e4cbf
11	\N	reflow-crm	rich-text/file-rich-text-image	cabecalho.PNG	33895	https://reflow-crm.s3.amazonaws.com/rich-text/file-rich-text-image/8b3db02d-bbb1-4734-b8c7-810b99dda1ee/cabecalho.PNG	1.01000000000000000000	38a3a372-32c6-4886-9ff5-4519fd244cd3
5	\N	reflow-crm	rich-text/file-rich-text-image	image.png	97565	https://reflow-crm.s3.amazonaws.com/rich-text/file-rich-text-image/5302505c-2603-4cb4-8a92-2aae7142185d/image.png	1.01000000000000000000	3c38cee3-3159-42f7-b58e-6c22a65c7486
6	\N	reflow-crm	rich-text/file-rich-text-image	image.png	136722	https://reflow-crm.s3.amazonaws.com/rich-text/file-rich-text-image/7d659225-6d78-46c4-986e-a0b56628ee8a/image.png	0.54999999999999960000	cac1f839-8256-4dfe-ae20-bf907ba5bb1e
7	\N	reflow-crm	rich-text/file-rich-text-image	image.png	23931	https://reflow-crm.s3.amazonaws.com/rich-text/file-rich-text-image/fc93bcb3-7db6-410a-8c3f-7e03d9eb3ce9/image.png	0.68999999999999970000	501f649e-01cf-4752-919a-b62602dce0a2
8	\N	reflow-crm	rich-text/file-rich-text-image	image.png	146986	https://reflow-crm.s3.amazonaws.com/rich-text/file-rich-text-image/f77702d4-1368-44e2-9672-30035ea96bd6/image.png	1.00000000000000000000	147bfc0f-0e82-4823-bc5d-57fd066faca4
9	\N	reflow-crm	rich-text/file-rich-text-image	image.png	37041	https://reflow-crm.s3.amazonaws.com/rich-text/file-rich-text-image/b1d7fd95-5cf9-4290-9666-57e1ffbd0e4c/image.png	1.00000000000000000000	01721f82-af65-4102-809f-17f612fc3cb5
10	\N	reflow-crm	rich-text/file-rich-text-image	cabecalho.PNG	33895	https://reflow-crm.s3.amazonaws.com/rich-text/file-rich-text-image/5b5cfa74-db41-4af4-8da6-d438dd190ab4/cabecalho.PNG	1.01000000000000000000	871eea62-bfaf-40a4-bfe3-4365226ee20f
12	\N	reflow-crm	rich-text/file-rich-text-image	cabecalho.PNG	33895	https://reflow-crm.s3.amazonaws.com/rich-text/file-rich-text-image/d90bc220-411a-4b65-a93f-37137090dc72/cabecalho.PNG	1.00000000000000000000	91edc34a-4698-4bc0-87c0-cec6822653ac
\.


--
-- Data for Name: text_list_option; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.text_list_option (id, list_type_id) FROM stdin;
\.


--
-- Data for Name: text_list_type; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.text_list_type (id, name, "order") FROM stdin;
1	unordered	1
2	ordered	2
\.


--
-- Data for Name: text_page; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.text_page (id, created_at, updated_at, raw_text, markdown_text, company_id, user_id) FROM stdin;
1	2020-12-03 14:22:54.840217+00	2020-12-03 16:23:48.771705+00			1	1
7	2021-01-29 18:22:44.120984+00	2021-01-31 19:34:53.073107+00			1	1
2	2020-12-03 19:46:10.473818+00	2020-12-12 15:58:14.608159+00			1	1
3	2020-12-12 18:01:57.969058+00	2021-01-29 18:19:59.42155+00			1	1
\.


--
-- Data for Name: text_table_option; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.text_table_option (id, border_color) FROM stdin;
1	\N
2	\N
3	#ffffff
4	#bfbfbf
5	\N
6	#ffffff
7	#bfbfbf
8	\N
9	#ffffff
10	#bfbfbf
11	\N
12	#ffffff
13	#bfbfbf
14	#bfbfbf
15	#ffffff
16	#bfbfbf
17	#bfbfbf
18	#ffffff
19	#bfbfbf
20	#bfbfbf
21	#ffffff
22	#bfbfbf
23	#bfbfbf
24	#ffffff
25	#bfbfbf
26	#bfbfbf
27	#ffffff
28	#bfbfbf
29	#bfbfbf
30	#ffffff
31	#bfbfbf
32	#bfbfbf
33	#ffffff
34	#bfbfbf
35	#bfbfbf
36	#ffffff
37	#bfbfbf
38	#bfbfbf
39	#ffffff
40	#bfbfbf
41	#bfbfbf
42	#ffffff
43	#bfbfbf
44	#bfbfbf
45	#ffffff
46	#bfbfbf
47	#bfbfbf
48	#ffffff
49	#bfbfbf
50	#ffffff
51	#bfbfbf
52	#ffffff
53	#bfbfbf
54	#ffffff
55	#bfbfbf
56	#ffffff
57	#bfbfbf
58	#ffffff
59	#bfbfbf
60	#ffffff
61	#ffffff
62	#ffffff
63	#ffffff
64	\N
65	#ffffff
66	\N
67	#ffffff
68	\N
69	#ffffff
70	\N
71	#ffffff
72	\N
73	#ffffff
74	\N
75	\N
76	#ffffff
77	\N
78	\N
79	#ffffff
80	\N
81	\N
\.


--
-- Data for Name: text_table_option_column_dimension; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.text_table_option_column_dimension (id, width, text_table_option_id, "order") FROM stdin;
1	50	1	0
2	50	1	1
3	50	2	0
4	50	2	1
5	50	3	0
6	50	3	1
7	24	4	0
8	20	4	1
9	23	4	2
10	17	4	3
11	41	4	4
12	17	5	0
13	21	5	1
14	24	5	2
15	22	5	3
16	41	5	4
17	50	6	0
18	50	6	1
19	24	7	0
20	20	7	1
21	22	7	2
22	18	7	3
23	41	7	4
24	17	8	0
25	21	8	1
26	24	8	2
27	22	8	3
28	41	8	4
29	50	9	0
30	50	9	1
31	24	10	0
32	20	10	1
33	22	10	2
34	18	10	3
35	41	10	4
36	17	11	0
37	21	11	1
38	24	11	2
39	22	11	3
40	41	11	4
41	50	12	0
42	50	12	1
43	24	13	0
44	20	13	1
45	22	13	2
46	18	13	3
47	41	13	4
48	17	14	0
49	21	14	1
50	24	14	2
51	22	14	3
52	41	14	4
53	50	15	0
54	50	15	1
55	24	16	0
56	20	16	1
57	22	16	2
58	18	16	3
59	41	16	4
60	17	17	0
61	21	17	1
62	24	17	2
63	22	17	3
64	41	17	4
65	50	18	0
66	50	18	1
67	24	19	0
68	20	19	1
69	22	19	2
70	18	19	3
71	41	19	4
72	17	20	0
73	21	20	1
74	24	20	2
75	22	20	3
76	41	20	4
77	50	21	0
78	50	21	1
79	24	22	0
80	20	22	1
81	22	22	2
82	18	22	3
83	41	22	4
84	17	23	0
85	21	23	1
86	24	23	2
87	22	23	3
88	41	23	4
89	50	24	0
90	50	24	1
91	24	25	0
92	20	25	1
93	22	25	2
94	18	25	3
95	41	25	4
96	17	26	0
97	21	26	1
98	24	26	2
99	22	26	3
100	41	26	4
101	50	27	0
102	50	27	1
103	24	28	0
104	20	28	1
105	22	28	2
106	18	28	3
107	41	28	4
108	17	29	0
109	21	29	1
110	24	29	2
111	22	29	3
112	41	29	4
113	50	30	0
114	50	30	1
115	24	31	0
116	20	31	1
117	22	31	2
118	18	31	3
119	41	31	4
120	17	32	0
121	21	32	1
122	24	32	2
123	22	32	3
124	41	32	4
125	50	33	0
126	50	33	1
127	24	34	0
128	20	34	1
129	22	34	2
130	18	34	3
131	41	34	4
132	17	35	0
133	21	35	1
134	24	35	2
135	22	35	3
136	41	35	4
137	50	36	0
138	50	36	1
139	24	37	0
140	20	37	1
141	22	37	2
142	18	37	3
143	41	37	4
144	17	38	0
145	21	38	1
146	24	38	2
147	22	38	3
148	41	38	4
149	50	39	0
150	50	39	1
151	24	40	0
152	20	40	1
153	22	40	2
154	18	40	3
155	41	40	4
156	17	41	0
157	21	41	1
158	24	41	2
159	22	41	3
160	41	41	4
161	50	42	0
162	50	42	1
163	24	43	0
164	20	43	1
165	22	43	2
166	18	43	3
167	41	43	4
168	17	44	0
169	21	44	1
170	24	44	2
171	22	44	3
172	41	44	4
173	50	45	0
174	50	45	1
175	24	46	0
176	20	46	1
177	22	46	2
178	18	46	3
179	41	46	4
180	17	47	0
181	21	47	1
182	24	47	2
183	22	47	3
184	41	47	4
185	50	48	0
186	50	48	1
187	24	49	0
188	20	49	1
189	22	49	2
190	18	49	3
191	41	49	4
192	20	50	0
193	20	50	1
194	12	50	2
195	24	50	3
196	24	50	4
197	17	51	0
198	21	51	1
199	24	51	2
200	22	51	3
201	41	51	4
202	50	52	0
203	50	52	1
204	24	53	0
205	20	53	1
206	22	53	2
207	18	53	3
208	41	53	4
209	20	54	0
210	20	54	1
211	12	54	2
212	24	54	3
213	24	54	4
214	17	55	0
215	21	55	1
216	24	55	2
217	22	55	3
218	41	55	4
219	50	56	0
220	50	56	1
221	24	57	0
222	20	57	1
223	22	57	2
224	18	57	3
225	41	57	4
226	20	58	0
227	20	58	1
228	12	58	2
229	24	58	3
230	24	58	4
231	17	59	0
232	21	59	1
233	24	59	2
234	22	59	3
235	41	59	4
236	50	60	0
237	50	60	1
238	50	61	0
239	50	61	1
240	50	62	0
241	50	62	1
242	50	63	0
243	50	63	1
244	20	64	0
245	20	64	1
246	20	64	2
247	20	64	3
248	20	64	4
249	50	65	0
250	50	65	1
251	20	66	0
252	20	66	1
253	20	66	2
254	20	66	3
255	20	66	4
256	50	67	0
257	50	67	1
258	20	68	0
259	20	68	1
260	20	68	2
261	20	68	3
262	20	68	4
263	50	69	0
264	50	69	1
265	20	70	0
266	20	70	1
267	20	70	2
268	20	70	3
269	20	70	4
270	50	71	0
271	50	71	1
272	20	72	0
273	20	72	1
274	20	72	2
275	20	72	3
276	20	72	4
277	50	73	0
278	50	73	1
279	20	74	0
280	20	74	1
281	20	74	2
282	20	74	3
283	20	74	4
284	17	75	0
285	21	75	1
286	24	75	2
287	22	75	3
288	16	75	4
289	50	76	0
290	50	76	1
291	20	77	0
292	20	77	1
293	20	77	2
294	20	77	3
295	20	77	4
296	17	78	0
297	21	78	1
298	24	78	2
299	22	78	3
300	16	78	4
301	50	79	0
302	50	79	1
303	20	80	0
304	20	80	1
305	20	80	2
306	20	80	3
307	20	80	4
308	17	81	0
309	21	81	1
310	24	81	2
311	22	81	3
312	16	81	4
\.


--
-- Data for Name: text_table_option_row_dimension; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.text_table_option_row_dimension (id, height, text_table_option_id, "order") FROM stdin;
1	\N	1	0
2	\N	1	1
3	\N	2	0
4	\N	2	1
5	\N	3	0
6	\N	3	1
7	\N	4	0
8	\N	4	1
9	\N	4	2
10	\N	5	0
11	\N	5	1
12	\N	6	0
13	\N	6	1
14	\N	7	0
15	\N	7	1
16	\N	7	2
17	\N	8	0
18	\N	8	1
19	\N	9	0
20	\N	9	1
21	\N	10	0
22	\N	10	1
23	\N	10	2
24	\N	11	0
25	\N	11	1
26	\N	12	0
27	\N	12	1
28	\N	13	0
29	\N	13	1
30	\N	13	2
31	\N	14	0
32	\N	14	1
33	\N	15	0
34	\N	15	1
35	\N	16	0
36	\N	16	1
37	\N	16	2
38	\N	17	0
39	\N	17	1
40	\N	18	0
41	\N	18	1
42	\N	19	0
43	\N	19	1
44	\N	19	2
45	\N	20	0
46	\N	20	1
47	\N	21	0
48	\N	21	1
49	\N	22	0
50	\N	22	1
51	\N	22	2
52	\N	23	0
53	\N	23	1
54	\N	24	0
55	\N	24	1
56	\N	25	0
57	\N	25	1
58	\N	25	2
59	\N	26	0
60	\N	26	1
61	\N	27	0
62	\N	27	1
63	\N	28	0
64	\N	28	1
65	\N	28	2
66	\N	29	0
67	\N	29	1
68	\N	30	0
69	\N	30	1
70	\N	31	0
71	\N	31	1
72	\N	31	2
73	\N	32	0
74	\N	32	1
75	\N	33	0
76	\N	33	1
77	\N	34	0
78	\N	34	1
79	\N	34	2
80	\N	35	0
81	\N	35	1
82	\N	36	0
83	\N	36	1
84	\N	37	0
85	\N	37	1
86	\N	37	2
87	\N	38	0
88	\N	38	1
89	\N	39	0
90	\N	39	1
91	\N	40	0
92	\N	40	1
93	\N	40	2
94	\N	41	0
95	\N	41	1
96	\N	42	0
97	\N	42	1
98	\N	43	0
99	\N	43	1
100	\N	43	2
101	\N	44	0
102	\N	44	1
103	\N	45	0
104	\N	45	1
105	\N	46	0
106	\N	46	1
107	\N	46	2
108	\N	47	0
109	\N	47	1
110	\N	48	0
111	\N	48	1
112	\N	49	0
113	\N	49	1
114	\N	49	2
115	\N	50	0
116	\N	50	1
117	\N	51	0
118	\N	51	1
119	\N	52	0
120	\N	52	1
121	\N	53	0
122	\N	53	1
123	\N	53	2
124	\N	54	0
125	\N	54	1
126	\N	55	0
127	\N	55	1
128	\N	56	0
129	\N	56	1
130	\N	57	0
131	\N	57	1
132	\N	57	2
133	\N	58	0
134	\N	58	1
135	\N	59	0
136	\N	59	1
137	\N	60	0
138	\N	60	1
139	\N	61	0
140	\N	61	1
141	\N	62	0
142	\N	62	1
143	\N	63	0
144	\N	63	1
145	\N	64	0
146	\N	64	1
147	\N	65	0
148	\N	65	1
149	\N	66	0
150	\N	66	1
151	\N	66	2
152	\N	66	3
153	\N	67	0
154	\N	67	1
155	\N	68	0
156	\N	68	1
157	\N	68	2
158	\N	68	3
159	\N	69	0
160	\N	69	1
161	\N	70	0
162	\N	70	1
163	\N	70	2
164	\N	70	3
165	\N	71	0
166	\N	71	1
167	\N	72	0
168	\N	72	1
169	\N	72	2
170	\N	72	3
171	\N	73	0
172	\N	73	1
173	\N	74	0
174	\N	74	1
175	\N	74	2
176	\N	74	3
177	\N	75	0
178	\N	75	1
179	\N	76	0
180	\N	76	1
181	\N	77	0
182	\N	77	1
183	\N	77	2
184	\N	77	3
185	\N	78	0
186	\N	78	1
187	\N	79	0
188	\N	79	1
189	\N	80	0
190	\N	80	1
191	\N	80	2
192	\N	80	3
193	\N	81	0
194	\N	81	1
\.


--
-- Data for Name: text_text_option; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.text_text_option (id, alignment_type_id) FROM stdin;
24	3
25	1
70	1
27	1
28	1
29	1
31	1
32	1
34	1
35	1
50	1
51	1
52	1
39	1
40	1
54	1
55	1
56	1
1	1
2	1
3	1
4	1
5	1
6	1
7	1
8	1
9	1
10	1
11	1
12	1
13	1
14	1
15	1
16	1
17	1
18	1
19	1
20	1
21	1
22	1
23	1
57	1
58	1
59	1
60	1
47	1
61	1
62	1
63	1
64	1
65	1
66	1
41	1
42	1
43	1
44	1
45	1
46	1
67	1
68	1
69	1
48	1
49	1
71	1
26	1
53	1
36	1
37	1
38	1
33	1
184	1
167	1
30	1
173	1
174	1
175	1
185	1
95	1
109	1
96	1
97	1
98	1
99	1
100	1
101	1
102	1
103	1
104	1
105	1
75	1
186	1
187	1
188	1
189	1
190	1
196	1
168	1
169	1
302	1
72	1
171	1
172	1
301	1
170	1
87	1
233	1
238	1
176	1
179	1
180	1
181	1
74	1
183	1
76	1
177	1
178	1
77	1
94	1
78	1
79	1
82	1
112	1
83	1
84	1
115	1
116	1
117	1
118	1
119	1
85	1
80	1
197	1
73	1
198	1
199	1
200	1
303	1
304	3
305	3
306	3
307	3
86	2
81	1
142	1
191	1
192	1
193	1
194	1
120	1
121	1
195	1
250	1
145	1
251	1
252	1
253	1
255	1
135	1
136	1
137	1
138	1
139	1
140	1
256	1
241	1
242	1
243	2
244	1
257	1
258	1
254	1
259	1
264	1
245	1
246	1
247	1
265	1
151	1
143	3
266	1
248	2
308	1
309	3
148	1
149	1
310	3
311	3
152	1
153	1
154	1
155	1
156	1
157	1
158	1
159	1
160	1
161	1
162	1
163	1
164	1
165	1
166	1
89	1
90	1
91	1
92	1
93	1
106	1
267	1
312	3
114	1
123	1
124	1
125	1
126	1
122	1
141	1
313	1
314	1
315	1
316	1
317	1
318	1
319	1
320	1
201	1
202	1
203	1
144	1
146	1
147	1
204	1
150	1
237	1
205	1
206	3
207	3
208	3
249	1
107	1
110	1
111	1
113	1
221	3
222	3
223	3
224	3
321	1
209	3
210	1
211	3
212	3
213	3
214	3
215	1
216	3
217	3
218	3
219	3
240	1
225	3
226	3
227	3
228	3
229	3
230	3
231	1
236	1
239	1
127	1
108	1
128	1
129	1
130	1
131	1
132	1
133	1
134	1
232	1
234	1
235	1
220	2
88	1
182	1
260	1
276	1
277	1
278	1
279	1
280	1
268	1
281	1
282	3
283	3
284	3
285	3
286	1
287	3
288	3
289	3
290	3
291	1
292	3
293	3
294	3
295	3
296	1
297	3
298	3
299	3
300	3
269	1
270	1
271	1
272	1
273	1
274	1
275	1
261	1
262	1
263	1
\.


--
-- Data for Name: theme; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.theme (id, display_name, created_at, theme_type_id, user_id, description, is_public, company_id) FROM stdin;
2	Vendas para corretores	2019-07-17 13:33:13.959749+00	\N	\N		f	\N
16	Pipeline de Vendas Padrão	2019-08-20 00:12:31.318+00	2	1	- Template de pipeline de vendas que se encaixa em qualquer negócio\n- Mapeie o motivo de perda das suas contas\n- Receba notificações um dia antes da previsão de fechamento do negócio\n- Anexe documentos sobre a negociação\n- Centralize as informações de seus clientes	t	1
17	Empresa Fotovoltaica	2019-08-20 01:47:34.967+00	2	1	- Para empresas que vendem equipamentos fotovoltaicos e desejam controlar suas vendas!\n- Inclua todas as informações sobre a instalação do sistema\n- Receba avisos sobre próximos fechamentos\n- Evite falta de informação no momento da instalação\n- Centralize as informações de todos os seus clientes	t	1
18	Relatório de Sinistro	2019-08-21 01:27:57.288+00	7	1	- Para corretores, assessorias e seguradoras que desejam controlar a abertura de sinistro\n- Anexe documentações importantes sobre o processo\n- Ganhe poder de análise sobre a saúde de suas apólices\n- Embase seus argumentos com números em suas negociações de renovação\n- Controle o processo de pagamento de sinistro em um único painel	t	1
19	Corretores Imobiliários	2019-08-22 00:41:59.329+00	2	1	- Para corretores de imóveis que querem organizar suas vendas\n- Centralize as informações de imóveis e clientes\n- Anexe documentos importantes de seus clientes\n- Não esqueça de comparecer à nenhuma visita agendada\n- Entenda os seus principais motivos de perda de negócios\n- Cadastre e atualize a situação de todos os imóveis sob sua gestão	t	1
1	Vazio	2019-07-16 22:48:06.938+00	1	1	- Para quem quer começar do 0 sem dor de cabeça\n- Apenas com um formulário de exemplo	t	1
20	Organização de Tarefas	2019-08-22 00:58:54.889+00	1	1	- Para pessoas que querem organizar o seu dia-a-dia de maneira eficiente!\n- Organize suas tarefas pessoais ou profissionais em um único lugar\n- Receba avisos de tarefas que precisam ser concluídas\n- Trabalhe de maneira objetiva nas tarefas mais importantes para você	t	1
15	Corretores de Seguro	2019-08-19 02:28:28.586+00	2	1	- Para corretores de Seguro que desejam organizar suas vendas!\n- Centralize o cadastro dos seus clientes em um único lugar\n- Este sistema possui campos para inserção de cálculos de diversas seguradoras\n- Avisos de renovação já estão configurados para aparecerem 60 dias antes do vencimento da apólice\n- O sistema já possui campos de anexo para incluir as cotações e apólices de seguradoras	t	1
21	Manutenção Corretiva	2019-08-22 02:28:21.615+00	7	1	- Para estabelecimentos hoteleiros que desejam organizar manutenções previstas\n- Centralize todas as informações sobre o serviço a ser realizado\n- Visualize o andamento das manutenções até a finalização das mesmas\n- Centralize as informações de seus fornecedores	t	1
22	Recrutamento e Seleção	2019-08-25 18:04:10.1+00	4	1	- Para departamentos de RH que desejam organizar o processo de recrutamento e seleção\n- Centralize as informações dos candidatos\n- Anexe currículos de cada candidato\n- Visualize o painel de processos seletivos em um único lugar\n- Receba avisos de entrevistas agendadas	t	1
23	Controle de Desligamentos	2019-08-25 19:18:33.459+00	4	1	- Para departamentos de RH que desejam organizar o processo demissional\n- Anexe documentos de cada colaboador\n- Visualize o painel de processo demssional em um único lugar\n- Receba avisos de entrevistas demissionais agendadas\n- Monte métricas para analisar o turn-over	t	1
24	Desenvolvimento de Software	2019-08-25 19:55:22.15+00	3	1	- Para departamentos de TI que desejam controlar suas atividades de desenvolvimento\n- Visualize o status de suas demandas em um único painel\n- Anexe evidências de bugs e deixe tudo documentado\n- Receba avisos de demandas à serem entregues	t	1
25	Controle de Despesas	2019-08-27 00:44:26.209+00	9	1	- Para empresas que desejam centralizar o lançamento de despesas de maneira simples\n- Separe suas despesas por diversos tipos e veja onde mais gasta\n- Anexe comprovantes de pagamento e deixe tudo organizado\n- Veja seus lançamentos por data e monte relatórios de análise	t	1
26	Controle de Recebíveis	2019-08-27 01:31:18.475+00	9	1	- Para empresas que precisam controlar as contas à receber\n- Anexe faturas e comprovantes por pagamento e deixe tudo documentado\n- Centralize o cadastro de clientes cobrados\n- Gerencia o status das suas contas à receber\n- Receba avisos de faturas próximas do vencimento e cobre seus recebimentos	t	1
27	Planejamento de Postagens	2019-08-27 02:28:01.859+00	6	1	- Para departamentos ou agências de marketing que desejam controlar o andamento das postagens em redes sociais\n- Receba avisos sobre postagens a serem realizadas\n- Visualize o andamento do post desde sua criação até a sua divulgação\n- Controle o valor gasto em postagens patrocinadas\n- Anexe a arte ou documentação referente à postagem	t	1
\.


--
-- Data for Name: theme_dashboard_chart_configuration; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.theme_dashboard_chart_configuration (id, name, for_company, aggregation_type_id, chart_type_id, form_id, label_field_id, number_format_type_id, theme_id, value_field_id) FROM stdin;
\.


--
-- Data for Name: theme_field; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.theme_field (id, created_at, updated_at, name, label_name, placeholder, required, "order", label_is_hidden, form_id, form_field_as_option_id, type_id, field_is_hidden, is_unique, number_configuration_mask, date_configuration_auto_create, date_configuration_auto_update, date_configuration_date_format_type_id, period_configuration_period_interval_type_id, formula_configuration, number_configuration_allow_negative, number_configuration_allow_zero, number_configuration_number_format_type_id, uuid, is_long_text_rich_text) FROM stdin;
452	2019-08-25 18:04:10.499+00	2021-04-18 04:12:45.158993+00	anexo_1	Anexo	\N	f	0	f	189	\N	6	f	f	\N	f	f	\N	\N	\N	t	t	\N	bb03630b-1bff-4ac4-ab91-be1810f730fc	f
431	2019-08-22 02:28:21.806+00	2021-04-18 04:12:44.95446+00	numerodoquarto	Número do quarto	\N	t	0	f	178	\N	1	f	f	\N	f	f	\N	\N	\N	t	t	\N	f0b23309-86b0-409c-8907-d9089eaa8818	f
9	2019-07-17 13:33:14.428537+00	2021-04-18 04:12:44.967371+00	motivodeperda	Motivo de Perda	\N	f	0	f	5	\N	4	f	f	\N	f	f	\N	\N	\N	t	t	\N	b2caebc3-b8c1-40c3-b439-85cbdf506570	f
11	2019-07-17 13:33:14.507011+00	2021-04-18 04:12:44.969483+00	datadeatualizacao	Data de atualização	\N	f	0	f	6	\N	3	f	f	\N	f	f	\N	\N	\N	t	t	\N	3f766da0-4144-404a-a49d-9f1fb0030687	f
13	2019-07-17 13:33:14.607431+00	2021-04-18 04:12:44.971425+00	anexo	Anexo	\N	f	0	t	7	\N	6	f	f	\N	f	f	\N	\N	\N	t	t	\N	9c910572-371a-4f46-a7cc-a46c50de1f5d	f
351	2019-08-20 00:12:31.341+00	2021-04-18 04:12:44.973282+00	cliente_2	Cliente	\N	t	0	f	143	359	5	f	f	\N	f	f	\N	\N	\N	t	t	\N	fca4e552-4941-454a-a7b9-5e48c8b4ecd5	f
355	2019-08-20 00:12:31.408+00	2021-04-18 04:12:44.97513+00	motivodeperda_1	Motivo de Perda	\N	t	0	f	144	\N	4	f	f	\N	f	f	\N	\N	\N	t	t	\N	0091e77e-5b4f-4d96-9283-95c842f14282	f
357	2019-08-20 00:12:31.434+00	2021-04-18 04:12:44.97694+00	anexos	Anexos	\N	f	0	t	145	\N	6	f	f	\N	f	f	\N	\N	\N	t	t	\N	05750678-142b-45f8-adf4-ac92d3cfd400	f
358	2019-08-20 00:12:31.448+00	2021-04-18 04:12:44.97883+00	historico_1	Histórico	\N	f	0	f	146	\N	7	f	f	\N	f	f	\N	\N	\N	t	t	\N	afc517ce-5aec-4294-8b84-86ff89b8be04	f
359	2019-08-20 00:12:31.492+00	2021-04-18 04:12:44.980709+00	nomedocliente_1	Nome do Cliente	\N	t	0	f	148	\N	2	f	f	\N	f	f	\N	\N	\N	t	t	\N	476b9c3c-bbde-421f-b22c-83baf91cd7ef	f
363	2019-08-20 01:47:34.99+00	2021-04-18 04:12:44.982586+00	cliente_2	Cliente	\N	t	0	f	150	376	5	f	f	\N	f	f	\N	\N	\N	t	t	\N	ef389443-48dd-4c94-87c0-6836e757e277	f
372	2019-08-20 01:47:35.189+00	2021-04-18 04:12:44.984394+00	motivodeperda_1	Motivo de Perda	\N	t	0	f	152	\N	4	f	f	\N	f	f	\N	\N	\N	t	t	\N	2df8bcc6-9b1f-4e5a-b3d1-6ea1d13ecca1	f
374	2019-08-20 01:47:35.215+00	2021-04-18 04:12:44.98628+00	anexo_1	Anexo	\N	f	0	t	153	\N	6	f	f	\N	f	f	\N	\N	\N	t	t	\N	30cbbd39-5871-41ba-a3d8-666b9b09af46	f
375	2019-08-20 01:47:35.231+00	2021-04-18 04:12:44.988125+00	observacao	Observação	\N	f	0	t	154	\N	7	f	f	\N	f	f	\N	\N	\N	t	t	\N	75a3e64d-b485-4226-8ee3-5074a55a02ed	f
459	2019-08-25 19:18:33.621+00	2021-04-18 04:12:44.990229+00	data	Data	\N	t	0	f	193	\N	3	f	f	\N	f	f	1	\N	\N	t	t	\N	35097a63-cd16-443d-bf5c-45580b41c69b	f
461	2019-08-25 19:18:33.655+00	2021-04-18 04:12:44.992072+00	anexo_2	Anexo	\N	f	0	f	194	\N	6	f	f	\N	f	f	\N	\N	\N	t	t	\N	99c78a5c-6c72-47b0-9d8b-ea0aae1c3e8c	f
1	2019-07-17 00:03:47.559+00	2021-04-18 04:12:44.99389+00	empty_field	Clique no campo para editar	\N	f	0	f	2	\N	2	f	f	\N	f	f	\N	\N	\N	t	t	\N	ba3a8767-1d82-40a3-bf29-416e657723ce	f
467	2019-08-25 19:55:22.288+00	2021-04-18 04:12:44.995842+00	comentariodependencia	Comentário de Pendência	\N	f	0	f	197	\N	7	f	f	\N	f	f	\N	\N	\N	t	t	\N	35e5937f-474e-4e06-8b8d-c14115373402	f
468	2019-08-25 19:55:22.308+00	2021-04-18 04:12:44.99771+00	anexo_1	Anexo	\N	f	0	t	198	\N	6	f	f	\N	f	f	\N	\N	\N	t	t	\N	019281fb-4317-451c-b889-261a657b380f	f
335	2019-08-19 02:28:28.616+00	2021-04-18 04:12:44.999716+00	nome_1	Nome	\N	t	0	f	135	347	5	f	f	\N	f	f	\N	\N	\N	t	t	\N	aac89477-49bc-4f36-a991-a6e4df160711	f
340	2019-08-19 02:28:28.693+00	2021-04-18 04:12:45.001532+00	vencimentodaapolice	Vencimento da Apólice	\N	t	0	f	136	\N	3	f	f	\N	f	f	1	\N	\N	t	t	\N	bf8429c4-e293-4dcc-b56d-592a39e91d80	f
342	2019-08-19 02:28:28.724+00	2021-04-18 04:12:45.010702+00	motivodeperda_1	Motivo de Perda	\N	t	0	f	137	\N	4	f	f	\N	f	f	\N	\N	\N	t	t	\N	640c3421-73dd-4580-be0e-d0d82f4e5861	f
344	2019-08-19 02:28:28.757+00	2021-04-18 04:12:45.108887+00	seguradora	Seguradora	\N	f	0	f	138	\N	4	f	f	\N	f	f	\N	\N	\N	t	t	\N	17bb83f9-1cc6-4d0b-a2bf-65678d2e336e	f
346	2019-08-19 02:28:28.786+00	2021-04-18 04:12:45.14914+00	historico_1	Histórico	\N	f	0	t	139	\N	7	f	f	\N	f	f	\N	\N	\N	t	t	\N	926d6f95-e11b-4c60-b133-84a6b5b8a776	f
347	2019-08-19 02:28:28.837+00	2021-04-18 04:12:45.151266+00	nomedosegurado	Nome do Segurado	\N	t	0	f	141	\N	2	f	f	\N	f	f	\N	\N	\N	t	t	\N	da4722b0-9b8e-4836-a262-7a31289eff59	f
421	2019-08-22 00:58:54.928+00	2021-04-18 04:12:45.153106+00	tarefa	Tarefa	\N	f	0	f	175	\N	2	f	f	\N	f	f	\N	\N	\N	t	t	\N	e711adbb-f280-47d5-bd37-e0b0d94f9b30	f
425	2019-08-22 02:28:21.653+00	2021-04-18 04:12:45.155023+00	fornecedor	Fornecedor	Insira o nome do fornecedor responsável	f	0	f	177	433	5	f	f	\N	f	f	\N	\N	\N	t	t	\N	73003aa6-d0bd-4830-8688-e768396ad9a6	f
449	2019-08-25 18:04:10.442+00	2021-04-18 04:12:45.157129+00	areadeatuacao	Área de Atuação	\N	t	0	f	188	\N	4	f	f	\N	f	f	\N	\N	\N	t	t	\N	469e1d98-7ef4-4603-b66f-1688592c617f	f
453	2019-08-25 19:18:33.495+00	2021-04-18 04:12:45.16081+00	nomedocolaborador	Nome do Colaborador	\N	t	0	f	191	\N	2	f	f	\N	f	f	\N	\N	\N	t	t	\N	22e9a6ec-0c4d-47d5-9f3f-2e66ba13dfd0	f
456	2019-08-25 19:18:33.553+00	2021-04-18 04:12:45.162619+00	motivo	Motivo	\N	t	0	f	192	\N	4	f	f	\N	f	f	\N	\N	\N	t	t	\N	98f4970e-0959-456e-b84b-6e05663481a9	f
376	2019-08-20 01:47:35.275+00	2021-04-18 04:12:45.164496+00	nomedocliente_1	Nome do Cliente	\N	t	0	f	156	\N	2	f	f	\N	f	f	\N	\N	\N	t	t	\N	8d2dd36e-fc91-4dec-a1b1-64adbf1e821d	f
380	2019-08-20 01:47:35.313+00	2021-04-18 04:12:45.166325+00	tipodeimovel	Tipo de Imóvel	\N	t	0	f	157	\N	4	f	f	\N	f	f	\N	\N	\N	t	t	\N	f298dcf2-6ced-44d0-acbe-15811b6c7976	f
399	2019-08-22 00:41:59.511+00	2021-04-18 04:12:45.168188+00	datadavisita	Data da Visita	\N	t	0	f	164	\N	3	f	f	\N	f	f	1	\N	\N	t	t	\N	645d3ef1-1677-434b-bd02-a96c0181d4f9	f
400	2019-08-22 00:41:59.545+00	2021-04-18 04:12:45.171095+00	motivodeperda_1	Motivo de Perda	\N	t	0	f	165	\N	4	f	f	\N	f	f	\N	\N	\N	t	t	\N	87332611-8d0a-4d41-b2e6-851465e09715	f
402	2019-08-22 00:41:59.6+00	2021-04-18 04:12:45.173699+00	observacoes	Observações	\N	f	0	t	166	\N	7	f	f	\N	f	f	\N	\N	\N	t	t	\N	a087ab58-2060-4f26-8c64-2621a5539206	f
403	2019-08-22 00:41:59.691+00	2021-04-18 04:12:45.175555+00	nomedocliente_1	Nome do Cliente	\N	t	0	f	168	\N	2	f	f	\N	f	f	\N	\N	\N	t	t	\N	9de5d783-ff51-4d12-867f-bddadeeeca38	f
407	2019-08-22 00:41:59.788+00	2021-04-18 04:12:45.177412+00	capitalmaximo	Capital máximo	Insira até quanto o cliente esta disposto à investir	t	0	f	169	\N	1	f	f	\N	f	f	\N	\N	\N	t	t	\N	ac3da2e9-165c-44c6-931f-ad78ea421c95	f
412	2019-08-22 00:41:59.907+00	2021-04-18 04:12:45.179262+00	documentacao	Documentação	\N	f	0	t	170	\N	6	f	f	\N	f	f	\N	\N	\N	t	t	\N	5430332a-bec4-46a7-b6d1-265e879ebc5f	f
413	2019-08-22 00:42:00.077+00	2021-04-18 04:12:45.18111+00	nomedesteimovel	Nome deste imóvel	Inisra um nome para este imóvel	t	0	f	172	\N	2	f	f	\N	f	f	\N	\N	\N	t	t	\N	d2eeace2-04ac-423e-8905-a6a57ea30ea0	f
418	2019-08-22 00:42:00.197+00	2021-04-18 04:12:45.182988+00	nomedoproprietario	Nome do proprietário	\N	t	0	f	173	\N	2	f	f	\N	f	f	\N	\N	\N	t	t	\N	ce60fa06-03dd-46ce-9be2-cdc7e10d93d4	f
367	2019-08-20 01:47:35.135+00	2021-04-18 04:12:45.184853+00	capacidadekwp	Capacidade kwp	\N	f	0	f	151	\N	1	f	f	\N	f	f	\N	\N	\N	t	t	\N	6696fdba-c87a-4d7c-bfd3-3a404358212d	f
386	2019-08-21 01:27:57.319+00	2021-04-18 04:12:45.186667+00	cliente_2	Cliente	\N	t	0	f	159	\N	2	f	f	\N	f	f	\N	\N	\N	t	t	\N	356b9600-8a22-4414-8112-26b342db4bbf	f
392	2019-08-21 01:27:57.4+00	2021-04-18 04:12:45.188493+00	anexos	Anexos	\N	f	0	t	160	\N	6	f	f	\N	f	f	\N	\N	\N	t	t	\N	40bf8d10-2b09-4200-bae0-e2dfda7333fb	f
393	2019-08-21 01:27:57.413+00	2021-04-18 04:12:45.19038+00	observacoes	Observações	\N	f	0	t	161	\N	7	f	f	\N	f	f	\N	\N	\N	t	t	\N	996fcd9e-ec50-4cee-9748-532198902db2	f
394	2019-08-22 00:41:59.376+00	2021-04-18 04:12:45.192345+00	imovel	Imóvel	\N	t	0	f	163	413	5	f	f	\N	f	f	\N	\N	\N	t	t	\N	6210fff7-d3c5-4aa5-8cbf-61ad6cd809e9	f
462	2019-08-25 19:55:22.185+00	2021-04-18 04:12:45.194266+00	atividade_1	Atividade	Descreva brevemente a atividade a ser realizada	t	0	f	196	\N	7	f	f	\N	f	f	\N	\N	\N	t	t	\N	b00df87b-b53a-4f6c-b2d7-c8c9a4cdf2da	f
469	2019-08-25 19:55:22.327+00	2021-04-18 04:12:45.196343+00	datadohistorico	Data do histórico	\N	f	0	f	199	\N	3	f	f	\N	f	f	1	\N	\N	t	t	\N	c909cea0-d861-4f6d-8527-5fc249271a03	f
2	2019-07-17 13:33:14.049864+00	2021-04-18 04:12:45.198291+00	nomedocliente	Nome do Cliente	\N	f	0	f	4	\N	2	f	f	\N	f	f	\N	\N	\N	t	t	\N	08fd2c10-aaf7-472c-9c72-4ebcebd206be	f
432	2019-08-22 02:28:21.828+00	2021-04-18 04:12:45.200188+00	observacoes	Observações	Insira observações importantes sobre o serviço	f	0	f	179	\N	7	f	f	\N	f	f	\N	\N	\N	t	t	\N	27a740c0-0554-4cfc-9da7-74e48babb904	f
433	2019-08-22 02:28:21.932+00	2021-04-18 04:12:45.202126+00	nomedofornecedor	Nome do fornecedor	\N	t	0	f	181	\N	2	f	f	\N	f	f	\N	\N	\N	t	t	\N	e8708479-e7fa-4421-a6c8-3e557b588d67	f
437	2019-08-25 18:04:10.146+00	2021-04-18 04:12:45.204101+00	candidato	Candidato	\N	t	0	f	183	445	5	f	f	\N	f	f	\N	\N	\N	t	t	\N	4998a506-3d94-4a19-8cac-0055ed81303d	f
442	2019-08-25 18:04:10.281+00	2021-04-18 04:12:45.205964+00	datadaentrevista	Data da Entrevista	\N	t	0	f	184	\N	3	f	f	\N	f	f	1	\N	\N	t	t	\N	e7a971c5-09c3-4250-a68e-1e9f51efaa24	f
444	2019-08-25 18:04:10.316+00	2021-04-18 04:12:45.207765+00	observacoes	Observações	\N	f	0	t	185	\N	7	f	f	\N	f	f	\N	\N	\N	t	t	\N	708768de-9fc5-443d-84b5-0b73133e3658	f
445	2019-08-25 18:04:10.386+00	2021-04-18 04:12:45.209591+00	nomedocandidato_1	Nome do Candidato	\N	t	0	f	187	\N	2	f	f	\N	f	f	\N	\N	\N	t	t	\N	e9bca541-d28e-4862-9b6d-8b528b19943f	f
475	2019-08-27 00:44:26.327+00	2021-04-18 04:12:45.211528+00	comprovantes	Comprovantes	\N	f	0	t	202	\N	6	f	f	\N	f	f	\N	\N	\N	t	t	\N	173e8f10-855e-4642-a9f9-50273d959af0	f
476	2019-08-27 01:31:18.519+00	2021-04-18 04:12:45.21345+00	cliente_2	Cliente	\N	f	0	f	204	484	5	f	f	\N	f	f	\N	\N	\N	t	t	\N	ce1b2afe-1f3e-45f2-bb45-0c872623725e	f
482	2019-08-27 01:31:18.684+00	2021-04-18 04:12:45.215321+00	datadepagamento	Data de pagamento	\N	t	0	t	205	\N	3	f	f	\N	f	f	1	\N	\N	t	t	\N	2c5acb42-7cec-4608-96d3-eff848ea2271	f
483	2019-08-27 01:31:18.709+00	2021-04-18 04:12:45.217164+00	anexos	Anexos	\N	f	0	t	206	\N	6	f	f	\N	f	f	\N	\N	\N	t	t	\N	3c6e73bb-4c5a-467c-a48c-554cd1dd64bd	f
484	2019-08-27 01:31:18.801+00	2021-04-18 04:12:45.218972+00	nomedocliente_1	Nome do Cliente	\N	t	0	f	208	\N	2	f	f	\N	f	f	\N	\N	\N	t	t	\N	dd337864-cd26-419c-bd4b-21d6278e2e14	f
488	2019-08-27 02:28:02.048+00	2021-04-18 04:12:45.220756+00	titulodopost	Título do Post	\N	t	0	f	210	\N	2	f	f	\N	f	f	\N	\N	\N	t	t	\N	50753f5b-0fcf-4261-957c-900678a3d58f	f
493	2019-08-27 02:28:02.347+00	2021-04-18 04:12:45.222696+00	valor	Valor	Insira o valor do impulsionamento	t	0	f	211	\N	1	f	f	\N	f	f	\N	\N	\N	t	t	\N	dc4d0d3b-b110-4558-a8c3-74c5612d132c	f
494	2019-08-27 02:28:02.375+00	2021-04-18 04:12:45.22458+00	observacoes	Observações	\N	f	0	t	212	\N	7	f	f	\N	f	f	\N	\N	\N	t	t	\N	197ff320-dc78-4799-b999-0805beae6262	f
495	2019-08-27 02:28:02.406+00	2021-04-18 04:12:45.226374+00	documentos	Documentos	\N	f	0	t	213	\N	6	f	f	\N	f	f	\N	\N	\N	t	t	\N	2f2905ea-250b-4689-9a7e-35f5a6162b8f	f
360	2019-08-20 00:12:31.5+00	2021-04-18 04:12:45.228326+00	email_2	Email	\N	f	1	f	148	\N	10	f	f	\N	f	f	\N	\N	\N	t	t	\N	a21bc2fc-d42b-4c8d-abbd-f6a4ee0b6896	f
348	2019-08-19 02:28:28.847+00	2021-04-18 04:12:45.230183+00	cpfcnpj	CPF/ CNPJ	\N	f	1	f	141	\N	1	f	f	\N	f	f	\N	\N	\N	t	t	\N	67343916-4349-4d9d-8087-69a203432fa3	f
345	2019-08-19 02:28:28.772+00	2021-04-18 04:12:45.232079+00	cotacao	Cotação	\N	f	1	f	138	\N	6	f	f	\N	f	f	\N	\N	\N	t	t	\N	e4bcccda-9511-4576-b3ee-378b0d8bcf4a	f
434	2019-08-22 02:28:21.948+00	2021-04-18 04:12:45.234014+00	telefone_1	Telefone	\N	f	1	f	181	\N	1	f	f	\N	f	f	\N	\N	\N	t	t	\N	09ece783-329c-464f-9417-a846ce6913fe	f
443	2019-08-25 18:04:10.297+00	2021-04-18 04:12:45.235869+00	horario	Horário	Insira o horário marcado. Ex: 9h às 10h	t	1	f	184	\N	2	f	f	\N	f	f	\N	\N	\N	t	t	\N	80acb6dc-38be-4448-8892-dfd46a7c8fdb	f
477	2019-08-27 01:31:18.539+00	2021-04-18 04:12:45.241391+00	produto_1	Produto	\N	t	1	f	204	\N	4	f	f	\N	f	f	\N	\N	\N	t	t	\N	485f3a41-14c8-4c6e-ab30-70a1a24a37da	f
368	2019-08-20 01:47:35.145+00	2021-04-18 04:12:45.243426+00	producaomensalkwh	Produção Mensal kwh	\N	f	1	f	151	\N	1	f	f	\N	f	f	\N	\N	\N	t	t	\N	52abc37b-2d3c-4b85-bbfe-5d28f0006cde	f
377	2019-08-20 01:47:35.283+00	2021-04-18 04:12:45.245343+00	telefone_1	Telefone	\N	f	1	f	156	\N	1	f	f	\N	f	f	\N	\N	\N	t	t	\N	bf6eb23f-0bdf-4881-8f27-5142f662d40c	f
381	2019-08-20 01:47:35.324+00	2021-04-18 04:12:45.247202+00	tipodefase	Tipo de Fase	\N	t	1	f	157	\N	4	f	f	\N	f	f	\N	\N	\N	t	t	\N	ab2bf61c-2be4-4b7e-92b1-264b0d2f7b93	f
454	2019-08-25 19:18:33.508+00	2021-04-18 04:12:45.249044+00	dapartamento	Dapartamento	\N	t	1	f	191	\N	4	f	f	\N	f	f	\N	\N	\N	t	t	\N	0d81a468-3c85-4317-906b-19adfbf915cd	f
356	2019-08-20 00:12:31.421+00	2021-04-18 04:12:45.250909+00	comentarios	Comentários	\N	f	1	f	144	\N	7	f	f	\N	f	f	\N	\N	\N	t	t	\N	1d01aaa1-e741-43b4-ab09-c16adc5308ef	f
352	2019-08-20 00:12:31.351+00	2021-04-18 04:12:45.252787+00	previsaodefechamento_1	Previsão de Fechamento	\N	t	1	f	143	\N	3	f	f	\N	f	f	1	\N	\N	t	t	\N	9b8afdd8-86f6-4cd8-a6ca-a59e7b39a7b0	f
14	2019-07-17 13:33:14.736639+00	2021-04-18 04:12:45.254635+00	nomedocliente_1	Nome do Cliente	\N	f	1	f	9	\N	2	f	f	\N	f	f	\N	\N	\N	t	t	\N	02360200-ea83-4e4a-8585-392f0e8b247a	f
12	2019-07-17 13:33:14.541432+00	2021-04-18 04:12:45.256544+00	historico	Histórico	\N	f	1	f	6	\N	7	f	f	\N	f	f	\N	\N	\N	t	t	\N	6fd754f5-cc99-4e76-a400-5f6cf03761f2	f
3	2019-07-17 13:33:14.076943+00	2021-04-18 04:12:45.258338+00	responsavel	Responsável	\N	f	1	f	4	\N	4	f	f	\N	f	f	\N	\N	\N	t	t	\N	37caba7a-c648-4bd9-965b-2320560febdd	f
343	2019-08-19 02:28:28.739+00	2021-04-18 04:12:45.260229+00	proximaoportunidade	Próxima Oportunidade	Insira a data de vencimento da apólice	f	1	f	137	\N	3	f	f	\N	f	f	1	\N	\N	t	t	\N	d657eefd-1236-4cdf-a026-6d5e59eb0843	f
10	2019-07-17 13:33:14.463787+00	2021-04-18 04:12:45.26207+00	detalhedomotivo	Detalhe do motivo	\N	f	1	f	5	\N	7	f	f	\N	f	f	\N	\N	\N	t	t	\N	f599c61f-17b3-4ba8-8900-a0cb2da4c33c	f
485	2019-08-27 01:31:18.816+00	2021-04-18 04:12:45.263915+00	cnpjcpf	CNPJ/ CPF	\N	t	1	f	208	\N	1	f	f	\N	f	f	\N	\N	\N	t	t	\N	40ed94e8-33a5-4c25-ae2d-adbf5d9e57c2	f
419	2019-08-22 00:42:00.214+00	2021-04-18 04:12:45.265759+00	telefone_1	Telefone	\N	t	1	f	173	\N	1	f	f	\N	f	f	\N	\N	\N	t	t	\N	976c2bfa-a29e-4690-9f32-660ebae49f43	f
446	2019-08-25 18:04:10.398+00	2021-04-18 04:12:45.26763+00	email_2	Email	\N	t	1	f	187	\N	10	f	f	\N	f	f	\N	\N	\N	t	t	\N	6663f7e9-a2ae-4431-83b7-ff360a1df522	f
401	2019-08-22 00:41:59.57+00	2021-04-18 04:12:45.269455+00	comentarios	Comentários	\N	f	1	f	165	\N	7	f	f	\N	f	f	\N	\N	\N	t	t	\N	a55aee1f-f77a-4a38-83c8-1ac12cc70434	f
457	2019-08-25 19:18:33.571+00	2021-04-18 04:12:45.271413+00	comentarios	Comentários	\N	f	1	f	192	\N	7	f	f	\N	f	f	\N	\N	\N	t	t	\N	3e2e9fc2-3ffe-45f6-9913-f4e81b908b88	f
489	2019-08-27 02:28:02.101+00	2021-04-18 04:12:45.273314+00	redesocial	Rede Social	Insira a rede social onde será postado	t	1	f	210	\N	11	f	f	\N	f	f	\N	\N	\N	t	t	\N	cd980889-50e1-43b7-b68b-c9c7ef5bfa20	f
404	2019-08-22 00:41:59.723+00	2021-04-18 04:12:45.275147+00	email_3	Email	\N	t	1	f	168	\N	10	f	f	\N	f	f	\N	\N	\N	t	t	\N	692aa1b9-4af2-454e-a936-2df751ff8ed2	f
426	2019-08-22 02:28:21.671+00	2021-04-18 04:12:45.276995+00	sistema	Sistema	Insira o tipo de sistema com problema	t	1	f	177	\N	4	f	f	\N	f	f	\N	\N	\N	t	t	\N	8fc03122-aac9-421e-b5ab-a9da09843e0d	f
341	2019-08-19 02:28:28.702+00	2021-04-18 04:12:45.27885+00	seguradoraescolhida	Seguradora Escolhida	Insira a seguradora escolhida	t	1	f	136	\N	4	f	f	\N	f	f	\N	\N	\N	t	t	\N	b7aeca86-ce49-4ef4-a968-6a388acf7ae4	f
450	2019-08-25 18:04:10.461+00	2021-04-18 04:12:45.28076+00	nivel	Nível	\N	t	1	f	188	\N	4	f	f	\N	f	f	\N	\N	\N	t	t	\N	7119332b-fb49-41f7-bff9-2b4a6d611373	f
408	2019-08-22 00:41:59.804+00	2021-04-18 04:12:45.282715+00	interesse	Interesse	\N	t	1	f	169	\N	4	f	f	\N	f	f	\N	\N	\N	t	t	\N	641f0243-e355-4506-b0c5-acfa1a07b914	f
336	2019-08-19 02:28:28.627+00	2021-04-18 04:12:45.284609+00	produto_1	Produto	\N	t	1	f	135	\N	4	f	f	\N	f	f	\N	\N	\N	t	t	\N	e47cc3d4-fe70-4556-b516-a0cb2d445e2f	f
463	2019-08-25 19:55:22.198+00	2021-04-18 04:12:45.286562+00	tipodedesenvolvimento_1	Tipo de desenvolvimento	\N	t	1	f	196	\N	4	f	f	\N	f	f	\N	\N	\N	t	t	\N	3bdb2fcd-5ec4-452f-bf0b-0c3c1f7d3396	f
460	2019-08-25 19:18:33.636+00	2021-04-18 04:12:45.28846+00	horario_1	Horário	Insira o horário da entrevista. Ex: 10h às 11h	t	1	f	193	\N	2	f	f	\N	f	f	\N	\N	\N	t	t	\N	61f21959-1ce0-43d7-a7e4-15432eedada0	f
470	2019-08-25 19:55:22.339+00	2021-04-18 04:12:45.290377+00	comentarios	Comentários	\N	f	1	f	199	\N	7	f	f	\N	f	f	\N	\N	\N	t	t	\N	1ed94a7f-ab48-4622-b6fd-320d3ac162ea	f
471	2019-08-27 00:44:26.243+00	2021-04-18 04:12:45.292246+00	tipodedespesa	Tipo de Despesa	\N	t	1	f	201	\N	4	f	f	\N	f	f	\N	\N	\N	t	t	\N	d865a57d-5c78-44bb-87e2-6254486a9393	f
414	2019-08-22 00:42:00.094+00	2021-04-18 04:12:45.295608+00	endereco_1	Endereço	\N	t	1	f	172	\N	2	f	f	\N	f	f	\N	\N	\N	t	t	\N	b2914934-9259-4df2-b69a-6c1645593b15	f
438	2019-08-25 18:04:10.168+00	2021-04-18 04:12:45.297565+00	areacontratante	Área Contratante	\N	t	1	f	183	\N	4	f	f	\N	f	f	\N	\N	\N	t	t	\N	5a028d06-de35-4ea6-9c9c-6a8e6a4bed55	f
373	2019-08-20 01:47:35.202+00	2021-04-18 04:12:45.299435+00	comentarios	Comentários	\N	f	1	f	152	\N	7	f	f	\N	f	f	\N	\N	\N	t	t	\N	b6553bc7-1d88-4e11-94b6-d7e54e7d3577	f
364	2019-08-20 01:47:35.004+00	2021-04-18 04:12:45.301295+00	previsaodefechamento_1	Previsão de Fechamento	\N	t	1	f	150	\N	3	f	f	\N	f	f	1	\N	\N	t	t	\N	96a873ac-9e06-4017-a77d-319658baa7c8	f
422	2019-08-22 00:58:54.944+00	2021-04-18 04:12:45.303177+00	prioridade_2	Prioridade	\N	f	1	f	175	\N	4	f	f	\N	f	f	\N	\N	\N	t	t	\N	3c21c833-47e0-4ba7-b69b-07bdc9efa184	f
395	2019-08-22 00:41:59.396+00	2021-04-18 04:12:45.305092+00	cliente_2	Cliente	\N	t	1	f	163	403	5	f	f	\N	f	f	\N	\N	\N	t	t	\N	30758161-9b81-4952-b212-87f82d64e043	f
409	2019-08-22 00:41:59.825+00	2021-04-18 04:12:45.307029+00	prazoparafechamento	Prazo para Fechamento	Insira em quanto tempo o cliente deseja fechar negócio	t	2	f	169	\N	4	f	f	\N	f	f	\N	\N	\N	t	t	\N	83d517e6-df9a-4fe8-b4c6-74641ff6fc10	f
439	2019-08-25 18:04:10.203+00	2021-04-18 04:12:45.308999+00	cargopretendido	Cargo Pretendido	\N	t	2	f	183	\N	4	f	f	\N	f	f	\N	\N	\N	t	t	\N	8669d52b-bef9-4a75-a533-caba77ec1c70	f
451	2019-08-25 18:04:10.48+00	2021-04-18 04:12:45.310927+00	salarioatual	Salário Atual	\N	t	2	f	188	\N	1	f	f	\N	f	f	\N	\N	\N	t	t	\N	47040691-ee97-4c99-94ac-bf8fc504ddae	f
458	2019-08-25 19:18:33.583+00	2021-04-18 04:12:45.312928+00	status_4	Status	\N	t	2	f	192	\N	4	f	f	\N	f	f	\N	\N	\N	t	t	\N	9dbe8aec-ec89-4b09-83de-4653533a692d	f
365	2019-08-20 01:47:35.069+00	2021-04-18 04:12:45.315001+00	valor	Valor	Insira o valor desta oportunidade	t	2	f	150	\N	1	f	f	\N	f	f	\N	\N	\N	t	t	\N	265fbd3a-113f-41c7-84f8-dea0a0fe3d11	f
369	2019-08-20 01:47:35.153+00	2021-04-18 04:12:45.316931+00	areanecessaria	Àrea necessária	Valor em metros quadrados	f	2	f	151	\N	1	f	f	\N	f	f	\N	\N	\N	t	t	\N	e55e9897-0691-4f6a-83c0-5134077e93a9	f
378	2019-08-20 01:47:35.292+00	2021-04-18 04:12:45.318783+00	email_2	Email	\N	f	2	f	156	\N	10	f	f	\N	f	f	\N	\N	\N	t	t	\N	ed90b6a0-ac7f-4d5f-a0ed-4cb1aebc9053	f
486	2019-08-27 01:31:18.834+00	2021-04-18 04:12:45.320722+00	email_2	Email	\N	f	2	f	208	\N	10	f	f	\N	f	f	\N	\N	\N	t	t	\N	85c77e7c-68dd-4d80-ba28-7991689c372a	f
447	2019-08-25 18:04:10.411+00	2021-04-18 04:12:45.322554+00	telefone_1	Telefone	\N	t	2	f	187	\N	1	f	f	\N	f	f	\N	\N	\N	t	t	\N	cac3bd00-a71f-462e-931a-31bf4739360c	f
405	2019-08-22 00:41:59.738+00	2021-04-18 04:12:45.324426+00	telefone_2	Telefone	\N	t	2	f	168	\N	1	f	f	\N	f	f	\N	\N	\N	t	t	\N	cc4a6449-111b-489c-a30d-4529221b87c2	f
415	2019-08-22 00:42:00.111+00	2021-04-18 04:12:45.326226+00	bairro	Bairro	\N	t	2	f	172	\N	2	f	f	\N	f	f	\N	\N	\N	t	t	\N	b9ac6e32-e5a0-4d26-bfc1-47731cefcf51	f
472	2019-08-27 00:44:26.285+00	2021-04-18 04:12:45.328138+00	valor	Valor	\N	t	2	f	201	\N	1	f	f	\N	f	f	\N	\N	\N	t	t	\N	5354be7a-6d7d-42c1-8eb9-b19997544141	f
349	2019-08-19 02:28:28.856+00	2021-04-18 04:12:45.329988+00	telefone_1	Telefone	\N	f	2	f	141	\N	1	f	f	\N	f	f	\N	\N	\N	t	t	\N	82c1c039-4043-4017-8d46-c055e09fd2b9	f
353	2019-08-20 00:12:31.359+00	2021-04-18 04:12:45.331948+00	valor	Valor	\N	t	2	f	143	\N	1	f	f	\N	f	f	\N	\N	\N	t	t	\N	6389503a-f264-4ab8-8cf0-647dd53a3160	f
361	2019-08-20 00:12:31.509+00	2021-04-18 04:12:45.33387+00	telefone_1	Telefone	\N	f	2	f	148	\N	1	f	f	\N	f	f	\N	\N	\N	t	t	\N	72b98c9f-d2c9-4aa5-b22c-9d8e1aacfa31	f
382	2019-08-20 01:47:35.339+00	2021-04-18 04:12:45.335732+00	tipodesistema	Tipo de Sistema	\N	t	2	f	157	\N	4	f	f	\N	f	f	\N	\N	\N	t	t	\N	71d6536c-746b-4053-a3c4-bd8c129d1b98	f
4	2019-07-17 13:33:14.130437+00	2021-04-18 04:12:45.337777+00	produto	Produto	\N	f	2	f	4	\N	4	f	f	\N	f	f	\N	\N	\N	t	t	\N	ab6c0a9c-69b0-46eb-9c3f-78dd5027e3d8	f
387	2019-08-21 01:27:57.329+00	2021-04-18 04:12:45.339896+00	nomedosegurado	Nome do Segurado	\N	t	2	f	159	\N	2	f	f	\N	f	f	\N	\N	\N	t	t	\N	537124e1-57e2-404a-a677-3c16c0ef48b2	f
15	2019-07-17 13:33:14.767756+00	2021-04-18 04:12:45.341788+00	telefone	Telefone	\N	f	2	f	9	\N	2	f	f	\N	f	f	\N	\N	\N	t	t	\N	9e184246-d870-4df4-b112-8238c34a466a	f
396	2019-08-22 00:41:59.416+00	2021-04-18 04:12:45.3437+00	previsaodefechamento_1	Previsão de Fechamento	\N	t	2	f	163	\N	3	f	f	\N	f	f	1	\N	\N	t	t	\N	228e49ad-ae75-4d9d-884f-92bd1c9baa24	f
455	2019-08-25 19:18:33.527+00	2021-04-18 04:12:45.348807+00	cargo	Cargo	\N	t	2	f	191	\N	4	f	f	\N	f	f	\N	\N	\N	t	t	\N	d9b5be81-3acf-4b12-a041-afd84ba64f5d	f
478	2019-08-27 01:31:18.57+00	2021-04-18 04:12:45.350768+00	valor	Valor	\N	t	2	f	204	\N	1	f	f	\N	f	f	\N	\N	\N	t	t	\N	0ab3f899-9326-4748-a321-140d20f13c48	f
464	2019-08-25 19:55:22.216+00	2021-04-18 04:12:45.352656+00	prioridade_2	Prioridade	\N	t	2	f	196	\N	4	f	f	\N	f	f	\N	\N	\N	t	t	\N	c7083283-b31e-48a9-9a0c-ca29b68c5072	f
337	2019-08-19 02:28:28.643+00	2021-04-18 04:12:45.35447+00	iniciodevigencia	Início de Vigência	\N	t	2	f	135	\N	3	f	f	\N	f	f	1	\N	\N	t	t	\N	6bae5cfe-d18a-4502-ba0a-828476bb3ee8	f
435	2019-08-22 02:28:21.977+00	2021-04-18 04:12:45.356318+00	email_2	Email	\N	f	2	f	181	\N	10	f	f	\N	f	f	\N	\N	\N	t	t	\N	4fcbf4c0-12fb-4c7c-ae34-e117c8b9403b	f
420	2019-08-22 00:42:00.23+00	2021-04-18 04:12:45.358143+00	email_2	Email	\N	t	2	f	173	\N	10	f	f	\N	f	f	\N	\N	\N	t	t	\N	0f98e34a-ee74-4054-970d-1ac2996f53cd	f
490	2019-08-27 02:28:02.146+00	2021-04-18 04:12:45.359948+00	datadepostagem	Data de Postagem	Data postada ou de previsão	t	2	f	210	\N	3	f	f	\N	f	f	1	\N	\N	t	t	\N	99948ffd-cba6-485a-a4ef-41834ae6fe9e	f
423	2019-08-22 00:58:54.965+00	2021-04-18 04:12:45.361787+00	dataparaconclusao	Data para conclusão	\N	t	2	f	175	\N	3	f	f	\N	f	f	1	\N	\N	t	t	\N	a159bb01-ec67-4320-b609-58fbaa443311	f
427	2019-08-22 02:28:21.696+00	2021-04-18 04:12:45.36361+00	prioridade_2	Prioridade	Insira a prioridade para manutenção	t	2	f	177	\N	4	f	f	\N	f	f	\N	\N	\N	t	t	\N	7858bf6f-af56-4f8c-8b61-ee50efdfc580	f
5	2019-07-17 13:33:14.174457+00	2021-04-18 04:12:45.365423+00	premio	Prêmio	\N	f	3	f	4	\N	1	f	f	#.##0,00	f	f	\N	\N	\N	t	t	2	7964a419-9947-4fca-a85f-d77f73f94b2f	f
487	2019-08-27 01:31:18.85+00	2021-04-18 04:12:45.367264+00	telefone_1	Telefone	\N	t	3	f	208	\N	1	f	f	\N	f	f	\N	\N	\N	t	t	\N	f2c0f96e-79cb-4b17-abd4-8a0bed18303b	f
473	2019-08-27 00:44:26.297+00	2021-04-18 04:12:45.369066+00	datadepagamento	Data de Pagamento	\N	t	3	f	201	\N	3	f	f	\N	f	f	1	\N	\N	t	t	\N	7177f756-88ff-4b19-88c3-aa0e367ab0e3	f
338	2019-08-19 02:28:28.653+00	2021-04-18 04:12:45.370923+00	premio	Prêmio	Insira o prêmio da apólice	t	3	f	135	\N	1	f	f	\N	f	f	\N	\N	\N	t	t	\N	015a56f0-f33b-4a79-b37c-31cd8f662460	f
362	2019-08-20 00:12:31.518+00	2021-04-18 04:12:45.372719+00	endereco_1	Endereço	\N	f	3	f	148	\N	2	f	f	\N	f	f	\N	\N	\N	t	t	\N	4104f3c2-9ac0-4a9e-94b0-e98b688c2485	f
366	2019-08-20 01:47:35.087+00	2021-04-18 04:12:45.374547+00	status_3	Status	\N	t	3	f	150	\N	4	f	f	\N	f	f	\N	\N	\N	t	t	\N	33c9134a-1f34-4cfd-9321-716b8bbf3085	f
436	2019-08-22 02:28:21.991+00	2021-04-18 04:12:45.376378+00	tipodeservico	Tipo de serviço	Insira a especialização do fornecedor	t	3	f	181	\N	4	f	f	\N	f	f	\N	\N	\N	t	t	\N	7c1c563b-6e55-41a7-a26e-375cf8c4f60a	f
416	2019-08-22 00:42:00.128+00	2021-04-18 04:12:45.378219+00	cidade	Cidade	\N	t	3	f	172	\N	2	f	f	\N	f	f	\N	\N	\N	t	t	\N	c1b9bca8-62ec-4472-b459-e317734b3a19	f
397	2019-08-22 00:41:59.436+00	2021-04-18 04:12:45.380099+00	valorpotencial	Valor	Insira o valor desta negociação	t	3	f	163	\N	1	f	f	\N	f	f	\N	\N	\N	t	t	\N	78adba41-daaf-4720-84a2-b1fc6107007f	f
491	2019-08-27 02:28:02.19+00	2021-04-18 04:12:45.381926+00	status_3	Status	\N	t	3	f	210	\N	4	f	f	\N	f	f	\N	\N	\N	t	t	\N	2ad46e08-e472-43d5-9331-525ead5c9bdd	f
424	2019-08-22 00:58:54.979+00	2021-04-18 04:12:45.383742+00	status_3	Status	\N	t	3	f	175	\N	4	f	f	\N	f	f	\N	\N	\N	t	t	\N	588fc1a7-921b-448e-816f-ddf6280bfe14	f
410	2019-08-22 00:41:59.85+00	2021-04-18 04:12:45.385528+00	tipodeimovel	Tipo de imóvel	\N	t	3	f	169	\N	4	f	f	\N	f	f	\N	\N	\N	t	t	\N	2a450599-aab4-404e-97fb-794a8bde4cc3	f
440	2019-08-25 18:04:10.226+00	2021-04-18 04:12:45.387322+00	salariopretendido	Salário Pretendido	\N	t	3	f	183	\N	1	f	f	\N	f	f	\N	\N	\N	t	t	\N	ec0c7a54-dc20-44d6-9319-4eb075c52f41	f
465	2019-08-25 19:55:22.233+00	2021-04-18 04:12:45.389176+00	dataparaconclusao	Data para conclusão	\N	t	3	f	196	\N	3	f	f	\N	f	f	1	\N	\N	t	t	\N	e06e22b8-e0e8-4878-8c02-4aa7760251ba	f
479	2019-08-27 01:31:18.59+00	2021-04-18 04:12:45.391019+00	vencimentodafatura	Vencimento da Fatura	\N	t	3	f	204	\N	3	f	f	\N	f	f	1	\N	\N	t	t	\N	be7d837d-3bea-4b34-928a-8bd3aa44d6be	f
428	2019-08-22 02:28:21.724+00	2021-04-18 04:12:45.392873+00	valordamanutencao	Valor da manutenção	Insira o valor gasto ou previsto	f	3	f	177	\N	1	f	f	\N	f	f	\N	\N	\N	t	t	\N	6b281b5a-800f-4ad7-8cae-0175b7f669bf	f
406	2019-08-22 00:41:59.757+00	2021-04-18 04:12:45.394704+00	cpf	CPF	\N	f	3	f	168	\N	1	f	f	\N	f	f	\N	\N	\N	t	t	\N	15acac0c-fcd3-41a9-95bc-a7c3b3e76a9a	f
448	2019-08-25 18:04:10.423+00	2021-04-18 04:12:45.39657+00	idade_1	Idade	\N	t	3	f	187	\N	1	f	f	\N	f	f	\N	\N	\N	t	t	\N	ffca6fc5-5731-4287-b022-351b0962974a	f
379	2019-08-20 01:47:35.3+00	2021-04-18 04:12:45.398394+00	endereco_1	Endereço	\N	f	3	f	156	\N	2	f	f	\N	f	f	\N	\N	\N	t	t	\N	09a1808b-75db-47b0-94c0-6c54c1537e5e	f
370	2019-08-20 01:47:35.162+00	2021-04-18 04:12:45.400262+00	pesoestimado	Peso estimado	Insira o valor em kg por metro quadrado	f	3	f	151	\N	1	f	f	\N	f	f	\N	\N	\N	t	t	\N	c851d206-9c02-4cd3-bdc1-1c010bdaf25f	f
388	2019-08-21 01:27:57.339+00	2021-04-18 04:12:45.402076+00	numerodaapolice	Número da Apólice	\N	t	3	f	159	\N	1	f	f	\N	f	f	\N	\N	\N	t	t	\N	fbfb8e3d-1ee7-43b0-9505-ea1b8df2b0a8	f
16	2019-07-17 13:33:14.794458+00	2021-04-18 04:12:45.403893+00	email	Email	\N	f	3	f	9	\N	10	f	f	\N	f	f	\N	\N	\N	t	t	\N	ff6452e2-6f35-4784-b7f7-ec07856c4dd8	f
350	2019-08-19 02:28:28.864+00	2021-04-18 04:12:45.405717+00	email_2	E-mail	\N	f	3	f	141	\N	10	f	f	\N	f	f	\N	\N	\N	t	t	\N	fe332e2a-ae81-4e9f-ac5c-658477a5cc43	f
354	2019-08-20 00:12:31.37+00	2021-04-18 04:12:45.407606+00	status_3	Status	\N	t	3	f	143	\N	4	f	f	\N	f	f	\N	\N	\N	t	t	\N	639f7188-0dd1-45dd-9ea9-41ef4021da3c	f
383	2019-08-20 01:47:35.351+00	2021-04-18 04:12:45.409397+00	custoconsumomedio	Custo Consumo Médio	\N	f	3	f	157	\N	1	f	f	\N	f	f	\N	\N	\N	t	t	\N	f4ba2fa6-fb92-4012-8e03-fba9abd73173	f
384	2019-08-20 01:47:35.359+00	2021-04-18 04:12:45.411353+00	consumomediomensal	Consumo Médio Mensal	Insira o valor em Kwh	f	4	f	157	\N	1	f	f	\N	f	f	\N	\N	\N	t	t	\N	e414f594-d2e7-498d-a476-a809c6591a51	f
429	2019-08-22 02:28:21.739+00	2021-04-18 04:12:45.413443+00	status_3	Status	\N	t	4	f	177	\N	4	f	f	\N	f	f	\N	\N	\N	t	t	\N	248985d1-9e4b-46a0-8f95-67d7af6689ff	f
339	2019-08-19 02:28:28.662+00	2021-04-18 04:12:45.415278+00	status_3	Status	\N	t	4	f	135	\N	4	f	f	\N	f	f	\N	\N	\N	t	t	\N	c17364ac-18da-4c81-8b76-0898c9566a23	f
474	2019-08-27 00:44:26.309+00	2021-04-18 04:12:45.417939+00	observacoes	Observações	\N	f	4	f	201	\N	7	f	f	\N	f	f	\N	\N	\N	t	t	\N	a4a8fdcf-b53b-4b7f-8d36-478e830a98b0	f
389	2019-08-21 01:27:57.348+00	2021-04-18 04:12:45.41972+00	datadosinistro	Data do Sinistro	\N	t	4	f	159	\N	3	f	f	\N	f	f	1	\N	\N	t	t	\N	934a9061-4319-4f93-8a7d-c53709cc6427	f
398	2019-08-22 00:41:59.452+00	2021-04-18 04:12:45.421528+00	status_3	Status	\N	t	4	f	163	\N	4	f	f	\N	f	f	\N	\N	\N	t	t	\N	59afa830-8574-4939-9891-af56f34053f3	f
371	2019-08-20 01:47:35.172+00	2021-04-18 04:12:45.4233+00	quantidadedemodulos	Quantidade de módulos	\N	f	4	f	151	\N	1	f	f	\N	f	f	\N	\N	\N	t	t	\N	ede9dd34-3a6a-46ba-b9fd-c0a03ad0c355	f
411	2019-08-22 00:41:59.882+00	2021-04-18 04:12:45.425153+00	metragemdesejada	Metragem desejada	Insira valores em metros quadrados	t	4	f	169	\N	1	f	f	\N	f	f	\N	\N	\N	t	t	\N	5440805b-2801-483f-92d8-b51449c3c2cf	f
466	2019-08-25 19:55:22.249+00	2021-04-18 04:12:45.42699+00	status_3	Status	\N	t	4	f	196	\N	4	f	f	\N	f	f	\N	\N	\N	t	t	\N	c4e702f2-6b01-4f8d-9c47-621fa748de7f	f
6	2019-07-17 13:33:14.203826+00	2021-04-18 04:12:45.428841+00	previsaodefechamento	Previsão de fechamento	\N	f	4	f	4	\N	3	f	f	\N	f	f	\N	\N	\N	t	t	\N	5cc737f0-9e93-4d98-93b1-8ca11eb0c5f6	f
492	2019-08-27 02:28:02.28+00	2021-04-18 04:12:45.430667+00	tipodepostagem	Tipo de Postagem	\N	t	4	f	210	\N	4	f	f	\N	f	f	\N	\N	\N	t	t	\N	8a3fd023-3bf5-4a1f-a2ac-a02c1948affb	f
480	2019-08-27 01:31:18.61+00	2021-04-18 04:12:45.432456+00	metododepagamento	Método de Pagamento	\N	t	4	f	204	\N	4	f	f	\N	f	f	\N	\N	\N	t	t	\N	22e51689-f02b-4232-9887-9fa6a81d48a0	f
17	2019-07-17 13:33:14.825661+00	2021-04-18 04:12:45.434285+00	endereco	Endereço	\N	f	4	f	9	\N	2	f	f	\N	f	f	\N	\N	\N	t	t	\N	f339af4e-1d3d-4a67-b63e-091caa2ecf82	f
441	2019-08-25 18:04:10.239+00	2021-04-18 04:12:45.43609+00	status_3	Status	\N	t	4	f	183	\N	4	f	f	\N	f	f	\N	\N	\N	t	t	\N	07468fc8-dadc-41a6-a84b-e18103228e14	f
417	2019-08-22 00:42:00.155+00	2021-04-18 04:12:45.438031+00	disponibilidade	Disponibilidade	\N	t	4	f	172	\N	4	f	f	\N	f	f	\N	\N	\N	t	t	\N	b3b9f341-1bc5-4424-ad2b-fe2bf9de1d23	f
7	2019-07-17 13:33:14.277025+00	2021-04-18 04:12:45.439862+00	filial	Filial	\N	t	5	f	4	\N	4	f	f	\N	f	f	\N	\N	\N	t	t	\N	7024ef57-ee17-4602-9770-e92490e52a19	f
390	2019-08-21 01:27:57.357+00	2021-04-18 04:12:45.441694+00	valordosinistro	Valor do Sinistro	\N	t	5	f	159	\N	1	f	f	\N	f	f	\N	\N	\N	t	t	\N	0ed3ab62-26b2-4e6d-8f32-d2eafa9d1c62	f
430	2019-08-22 02:28:21.772+00	2021-04-18 04:12:45.443527+00	localdaocorrencia	Local da ocorrência	\N	t	5	f	177	\N	4	f	f	\N	f	f	\N	\N	\N	t	t	\N	fb8bc2d2-546d-4c2f-9a8e-b2681e304670	f
481	2019-08-27 01:31:18.634+00	2021-04-18 04:12:45.445323+00	status_3	Status	\N	t	5	f	204	\N	4	f	f	\N	f	f	\N	\N	\N	t	t	\N	9265391b-d3b6-419f-a653-f56be036160d	f
385	2019-08-20 01:47:35.368+00	2021-04-18 04:12:45.447181+00	tarifamediaultimaconta	Tárifa Média Última Conta		f	5	f	157	\N	1	f	f	\N	f	f	\N	\N	\N	t	t	\N	566cbd27-7987-4ea5-966a-e23bdd96f89c	f
391	2019-08-21 01:27:57.372+00	2021-04-18 04:12:45.448952+00	status_3	Status	\N	f	6	f	159	\N	4	f	f	\N	f	f	\N	\N	\N	t	t	\N	7ea7ce64-4b14-4952-8681-32e0856d07cf	f
8	2019-07-17 13:33:14.317498+00	2021-04-18 04:12:45.450959+00	status	Status	\N	f	6	f	4	\N	4	f	f	\N	f	f	\N	\N	\N	t	t	\N	f871cd50-f5a2-4a34-b281-bef25edca07a	f
\.


--
-- Data for Name: theme_field_options; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.theme_field_options (id, created_at, updated_at, option, "order", field_id, uuid) FROM stdin;
1	2019-07-17 13:33:14.086871+00	2021-02-26 04:43:32.458983+00	Mario Fulano	0	3	d1865df9-8257-4926-8f42-4bd453895f06
2	2019-07-17 13:33:14.087355+00	2021-02-26 04:43:32.470531+00	Luana Siclana	0	3	c52e73e8-626d-4a88-ba8c-a9e7d9a37b81
3	2019-07-17 13:33:14.087795+00	2021-02-26 04:43:32.472316+00	Robinson Machado	0	3	8f1c5025-5efe-430b-b836-b1ea689288e6
4	2019-07-17 13:33:14.13871+00	2021-02-26 04:43:32.473723+00	Residencial	0	4	dc66b909-7b72-44a1-8cd0-c4e30a3806c8
5	2019-07-17 13:33:14.139196+00	2021-02-26 04:43:32.475201+00	Marítimo	0	4	05ece662-0d1e-40dc-8943-39afbc5c9157
6	2019-07-17 13:33:14.139631+00	2021-02-26 04:43:32.476615+00	Automóvel	0	4	f6918faa-04a6-47d8-a5f3-423c75100a6a
7	2019-07-17 13:33:14.140076+00	2021-02-26 04:43:32.478001+00	Saúde	0	4	6c24ca87-234d-4937-8e08-760ed46465ec
8	2019-07-17 13:33:14.140494+00	2021-02-26 04:43:32.479406+00	Frota	0	4	90e6792a-8341-4c31-8e32-0c784e945f58
9	2019-07-17 13:33:14.140915+00	2021-02-26 04:43:32.480995+00	Engenharia	0	4	89defeda-dd67-4392-b123-d65e684e8020
10	2019-07-17 13:33:14.141351+00	2021-02-26 04:43:32.482428+00	Vida	0	4	17edc2f4-7bfc-43f7-b6c2-e20e9c8bfe72
11	2019-07-17 13:33:14.285409+00	2021-02-26 04:43:32.48385+00	São Paulo	0	7	cfdb2c65-b09c-4483-9ba8-6cbbc07aa3bf
12	2019-07-17 13:33:14.285967+00	2021-02-26 04:43:32.485214+00	Rio de Janeiro	0	7	5e1535b2-f5c2-443d-911c-91c574ac6c2c
18	2019-07-17 13:33:14.436081+00	2021-02-26 04:43:32.486579+00	Perda de Prazo	1	9	cfd4bfe8-4685-4f0f-9d7d-7247559dc4ec
19	2019-07-17 13:33:14.436463+00	2021-02-26 04:43:32.487941+00	Valor muito alto	1	9	4c7214ee-03d5-43d0-b998-b137f5fdc13a
511	2019-08-22 00:41:59.809+00	2021-02-26 04:43:32.489302+00	Aluguel	1	408	a27056f0-b6d6-49fd-9143-fc8b02ad0408
512	2019-08-22 00:41:59.81+00	2021-02-26 04:43:32.49074+00	Compra	1	408	fef4a012-f818-46f7-ac77-569df88e793e
513	2019-08-22 00:41:59.831+00	2021-02-26 04:43:32.492176+00	1 mês	1	409	555e2bc1-b4ce-4812-9edf-be4d38e3e8bc
514	2019-08-22 00:41:59.831+00	2021-02-26 04:43:32.493609+00	3 meses	1	409	0d539be8-d89c-4d31-8f99-0d8220912ee7
515	2019-08-22 00:41:59.832+00	2021-02-26 04:43:32.494964+00	6 meses	1	409	e776d80e-8997-4ccf-ae31-d8daf3ed2aed
516	2019-08-22 00:41:59.832+00	2021-02-26 04:43:32.496313+00	12 meses	1	409	32ab82a5-ec29-49f9-9c33-b57288f28380
523	2019-08-22 00:58:54.949+00	2021-02-26 04:43:32.497674+00	Média	0	422	28d79c57-2114-4392-adf0-eb33b9a0eebe
524	2019-08-22 00:58:54.95+00	2021-02-26 04:43:32.499005+00	Baixa	0	422	9f083136-e5c7-4cfb-b7be-f887f2d69c51
525	2019-08-22 00:58:54.95+00	2021-02-26 04:43:32.533888+00	Alta	0	422	f7479d2e-1927-404f-a8db-8975f8645448
530	2019-08-22 02:28:21.678+00	2021-02-26 04:43:32.535621+00	Elétrica	0	426	2b622e18-8e6c-4bea-a7e0-2956ea63dcdc
531	2019-08-22 02:28:21.679+00	2021-02-26 04:43:32.537076+00	Ar-Condicionado	0	426	954fa566-aa95-45af-b146-e403f31ced14
532	2019-08-22 02:28:21.679+00	2021-02-26 04:43:32.538454+00	Hidráulica	0	426	b3e270dc-006b-4cc5-979b-e45d6e50a561
533	2019-08-22 02:28:21.679+00	2021-02-26 04:43:32.539931+00	Marcenaria	0	426	742a4f9d-f8a5-4287-8898-00dbc7cea77b
534	2019-08-22 02:28:21.68+00	2021-02-26 04:43:32.541389+00	Telefonia	0	426	6091c295-1532-4082-a028-202897105a5d
615	2019-08-27 00:44:26.25+00	2021-02-26 04:43:32.542806+00	Energia	2	471	14999db6-3bae-4baa-ada5-eb8d529a6ca8
535	2019-08-22 02:28:21.68+00	2021-02-26 04:43:32.544216+00	Pintura	0	426	bae74075-65c5-44c3-8552-9d29b5da0b97
536	2019-08-22 02:28:21.701+00	2021-02-26 04:43:32.54565+00	Alta	0	427	5a375070-1595-4ca9-a715-81070c930641
537	2019-08-22 02:28:21.701+00	2021-02-26 04:43:32.54712+00	Média	0	427	4296633f-af23-43c2-b4e9-3ee40cdf2bd4
538	2019-08-22 02:28:21.702+00	2021-02-26 04:43:32.548491+00	Baixa	0	427	8fcafbde-3f32-4fb9-81e3-5c872531df42
543	2019-08-22 02:28:21.778+00	2021-02-26 04:43:32.549825+00	Quarto	0	430	0de20b5c-cc6f-4125-8d42-50d913741513
544	2019-08-22 02:28:21.778+00	2021-02-26 04:43:32.551166+00	Recepção	0	430	c38e8eba-6c20-41bc-b943-7d8ed8f44bea
545	2019-08-22 02:28:21.779+00	2021-02-26 04:43:32.552515+00	Piscina	0	430	b75a702f-27eb-47bf-8ff5-f08f765db5da
546	2019-08-22 02:28:21.779+00	2021-02-26 04:43:32.553939+00	Garagem	0	430	4811ca69-6cd0-4dba-b5db-58822b85110c
547	2019-08-22 02:28:21.779+00	2021-02-26 04:43:32.555319+00	Fachada	0	430	8e0f4eab-48ec-4829-9ceb-4cdb83e7d972
548	2019-08-22 02:28:21.997+00	2021-02-26 04:43:32.556671+00	Elétrica	0	436	5dd7a70d-b647-46c0-88bc-2ef46502b6f8
549	2019-08-22 02:28:21.998+00	2021-02-26 04:43:32.558105+00	Ar-condicionado	0	436	8f63d04b-6b40-45d7-9a55-41aea6d27220
477	2019-08-20 00:12:31.411+00	2021-02-26 04:43:32.559417+00	Valor alto	1	355	90484001-e865-40f4-8b21-bdfc2c1bf6f0
478	2019-08-20 00:12:31.412+00	2021-02-26 04:43:32.560754+00	Perda de Prazo	1	355	82255646-cebc-423e-8cf1-b9ab8b01d301
479	2019-08-20 00:12:31.412+00	2021-02-26 04:43:32.562133+00	Cliente desistiu de comprar o produto	1	355	3d1757dd-fc07-48ee-80e7-e8951b23192d
480	2019-08-20 00:12:31.412+00	2021-02-26 04:43:32.5635+00	Não foi mais possível contatar o cliente	1	355	e7e1d756-2b96-42f9-9024-481e1832b7c2
487	2019-08-20 01:47:35.192+00	2021-02-26 04:43:32.564889+00	Concorrente com preço menor	2	372	872378ba-84af-4107-8c29-b6a3f37bba13
488	2019-08-20 01:47:35.192+00	2021-02-26 04:43:32.566244+00	Cliente desistiu da instalação	2	372	1e20fcb9-47f5-494b-82f9-09138f6dcfca
489	2019-08-20 01:47:35.192+00	2021-02-26 04:43:32.567679+00	Local inadequado para instalação	2	372	0f49e401-434d-4b45-946c-a799c0fce8dd
490	2019-08-20 01:47:35.316+00	2021-02-26 04:43:32.56902+00	Empresa	1	380	395a80eb-2ed1-4f6e-b17a-6005fb914ce7
491	2019-08-20 01:47:35.316+00	2021-02-26 04:43:32.570421+00	Residência	1	380	25fd5222-0f8a-40c2-9257-8059ef2f4614
492	2019-08-20 01:47:35.33+00	2021-02-26 04:43:32.571814+00	Monofásica	1	381	5eec1cfb-860f-4c9f-814d-cd8919467571
493	2019-08-20 01:47:35.33+00	2021-02-26 04:43:32.573198+00	Bifásica	1	381	cefae8ce-0dc7-48bc-8f2b-97a72d205fbf
494	2019-08-20 01:47:35.331+00	2021-02-26 04:43:32.57462+00	Trifásica	1	381	c224789c-ac38-4688-994c-dc6b9bd9b68e
495	2019-08-20 01:47:35.342+00	2021-02-26 04:43:32.575934+00	On Grid	1	382	47894e25-f649-490d-8ae7-e909a84861a7
496	2019-08-20 01:47:35.342+00	2021-02-26 04:43:32.577258+00	Off Grid	1	382	e1a9a4e9-0209-47b1-b1bb-6c94a4f0b199
497	2019-08-20 01:47:35.342+00	2021-02-26 04:43:32.5787+00	Híbrido	1	382	21a069d1-420a-4d60-83db-2504274564f1
507	2019-08-22 00:41:59.551+00	2021-02-26 04:43:32.580084+00	Cliente optou por imóvel mais barato	2	400	f68f8c0b-930e-45e4-a9ee-0a2d4c7eaa00
508	2019-08-22 00:41:59.551+00	2021-02-26 04:43:32.581402+00	Localização ruim	2	400	6befa81a-8380-49b3-aaff-31d955d74acd
509	2019-08-22 00:41:59.552+00	2021-02-26 04:43:32.582828+00	Imóvel com problemas	2	400	07585981-ca77-43f6-8937-3a1807da8d38
510	2019-08-22 00:41:59.552+00	2021-02-26 04:43:32.584178+00	Cliente desistiu do negócio	2	400	e0fbdd8a-bb95-4012-9ef0-e13b12fd57cc
613	2019-08-27 00:44:26.249+00	2021-02-26 04:43:32.585628+00	Visita Comercial	0	471	774246f5-140a-470a-a85b-080ae557a9ab
614	2019-08-27 00:44:26.249+00	2021-02-26 04:43:32.586961+00	Telefone	1	471	4c45b60d-3c77-43f5-8c0c-2e115274a329
616	2019-08-27 00:44:26.25+00	2021-02-26 04:43:32.588328+00	Equipamentos	3	471	718894f1-159a-4b2d-97a6-ff72a465c707
617	2019-08-27 00:44:26.25+00	2021-02-26 04:43:32.589708+00	Software	4	471	0a1b66e8-e37b-41e7-b6ec-88f71bbce2e6
618	2019-08-27 00:44:26.25+00	2021-02-26 04:43:32.591076+00	Salários	5	471	44520864-34f2-4ec2-a68c-c7dd07553277
619	2019-08-27 00:44:26.251+00	2021-02-26 04:43:32.592443+00	Contador	6	471	2a607014-53fc-43c2-af0e-444a0d2c6819
620	2019-08-27 00:44:26.251+00	2021-02-26 04:43:32.593807+00	Advogado	7	471	33b3ab2c-e4c4-4599-a749-d6c727c51cb3
609	2019-08-25 19:55:22.255+00	2021-02-26 04:43:32.595169+00	Backlog	0	466	90b3ccbd-4c87-40ec-81d6-c87ff8e8e0d9
610	2019-08-25 19:55:22.255+00	2021-02-26 04:43:32.596536+00	Fazendo	1	466	8396f93e-b2d7-45e0-93ee-8031e7211496
611	2019-08-25 19:55:22.255+00	2021-02-26 04:43:32.597942+00	Pendente	2	466	c535f638-6c9d-4d7a-85f9-fc463bd8103d
612	2019-08-25 19:55:22.255+00	2021-02-26 04:43:32.599269+00	Concluído	3	466	77e03fb1-c876-4617-855a-d565bee39234
498	2019-08-21 01:27:57.377+00	2021-02-26 04:43:32.600642+00	Aberto	0	391	513b7d63-8f7b-4f98-b16f-494c79841cad
499	2019-08-21 01:27:57.377+00	2021-02-26 04:43:32.602006+00	Análise	1	391	8d728d53-15dc-46f7-bbe2-8dbd2ad67d69
500	2019-08-21 01:27:57.378+00	2021-02-26 04:43:32.603464+00	Indenizado	2	391	2097436f-d56b-41de-b397-557bc93eda8c
501	2019-08-21 01:27:57.378+00	2021-02-26 04:43:32.605898+00	Recusado	3	391	025fcf8d-9d1f-40f3-89bc-39b7cd897cad
526	2019-08-22 00:58:54.984+00	2021-02-26 04:43:32.607316+00	Backlog	0	424	dfcf5405-55ed-4b67-9867-e0d79114a0db
527	2019-08-22 00:58:54.984+00	2021-02-26 04:43:32.608704+00	Fazendo	1	424	c738ed6a-cde4-42fd-8880-4adf5529d25c
528	2019-08-22 00:58:54.985+00	2021-02-26 04:43:32.610153+00	Pausado	2	424	aee58396-f9d0-4220-a007-12a38f3eb8c9
529	2019-08-22 00:58:54.985+00	2021-02-26 04:43:32.611807+00	Feito	3	424	4df7a844-eb0e-4fa6-859d-0864b99dcf3f
442	2019-08-19 02:28:28.631+00	2021-02-26 04:43:32.613164+00	Saúde	0	336	834810d1-6276-4bd1-a60e-e1b5fb0895e3
443	2019-08-19 02:28:28.631+00	2021-02-26 04:43:32.614581+00	Garantia	0	336	cc2e03b3-61f5-432a-b146-7daccdb43205
444	2019-08-19 02:28:28.632+00	2021-02-26 04:43:32.615864+00	Transportes	0	336	9a4214ea-04c5-48ac-b084-a9df065c5f8f
445	2019-08-19 02:28:28.632+00	2021-02-26 04:43:32.617309+00	Engenharia	0	336	12cc16a6-7fa8-47e9-9906-56e2ea90e95e
446	2019-08-19 02:28:28.632+00	2021-02-26 04:43:32.618716+00	Fiança Locatícia	0	336	0c885af2-c4d8-4176-963a-22e003e1d760
452	2019-08-19 02:28:28.706+00	2021-02-26 04:43:32.620118+00	Allianz	1	341	1aa85e0b-1500-4fcc-add4-b37c74ff941c
453	2019-08-19 02:28:28.706+00	2021-02-26 04:43:32.621525+00	Amil	1	341	fa0c05d9-580d-49da-b564-68279bab2e8c
454	2019-08-19 02:28:28.707+00	2021-02-26 04:43:32.622877+00	Tokio Marine	1	341	db95e5ea-b88f-421c-be35-71d806268574
455	2019-08-19 02:28:28.707+00	2021-02-26 04:43:32.624353+00	Sul América	1	341	aaec3202-fb4f-4823-845f-26b1b35892ed
456	2019-08-19 02:28:28.707+00	2021-02-26 04:43:32.625689+00	Sompo	1	341	1cae50f4-ce3d-4052-bbd2-b8eb4b1429c8
457	2019-08-19 02:28:28.708+00	2021-02-26 04:43:32.627069+00	Berkley	1	341	a3d4a4a6-88ff-4934-b66e-7abc11170eeb
458	2019-08-19 02:28:28.708+00	2021-02-26 04:43:32.628453+00	Junto	1	341	55b54f38-985d-4373-8ebd-19ae700fece9
459	2019-08-19 02:28:28.727+00	2021-02-26 04:43:32.629812+00	Cliente desistiu do seguro	2	342	11b6ecbc-fe69-4d23-88c3-f1b588db111f
460	2019-08-19 02:28:28.728+00	2021-02-26 04:43:32.631207+00	Conseguiu prêmio menor em outra corretora	2	342	c14205e4-a0bf-4e52-b26f-211830a64172
461	2019-08-19 02:28:28.728+00	2021-02-26 04:43:32.632615+00	Perda de prazo pela seguradora	2	342	2f6197cc-b815-4394-9ec9-9d89ceace10f
462	2019-08-19 02:28:28.76+00	2021-02-26 04:43:32.633979+00	Allianz	3	344	ff87f5bf-133d-49d0-a4fc-9e89ea752e2a
463	2019-08-19 02:28:28.761+00	2021-02-26 04:43:32.635404+00	Amil	3	344	24da117d-416a-4674-8967-5abd9dbfc65d
464	2019-08-19 02:28:28.761+00	2021-02-26 04:43:32.636732+00	Sul América	3	344	4405368a-7a6c-4e84-8699-df0ffca58362
465	2019-08-19 02:28:28.761+00	2021-02-26 04:43:32.638108+00	Tokio Marine	3	344	da9391aa-baaf-479a-9938-6013a162476c
466	2019-08-19 02:28:28.762+00	2021-02-26 04:43:32.639494+00	Sompo	3	344	7548dec2-ce29-4087-96c6-9fc3a8b1ac58
467	2019-08-19 02:28:28.762+00	2021-02-26 04:43:32.640918+00	Berkley	3	344	c58b7ac8-828d-4d26-958b-3af3a7bc698a
468	2019-08-19 02:28:28.762+00	2021-02-26 04:43:32.642319+00	Junto	3	344	98d89040-e432-496d-9be9-20835f8f0175
469	2019-08-19 02:28:28.762+00	2021-02-26 04:43:32.643717+00	Argo	3	344	8fa67f40-eaf4-4295-be35-f397e1d58af9
597	2019-08-25 19:18:33.587+00	2021-02-26 04:43:32.645104+00	Informado	0	458	ac53ad7a-7429-45c8-96a7-0da74763e032
598	2019-08-25 19:18:33.587+00	2021-02-26 04:43:32.646498+00	Documentação	1	458	13f3ae1f-fb0c-45aa-a801-ef24340f4af2
599	2019-08-25 19:18:33.588+00	2021-02-26 04:43:32.647962+00	Entrevista	2	458	090e95df-3572-4a25-b3d6-5d580b9dd628
600	2019-08-25 19:18:33.588+00	2021-02-26 04:43:32.649298+00	Concluído	3	458	f7b74b4f-bc07-41c7-9858-74fe79e03e3f
588	2019-08-25 19:18:33.532+00	2021-02-26 04:43:32.650711+00	Estagiário	0	455	e557d44e-3e7f-472a-8e19-9efb8dd6c746
589	2019-08-25 19:18:33.533+00	2021-02-26 04:43:32.652029+00	Assistente	0	455	06fe3749-208d-4f30-9f46-f7bfac759d71
590	2019-08-25 19:18:33.533+00	2021-02-26 04:43:32.653454+00	Analista	0	455	7a52ccd8-a3cc-4fdc-a521-b30770ea1dee
591	2019-08-25 19:18:33.533+00	2021-02-26 04:43:32.655689+00	Coodernador	0	455	bb501278-dcf0-47b5-83a7-6f6238b0b250
593	2019-08-25 19:18:33.534+00	2021-02-26 04:43:32.657067+00	Diretor	0	455	55f8ad33-e4ff-49a8-acc1-ef062dcbdd90
594	2019-08-25 19:18:33.558+00	2021-02-26 04:43:32.658379+00	Demissão	1	456	87856c00-95c0-4ac7-8fa7-ddbc11b3a522
595	2019-08-25 19:18:33.558+00	2021-02-26 04:43:32.659666+00	Transferência	1	456	306edefc-f66d-41c2-8fde-d7b2e7dd1be7
596	2019-08-25 19:18:33.558+00	2021-02-26 04:43:32.661086+00	Aposentadoria	1	456	7a61e80f-9b8b-4c11-91fd-f9ad11f81cbd
601	2019-08-25 19:55:22.203+00	2021-02-26 04:43:32.662444+00	Melhoria	0	463	53949b4f-d5aa-401a-8c81-0be1946acfe9
602	2019-08-25 19:55:22.203+00	2021-02-26 04:43:32.663763+00	UX/ UI	0	463	24320321-7eea-4df5-820c-712ebde57e3b
603	2019-08-25 19:55:22.204+00	2021-02-26 04:43:32.6651+00	Bug	0	463	142209fe-df9b-4030-9ede-97fb1289a5f9
604	2019-08-25 19:55:22.204+00	2021-02-26 04:43:32.666535+00	Manutenção	0	463	6c7c28fa-11c5-4f38-af75-fd90dff2715d
605	2019-08-25 19:55:22.204+00	2021-02-26 04:43:32.667927+00	Funcionalidade Nova	0	463	8acde400-9067-4c37-9c7d-4e00f4974976
606	2019-08-25 19:55:22.22+00	2021-02-26 04:43:32.669332+00	Alta	0	464	d338b782-f0cc-40c2-b6ea-0563a5421d57
13	2019-07-17 13:33:14.325372+00	2021-02-26 04:43:32.670727+00	Prospecção	0	8	e0571b58-06d6-491c-8b8a-d26f8bbb406d
16	2019-07-17 13:33:14.326926+00	2021-02-26 04:43:32.672065+00	Fechado	2	8	58319d66-5b9e-4499-9a46-f1920d5d65a3
17	2019-07-17 13:33:14.327348+00	2021-02-26 04:43:32.673449+00	Perdido	3	8	a967d80d-4ded-4704-982b-d1820cc2a0c8
14	2019-07-17 13:33:14.325886+00	2021-02-26 04:43:32.674751+00	Análise	4	8	51f1e0d8-c641-4e1e-9b23-c0706f3d42ff
15	2019-07-17 13:33:14.326487+00	2021-02-26 04:43:32.676163+00	Negociação	5	8	1f0b64ba-bc31-46ad-afdf-a1dfc383d91e
633	2019-08-27 01:31:18.641+00	2021-02-26 04:43:32.677538+00	Lançamento	0	481	707f9928-9019-4130-b3c0-eca43ae227c2
634	2019-08-27 01:31:18.641+00	2021-02-26 04:43:32.678931+00	Cobrado	1	481	fde018c0-2ca9-418b-b865-55a5e64d2e77
635	2019-08-27 01:31:18.642+00	2021-02-26 04:43:32.680239+00	Pendente	2	481	eeb5909c-436f-4e18-a739-172f9d4e62b9
636	2019-08-27 01:31:18.642+00	2021-02-26 04:43:32.681597+00	Pago	3	481	b5a84850-b334-4a4e-b775-67a2d0443e15
550	2019-08-22 02:28:21.998+00	2021-02-26 04:43:32.682923+00	Marcenaria	0	436	3777fd6d-e807-42ee-93e5-342d40c48e41
551	2019-08-22 02:28:22+00	2021-02-26 04:43:32.684202+00	Hidráulica	0	436	0b3016fe-6cd7-4f7e-b11d-c0114165ef8f
552	2019-08-22 02:28:22+00	2021-02-26 04:43:32.685524+00	Telefonia	0	436	a392998c-b99a-4e09-91a7-d744127548d2
553	2019-08-22 02:28:22.001+00	2021-02-26 04:43:32.686798+00	Pintura	0	436	b017527a-4880-440a-8858-b0861fc80372
554	2019-08-25 18:04:10.173+00	2021-02-26 04:43:32.688084+00	Comercial	0	438	5723a422-0262-44cf-90af-8742ff824aba
555	2019-08-25 18:04:10.174+00	2021-02-26 04:43:32.689412+00	Administrativo	0	438	979a002e-975c-4299-966d-71f86f769814
556	2019-08-25 18:04:10.174+00	2021-02-26 04:43:32.690742+00	Recursos Humanos	0	438	17914c65-8497-4f58-b4e5-107a63e37da5
557	2019-08-25 18:04:10.174+00	2021-02-26 04:43:32.69207+00	Financeiro	0	438	d2857805-67a8-4fcc-b68c-bdb0bad7049c
558	2019-08-25 18:04:10.174+00	2021-02-26 04:43:32.693355+00	Tecnologia da Informação	0	438	7525936a-6f21-4829-ae55-23b337450554
559	2019-08-25 18:04:10.208+00	2021-02-26 04:43:32.694708+00	Estagiário	0	439	db287b05-12ed-453b-8668-23222b3295f3
560	2019-08-25 18:04:10.208+00	2021-02-26 04:43:32.696046+00	Assistente	0	439	2b3a2a82-596f-4d7e-bf4d-1f7f6edac386
561	2019-08-25 18:04:10.208+00	2021-02-26 04:43:32.6975+00	Analista	0	439	3e1d7ac7-86b7-4cd5-99c7-5b27cc778a47
562	2019-08-25 18:04:10.208+00	2021-02-26 04:43:32.698855+00	Gerente	0	439	5aed677f-ff50-4a1e-b382-4d76ecea6312
563	2019-08-25 18:04:10.209+00	2021-02-26 04:43:32.700188+00	Diretor	0	439	5be0429e-ae45-4ca1-921b-cafbe2f5afd5
564	2019-08-25 18:04:10.209+00	2021-02-26 04:43:32.701526+00	Presidente	0	439	06dbab38-0333-486f-83ad-1c80790b5611
570	2019-08-25 18:04:10.447+00	2021-02-26 04:43:32.702908+00	Financeiro	1	449	7246f743-b2d3-4162-a4cc-8b18d1aa2077
571	2019-08-25 18:04:10.447+00	2021-02-26 04:43:32.704197+00	Recursos Humanos	1	449	3a6e591c-f037-4d7a-b83e-ecd554b1cfcb
572	2019-08-25 18:04:10.447+00	2021-02-26 04:43:32.705567+00	Comercial	1	449	20237431-1fe7-47ad-8b50-d222bf28a4db
573	2019-08-25 18:04:10.447+00	2021-02-26 04:43:32.706883+00	Tecnologia da Informação	1	449	86c817c3-4b57-4f14-866d-2e9c2f755b39
574	2019-08-25 18:04:10.447+00	2021-02-26 04:43:32.708179+00	Administrativo	1	449	af86421a-03fc-486a-9cd3-c289a0e950c8
575	2019-08-25 18:04:10.466+00	2021-02-26 04:43:32.709525+00	Estagiario	1	450	984e3f98-82dd-4131-8889-72c35da1c46a
576	2019-08-25 18:04:10.466+00	2021-02-26 04:43:32.710799+00	Assistente	1	450	265189a8-9a45-4364-9e29-8c478e197fce
577	2019-08-25 18:04:10.466+00	2021-02-26 04:43:32.712139+00	Analista	1	450	b930bd2f-d337-4d58-b29b-81e2c658672c
578	2019-08-25 18:04:10.467+00	2021-02-26 04:43:32.713524+00	Gerente	1	450	a68e7496-2506-4deb-a2d7-4d065b8aac74
579	2019-08-25 18:04:10.467+00	2021-02-26 04:43:32.714925+00	Diretor	1	450	ca21b415-d4f3-4dd3-8b15-4c18c6a73d07
580	2019-08-25 18:04:10.467+00	2021-02-26 04:43:32.716279+00	Presidente	1	450	62fbbf2e-39ba-4f51-bfea-2177af878d2e
581	2019-08-25 19:18:33.513+00	2021-02-26 04:43:32.717659+00	Tecnologia da Informação	0	454	aa5a0f30-ee74-489b-bbe2-92d3ba2404d4
582	2019-08-25 19:18:33.513+00	2021-02-26 04:43:32.718931+00	Recursos Humanos	0	454	a28537a2-5440-4254-aa87-883ddc353c7a
583	2019-08-25 19:18:33.513+00	2021-02-26 04:43:32.720329+00	Financeiro	0	454	ba11b5d3-dde1-4221-8c2e-1a2f6d549c56
584	2019-08-25 19:18:33.514+00	2021-02-26 04:43:32.721703+00	Comercial	0	454	fa194daf-7f52-486b-bde0-8eff63fd47b4
585	2019-08-25 19:18:33.514+00	2021-02-26 04:43:32.723059+00	Marketing	0	454	7c71fee2-fd92-4c38-9299-6da66d0329af
586	2019-08-25 19:18:33.514+00	2021-02-26 04:43:32.724437+00	Jurídico	0	454	af1bc7d6-9e2b-40b5-9af1-b3514cc7f156
587	2019-08-25 19:18:33.514+00	2021-02-26 04:43:32.725777+00	Administrativo	0	454	e1192491-9081-42a4-a71e-85ccb514fd29
565	2019-08-25 18:04:10.243+00	2021-02-26 04:43:32.727185+00	Triagem	0	441	3511388c-a7e9-4b13-8cb0-0c87019a2f5e
566	2019-08-25 18:04:10.243+00	2021-02-26 04:43:32.728548+00	Dinâmica	1	441	182cee8e-49b0-4f11-97b1-bf121598609f
569	2019-08-25 18:04:10.244+00	2021-02-26 04:43:32.729853+00	Entrevista	2	441	555f64b8-6927-415d-a413-cd727fa169d3
567	2019-08-25 18:04:10.244+00	2021-02-26 04:43:32.731439+00	Aprovado	3	441	51cc9759-c469-4489-ac6a-1d113cf7d800
568	2019-08-25 18:04:10.244+00	2021-02-26 04:43:32.732817+00	Arquivado	4	441	29279e2c-7b78-4afc-97a0-c08556a41831
592	2019-08-25 19:18:33.533+00	2021-02-26 04:43:32.734173+00	Gerente	0	455	fe6c54e1-66ef-4a65-8c10-5b58545c06e8
607	2019-08-25 19:55:22.221+00	2021-02-26 04:43:32.73559+00	Média	0	464	c48c731e-01e3-4739-b4b5-834ff3e9d3a0
608	2019-08-25 19:55:22.221+00	2021-02-26 04:43:32.736979+00	Baixa	0	464	15bcb456-2fd2-45b0-86b7-3450afd99b8a
621	2019-08-27 01:31:18.546+00	2021-02-26 04:43:32.738447+00	Produto 01	0	477	9af64f17-c231-47a5-9304-38c9cfbac992
622	2019-08-27 01:31:18.549+00	2021-02-26 04:43:32.739838+00	Produto 02	0	477	ce2ae87c-16ca-49b1-a5ef-fa0204db5b62
623	2019-08-27 01:31:18.549+00	2021-02-26 04:43:32.741223+00	Produto 03	0	477	b3f1f355-0db9-4d9e-8e67-4e0f1265cdc1
624	2019-08-27 01:31:18.549+00	2021-02-26 04:43:32.742649+00	Produto 04	0	477	8d55295a-1db6-43df-ba2f-0ab7d6243dce
625	2019-08-27 01:31:18.55+00	2021-02-26 04:43:32.74399+00	Produto 05	0	477	d9dc4f00-8c80-4bca-a664-11150a5e7e39
626	2019-08-27 01:31:18.55+00	2021-02-26 04:43:32.745339+00	Produto 06	0	477	48c8ff15-54b5-4b2d-b51b-4f5cb07a917c
627	2019-08-27 01:31:18.551+00	2021-02-26 04:43:32.746723+00	Produto 07	0	477	412a17b0-cd0a-44ca-8643-fad1f1d13d12
628	2019-08-27 01:31:18.551+00	2021-02-26 04:43:32.748011+00	Produto 08	0	477	5173063f-ba61-4686-893f-292ff8331561
629	2019-08-27 01:31:18.616+00	2021-02-26 04:43:32.749315+00	Boleto	0	480	77a37114-55b9-447c-af45-ada59d9abb47
630	2019-08-27 01:31:18.617+00	2021-02-26 04:43:32.750684+00	Transferência Bancária	0	480	1dbff836-6cb2-4cbf-9367-6cd93a3e9b37
631	2019-08-27 01:31:18.617+00	2021-02-26 04:43:32.752049+00	Cartão de Crédito	0	480	202a042b-0819-493c-b967-cb9a9e1d553f
632	2019-08-27 01:31:18.618+00	2021-02-26 04:43:32.753398+00	Dinheiro	0	480	a92a2fde-c20c-4ab0-8e0c-234b95fb1259
637	2019-08-27 02:28:02.112+00	2021-02-26 04:43:32.754828+00	Facebook	0	489	5c2fad06-1df9-4e84-8935-d311a4272a02
638	2019-08-27 02:28:02.113+00	2021-02-26 04:43:32.758583+00	Instagram	0	489	09b8fe96-7434-453a-bcd6-1aa991153d52
639	2019-08-27 02:28:02.113+00	2021-02-26 04:43:32.759905+00	Linkedin	0	489	2397d79d-9a9a-4cfc-8b14-26789af9dcfe
640	2019-08-27 02:28:02.113+00	2021-02-26 04:43:32.761208+00	Blog	0	489	9d9f9a73-b636-4a2a-80cb-1a7931d40b5e
647	2019-08-27 02:28:02.291+00	2021-02-26 04:43:32.762626+00	Patrocinado	0	492	ad89a846-9ab7-484c-bdc9-54d9b693677d
648	2019-08-27 02:28:02.292+00	2021-02-26 04:43:32.763916+00	Orgânico	0	492	319cbf8e-7b27-474a-8f19-bd6332ee5f6f
641	2019-08-27 02:28:02.214+00	2021-02-26 04:43:32.765218+00	Criação	0	491	d508ebcf-46cc-4cdc-bc49-68fd55a1af5a
642	2019-08-27 02:28:02.215+00	2021-02-26 04:43:32.766645+00	Planejamento	1	491	c9ea1e45-69f1-44e0-843d-31d2aa78e36e
643	2019-08-27 02:28:02.215+00	2021-02-26 04:43:32.767978+00	Redação	2	491	e5705b5e-be70-4adc-9684-6baaaf16979c
644	2019-08-27 02:28:02.217+00	2021-02-26 04:43:32.769328+00	Aprovação	3	491	a564f1d1-53db-4fad-abd3-793b6e3f5b59
645	2019-08-27 02:28:02.217+00	2021-02-26 04:43:32.770722+00	Publicado	4	491	29fa8bea-dfaf-4f02-89e8-9ce3cc79bf34
646	2019-08-27 02:28:02.218+00	2021-02-26 04:43:32.772038+00	Cancelado	5	491	93557e8a-b572-4bf3-89e4-ee67fb19ffc0
481	2019-08-20 01:47:35.091+00	2021-02-26 04:43:32.773343+00	Prospecção	0	366	453185f3-16f7-4c1d-b8fa-a5c2dd227a85
482	2019-08-20 01:47:35.092+00	2021-02-26 04:43:32.77467+00	Reunião	1	366	92d1b571-faa0-475f-84a4-c7a9ee6cca82
483	2019-08-20 01:47:35.092+00	2021-02-26 04:43:32.775987+00	Negociação	2	366	836f3663-8cde-4d0c-a8f0-8a5fd8a5091a
484	2019-08-20 01:47:35.092+00	2021-02-26 04:43:32.777269+00	Instalação	3	366	8ce7bfab-0679-427c-991a-4791d858de5f
485	2019-08-20 01:47:35.092+00	2021-02-26 04:43:32.77861+00	Fechado	4	366	f2461e01-faae-4931-84da-a4ecfba99834
486	2019-08-20 01:47:35.093+00	2021-02-26 04:43:32.779872+00	Perdido	5	366	79b9b03c-bdf9-49f3-ac32-f47716ef4126
447	2019-08-19 02:28:28.666+00	2021-02-26 04:43:32.781199+00	Prospecção	0	339	8362bed4-f575-48a0-9cce-4d811e437085
448	2019-08-19 02:28:28.666+00	2021-02-26 04:43:32.782493+00	1ª Cotação	1	339	a7580c7c-c0c3-434b-921e-6c177ec10f37
449	2019-08-19 02:28:28.667+00	2021-02-26 04:43:32.783751+00	Negociação	2	339	4393ac04-4cb8-4bec-b6e7-3e31e16e4329
450	2019-08-19 02:28:28.667+00	2021-02-26 04:43:32.785079+00	Fechado	3	339	43bb2baa-7710-44e8-9416-e9b462fd8cce
451	2019-08-19 02:28:28.667+00	2021-02-26 04:43:32.786465+00	Perdido	4	339	b5ac3679-30f3-48c2-95f8-2e5ea48db40e
474	2019-08-20 00:12:31.375+00	2021-02-26 04:43:32.787731+00	Contatado	0	354	c6e3fd99-7956-4b5a-b323-0b61a180eebd
475	2019-08-20 00:12:31.375+00	2021-02-26 04:43:32.789054+00	Fechado	1	354	94032b52-8be7-436d-b329-b526ba3cfcb9
476	2019-08-20 00:12:31.376+00	2021-02-26 04:43:32.790437+00	Perdido	2	354	4191983c-5783-41e4-a5dc-aef7457f547e
472	2019-08-20 00:12:31.375+00	2021-02-26 04:43:32.791692+00	Proposta	3	354	64a9bd9c-241b-4065-acfe-9173f9fe369d
473	2019-08-20 00:12:31.375+00	2021-02-26 04:43:32.793063+00	Negociação	4	354	62cc4385-376f-4054-87a7-8090f002f814
470	2019-08-20 00:12:31.374+00	2021-02-26 04:43:32.794402+00	Prospecção	5	354	6b2b1b3a-0579-4cc5-916b-4b87b271240a
471	2019-08-20 00:12:31.374+00	2021-02-26 04:43:32.795712+00	Reunião	6	354	b5dfd29f-3341-4227-bc83-bf1925905d22
539	2019-08-22 02:28:21.744+00	2021-02-26 04:43:32.796996+00	Identificado	0	429	4b4b3f9c-eb9b-4bd5-9375-d6f2f175f2b7
540	2019-08-22 02:28:21.744+00	2021-02-26 04:43:32.798322+00	Orçamento	1	429	a8410042-6f4d-4ee6-b92a-fa1afbb1b8a8
541	2019-08-22 02:28:21.745+00	2021-02-26 04:43:32.799638+00	Atendimento	2	429	ec84da74-8a0d-4875-9caf-6a88378c3eb0
542	2019-08-22 02:28:21.745+00	2021-02-26 04:43:32.801611+00	Finalizado	3	429	cedbada2-63a6-4918-9553-d0f83e5b64bf
502	2019-08-22 00:41:59.459+00	2021-02-26 04:43:32.802992+00	Prospecção	0	398	6c29cff5-43f6-4de2-a4c5-3c353ab09563
503	2019-08-22 00:41:59.459+00	2021-02-26 04:43:32.804368+00	Visita	1	398	c69a682c-ba84-46ac-abd0-81322146ea43
504	2019-08-22 00:41:59.46+00	2021-02-26 04:43:32.805708+00	Proposta	2	398	db04cb10-2db0-41df-b81a-c4fc30f514df
505	2019-08-22 00:41:59.46+00	2021-02-26 04:43:32.807071+00	Fechado	3	398	5c6a4c00-11b0-4f51-b740-28f5f7446ed9
506	2019-08-22 00:41:59.461+00	2021-02-26 04:43:32.808404+00	Perdido	4	398	7099e370-8b00-40c8-b404-2b6eb71d0286
517	2019-08-22 00:41:59.856+00	2021-02-26 04:43:32.809792+00	Apartamento	0	410	093b53a3-1100-421e-b4f4-9f98b1783aef
518	2019-08-22 00:41:59.857+00	2021-02-26 04:43:32.811157+00	Casa	1	410	d509c8bc-6b3e-4db3-90a4-0d73c4028763
519	2019-08-22 00:42:00.161+00	2021-02-26 04:43:32.812551+00	Alugar	0	417	ea1d1b81-c2ed-4fe1-9c45-45555d542519
520	2019-08-22 00:42:00.161+00	2021-02-26 04:43:32.813889+00	Vender	1	417	c3993352-f955-458e-9edf-fc0a4b1cca0f
521	2019-08-22 00:42:00.162+00	2021-02-26 04:43:32.815175+00	Alugado	2	417	a0df88fd-4a57-465a-9561-ea49c82c8acf
522	2019-08-22 00:42:00.162+00	2021-02-26 04:43:32.816618+00	Vendido	3	417	f48c42aa-2f65-4d6c-ba81-ed277ebbd029
\.


--
-- Data for Name: theme_form; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.theme_form (id, created_at, updated_at, form_name, label_name, "order", conditional_value, conditional_on_field_id, conditional_type_id, depends_on_id, theme_id, type_id, form_id, uuid, conditional_excludes_data_if_not_set, show_label_name) FROM stdin;
150	2019-08-20 01:47:34.986+00	2021-04-18 04:12:45.457546+00	informacoesgerais_1	Informações Gerais	0	\N	\N	\N	149	17	1	\N	1471e455-bfc9-416f-9b73-04ab1a7212e1	t	t
148	2019-08-20 00:12:31.488+00	2021-04-18 04:12:45.459557+00	informacoesdocliente	Informações do Cliente	0	\N	\N	\N	147	16	1	\N	c9da85bf-1fa5-451a-bd0e-77b441472bfc	t	t
208	2019-08-27 01:31:18.792+00	2021-04-18 04:12:45.461283+00	cadastro	Cadastro	0	\N	\N	\N	207	26	1	\N	7f6deb97-9dae-4010-87b2-16f37030eaa6	t	t
209	2019-08-27 02:28:01.967+00	2021-04-18 04:12:45.46298+00	postagens	Postagens	0	\N	\N	\N	\N	27	1	756	4e2de68a-df98-481d-b630-5085dfb325dd	t	t
210	2019-08-27 02:28:02.026+00	2021-04-18 04:12:45.464677+00	informacaodopost	Informação do Post	0	\N	\N	\N	209	27	1	\N	10e690b7-5d16-4f0d-9dff-bb9e0516e39e	t	t
143	2019-08-20 00:12:31.337+00	2021-04-18 04:12:45.466414+00	informacoesgerais_1	Informações Gerais	0	\N	\N	\N	142	16	1	\N	19694ee9-37a2-486a-a4a5-e74e4f3f104d	t	t
135	2019-08-19 02:28:28.611+00	2021-04-18 04:12:45.468313+00	informacoesgerais_1	Informações Gerais	0	\N	\N	\N	134	15	1	\N	085f8496-9501-45bf-ae19-6fb3c61711b0	t	t
191	2019-08-25 19:18:33.486+00	2021-04-18 04:12:45.470077+00	informacoesdocolaborador	Informações do Colaborador	0	\N	\N	\N	190	23	1	\N	73fc3b5d-7c75-418d-80cd-c417e11770cd	t	t
141	2019-08-19 02:28:28.833+00	2021-04-18 04:12:45.471823+00	informacoesdosegurado	Informações do Segurado	0	\N	\N	\N	140	15	1	\N	c585bbd8-982c-4c03-a276-a0333e50efe6	t	t
190	2019-08-25 19:18:33.478+00	2021-04-18 04:12:45.473585+00	processodedesligamento	Processo de Desligamento	0	\N	\N	\N	\N	23	1	697	48e10505-1ec4-4ef8-9849-6c0ba8a0ef42	t	t
1	2019-07-16 22:50:21.816+00	2021-04-18 04:12:45.475347+00	empty_form	Clique no card para editar	0	\N	\N	\N	\N	1	1	\N	0212dab3-b931-48af-af05-26ccdde4bdff	t	t
2	2019-07-16 22:50:26.443+00	2021-04-18 04:12:45.477045+00	empty_topic	Clique no card ou no lápis	0	\N	\N	\N	1	1	1	\N	125549ed-a9b2-40de-9a4d-e394964c7061	t	t
163	2019-08-22 00:41:59.366+00	2021-04-18 04:12:45.478781+00	informacoesdevenda_1	Informações de Venda	0	\N	\N	\N	162	19	1	\N	22e64f97-50c9-46c2-b055-c31405becf64	t	t
196	2019-08-25 19:55:22.179+00	2021-04-18 04:12:45.480593+00	informacoesgerais_1	Informações Gerais	0	\N	\N	\N	195	24	1	\N	6e0be5b9-b815-4037-aea1-3e9ac88dab6f	t	t
187	2019-08-25 18:04:10.379+00	2021-04-18 04:12:45.482344+00	informacaodocandidato	Informação do Candidato	0	\N	\N	\N	186	22	1	\N	4376e183-5efa-4342-a1d7-7fce5067fd59	t	t
183	2019-08-25 18:04:10.14+00	2021-04-18 04:12:45.484106+00	processo	Processo	0	\N	\N	\N	182	22	1	\N	709cf249-298a-4588-9f38-7d7d878b14e2	t	t
181	2019-08-22 02:28:21.925+00	2021-04-18 04:12:45.485758+00	informacoesdofornecedor	Informações do fornecedor	0	\N	\N	\N	180	21	1	\N	1e2f615f-3918-4d6e-8c99-d1d5c42ce7c8	t	t
168	2019-08-22 00:41:59.683+00	2021-04-18 04:12:45.487447+00	informacoesdocliente	Informações do Cliente	0	\N	\N	\N	167	19	1	\N	daba9ccd-0bda-43eb-afe7-334efefe9ecb	t	t
4	2019-07-17 13:33:14.030116+00	2021-04-18 04:12:45.48913+00	nomedocliente	Informações	0	\N	\N	\N	3	2	1	\N	ce90402c-ea67-411d-aa78-52a71152db9e	t	t
177	2019-08-22 02:28:21.645+00	2021-04-18 04:12:45.490821+00	informacoesdoservico	Informações do Serviço	0	\N	\N	\N	176	21	1	\N	87b68ebd-ef2e-4e69-9c97-c82775e77927	t	t
158	2019-08-21 01:27:57.308+00	2021-04-18 04:12:45.492503+00	sinistros	Sinistros	0	\N	\N	\N	\N	18	1	630	dd4edac3-d5a0-4550-a470-447cb8581096	t	t
172	2019-08-22 00:42:00.069+00	2021-04-18 04:12:45.494192+00	localizacaoedisponibilidade	Localização e Disponibilidade	0	\N	\N	\N	171	19	1	\N	808a4de5-bbde-44c7-920e-f74dfb4dead3	t	t
195	2019-08-25 19:55:22.171+00	2021-04-18 04:12:45.49593+00	controlededesenvolvimento	Controle de Desenvolvimento	0	\N	\N	\N	\N	24	1	702	279fcdcb-01bd-429a-ad3a-af5e99eaa3ad	t	t
174	2019-08-22 00:58:54.911+00	2021-04-18 04:12:45.497587+00	organizacaodetarefas	Tarefas	0	\N	\N	\N	\N	20	1	654	59e5eaf4-8999-4dac-a487-52c98f2277e5	t	t
175	2019-08-22 00:58:54.92+00	2021-04-18 04:12:45.499236+00	cadastrodetarefas	Cadastro de Tarefas	0	\N	\N	\N	174	20	1	\N	b83ba76a-7b29-4d49-ae92-5a2f5ddfdfcf	t	t
201	2019-08-27 00:44:26.236+00	2021-04-18 04:12:45.500913+00	lancamentodedespesas	Lançamento de Despesas	0	\N	\N	\N	200	25	1	\N	bca10240-60b6-443e-b64f-d533605069b6	t	t
160	2019-08-21 01:27:57.395+00	2021-04-18 04:12:45.531545+00	anexos	Anexos	1	\N	\N	\N	158	18	1	\N	4024411b-a0ee-4593-8657-d51bffa7fe04	t	t
200	2019-08-27 00:44:26.229+00	2021-04-18 04:12:45.502585+00	controledepagamentos	Controle de Pagamentos	0	\N	\N	\N	\N	25	1	747	0ffc0e57-d24d-4434-b6ce-f34e0624155e	t	t
156	2019-08-20 01:47:35.271+00	2021-04-18 04:12:45.504436+00	informacoesdocliente	Informações do Cliente	0	\N	\N	\N	155	17	1	\N	2a0c932a-7821-4226-82d5-03f7e2fde63a	t	t
204	2019-08-27 01:31:18.51+00	2021-04-18 04:12:45.506159+00	informacoesderecebiveis	Informações de Recebíveis	0	\N	\N	\N	203	26	1	\N	950ef1d0-838f-4ccc-818e-f3e74aef4949	t	t
159	2019-08-21 01:27:57.313+00	2021-04-18 04:12:45.507842+00	informacoesdosinistro	Informações do Sinistro	0	\N	\N	\N	158	18	1	\N	742b7367-81fc-49b5-ab0f-2f08de7a1fda	t	t
178	2019-08-22 02:28:21.797+00	2021-04-18 04:12:45.509555+00	numerodoquarto	Número do quarto	1	Quarto	430	1	176	21	1	\N	81e2c574-8871-4a2b-a75f-365c435dc192	t	t
5	2019-07-17 13:33:14.398991+00	2021-04-18 04:12:45.511338+00	detalhedeperda	Detalhe de Perda	1	Perdido	8	1	3	2	1	\N	92cb1c1a-f53e-4e36-9cd0-f9fe255a3fb8	t	t
9	2019-07-17 13:33:14.720127+00	2021-04-18 04:12:45.512996+00	cadastrodeclientes	Cadastro de Clientes	1	\N	\N	\N	8	2	1	\N	beb14c80-364a-4cda-8936-d760bee737a8	t	t
164	2019-08-22 00:41:59.498+00	2021-04-18 04:12:45.514936+00	detalhedavisita	Detalhe da Visita	1	Visita	398	1	162	19	1	\N	556f3b7e-c7d6-4fea-88eb-2dee07b4cf82	t	t
169	2019-08-22 00:41:59.772+00	2021-04-18 04:12:45.516746+00	capitaleinteresses	Capital e Interesses	1	\N	\N	\N	167	19	1	\N	7ad2e1e4-6062-42ae-b736-60e779d5e851	t	t
173	2019-08-22 00:42:00.188+00	2021-04-18 04:12:45.518495+00	proprietario	Proprietário	1	\N	\N	\N	171	19	1	\N	c6d4c549-07b4-49c2-9343-aa445df2d6a6	t	t
202	2019-08-27 00:44:26.322+00	2021-04-18 04:12:45.520233+00	comprovantes	Comprovantes	1	\N	\N	\N	200	25	1	\N	b2070824-a27d-44ac-8d3c-0090a0f58747	t	t
205	2019-08-27 01:31:18.672+00	2021-04-18 04:12:45.521919+00	datadepagamento	Data de Pagamento	1	Pago	481	1	203	26	1	\N	a289da25-464a-4102-b109-c8e6ba201074	t	t
136	2019-08-19 02:28:28.688+00	2021-04-18 04:12:45.523595+00	detalhedefechamento	Detalhe de Fechamento	1	Fechado	339	1	134	15	1	\N	51dd8b25-b3ba-4c17-b337-d5e2f63d29ca	t	t
144	2019-08-20 00:12:31.402+00	2021-04-18 04:12:45.525329+00	detalhedeperda_1	Detalhe de Perda	1	Perdido	354	1	142	16	1	\N	52849b15-4a69-475c-87ef-34f7f2a63377	t	t
151	2019-08-20 01:47:35.13+00	2021-04-18 04:12:45.527564+00	informacoestecnicas	Informações Técnicas	1	\N	\N	\N	149	17	1	\N	402a5c74-0eb2-4acd-86b1-7c0d0779cafa	t	t
157	2019-08-20 01:47:35.309+00	2021-04-18 04:12:45.529812+00	instalacao	Instalação	1	\N	\N	\N	155	17	1	\N	c3ba9ffc-c4c2-4786-ba10-7364a30b9ab2	t	t
211	2019-08-27 02:28:02.333+00	2021-04-18 04:12:45.533264+00	detalhedopatrocinio	Detalhe do Patrocínio	1	Patrocinado	492	1	209	27	1	\N	25982870-a9fc-4faa-b032-a08521938c6e	t	t
3	2019-07-17 13:33:13.980722+00	2021-04-18 04:12:45.534996+00	pipeline	Pipeline	1	\N	\N	\N	\N	2	1	\N	96aea385-6d4c-40d9-9081-d40b5b377630	t	t
184	2019-08-25 18:04:10.273+00	2021-04-18 04:12:45.536709+00	dataehorario	Data e Horário	1	Entrevista	441	1	182	22	1	\N	b220c6b6-699f-4c65-bbf5-e4600b05bd89	t	t
188	2019-08-25 18:04:10.436+00	2021-04-18 04:12:45.53842+00	niveldocandidato	Nível do Candidato	1	\N	\N	\N	186	22	1	\N	c410597e-1c70-4ea2-828d-a22001f991df	t	t
192	2019-08-25 19:18:33.547+00	2021-04-18 04:12:45.540137+00	informacoesdodesligamento	Informações do Desligamento	1	\N	\N	\N	190	23	1	\N	b6c710be-11ee-459b-aeec-a9226c069bb4	t	t
197	2019-08-25 19:55:22.28+00	2021-04-18 04:12:45.546553+00	detalhedependencia	Detalhe de Pendência	1	Pendente	466	1	195	24	1	\N	95438182-99ae-4cc0-bec6-8dc9746b28b9	t	t
161	2019-08-21 01:27:57.409+00	2021-04-18 04:12:45.548542+00	observacoes	Observações	2	\N	\N	\N	158	18	1	\N	471f272a-4c72-4dd0-8afb-d6ddfe7f76b9	t	t
185	2019-08-25 18:04:10.31+00	2021-04-18 04:12:45.550307+00	observacoes	Observações	2	\N	\N	\N	182	22	1	\N	3f64f245-99e6-4d20-b7c4-8384641a29a9	t	t
170	2019-08-22 00:41:59.899+00	2021-04-18 04:12:45.552098+00	documentacao	Documentação	2	\N	\N	\N	167	19	1	\N	fe4dc6f4-8f69-41ac-948f-1d8c870f5ce2	t	t
6	2019-07-17 13:33:14.489558+00	2021-04-18 04:12:45.553833+00	historicodademanda	Histórico da Demanda	2		\N	\N	3	2	2	\N	f4c94fa4-43bd-4c09-8793-30496163c8f0	t	t
179	2019-08-22 02:28:21.821+00	2021-04-18 04:12:45.555585+00	observacoes	Observações	2	\N	\N	\N	176	21	1	\N	9a5c5e63-97f4-46a0-b741-f15a89d23690	t	t
206	2019-08-27 01:31:18.699+00	2021-04-18 04:12:45.557292+00	anexos	Anexos	2	\N	\N	\N	203	26	1	\N	792a595c-c865-45a4-9f5a-cb823e4a0a4f	t	t
152	2019-08-20 01:47:35.182+00	2021-04-18 04:12:45.559035+00	detalhedeperda_1	Detalhe de Perda	2	Perdido	366	1	149	17	1	\N	4b026d6c-d9a4-4c3b-b743-2b4f021746dc	t	t
189	2019-08-25 18:04:10.492+00	2021-04-18 04:12:45.56301+00	anexosimportantes	Anexos importantes	2	\N	\N	\N	186	22	1	\N	fa221b48-6ebb-448e-a8a7-683cfcce3389	t	t
198	2019-08-25 19:55:22.302+00	2021-04-18 04:12:45.564777+00	evidencias	Evidências	2	\N	\N	\N	195	24	1	\N	1e5f4239-f835-451a-96df-df4ff4aa79cf	t	t
193	2019-08-25 19:18:33.613+00	2021-04-18 04:12:45.566502+00	datadaentrevistademissional	Data da Entrevista Demissional	2	Entrevista	458	1	190	23	1	\N	5a79bcfd-bc45-40f4-8e05-7f787f8d3492	t	t
165	2019-08-22 00:41:59.534+00	2021-04-18 04:12:45.568266+00	detalhedeperda_1	Detalhe de Perda	2	Perdido	398	1	162	19	1	\N	76a50567-6171-4d8c-9287-438f9f51f737	t	t
145	2019-08-20 00:12:31.431+00	2021-04-18 04:12:45.569999+00	anexos	Anexos	2	\N	\N	\N	142	16	1	\N	8ddb56d9-bb71-4dd3-86b5-7f9f867134f1	t	t
137	2019-08-19 02:28:28.719+00	2021-04-18 04:12:45.571747+00	detalhedeperda_1	Detalhe de Perda	2	Perdido	339	1	134	15	1	\N	0f8b7f5a-6522-4d37-8011-1497bb3b765f	t	t
212	2019-08-27 02:28:02.366+00	2021-04-18 04:12:45.573467+00	observacoes	Observações	2	\N	\N	\N	209	27	1	\N	8f5000e9-aa4f-4df1-a736-94c00b937f05	t	t
7	2019-07-17 13:33:14.56778+00	2021-04-18 04:12:45.575233+00	anexos	Anexos	3		\N	\N	3	2	1	\N	29a86c8f-8dc7-4fa9-bd3c-5d68f5b7c699	t	t
146	2019-08-20 00:12:31.443+00	2021-04-18 04:12:45.577034+00	historico_1	Histórico	3	\N	\N	\N	142	16	2	\N	8f9da2c7-7425-421f-8c96-ed0dbb4df88d	t	t
153	2019-08-20 01:47:35.211+00	2021-04-18 04:12:45.578735+00	anexos	Anexos	3	\N	\N	\N	149	17	1	\N	5508ca74-d18b-4163-be07-695ef0414fd7	t	t
194	2019-08-25 19:18:33.648+00	2021-04-18 04:12:45.580728+00	documentacaodedesligamento	Documentação de desligamento	3	\N	\N	\N	190	23	1	\N	56222ddf-5ae5-4823-a836-c7c62558cd19	t	t
8	2019-07-17 13:33:14.695323+00	2021-04-18 04:12:45.582496+00	clientes	Clientes	3	\N	\N	\N	\N	2	1	\N	6cd41f62-6384-480e-933b-7b1371c0d3f1	t	t
213	2019-08-27 02:28:02.392+00	2021-04-18 04:12:45.584249+00	documentos	Documentos	3	\N	\N	\N	209	27	1	\N	79300f0b-7469-4fac-bbde-99231e2bd2cd	t	t
199	2019-08-25 19:55:22.321+00	2021-04-18 04:12:45.585971+00	historico_1	Histórico	3	\N	\N	\N	195	24	2	\N	e3cb7897-84dc-4ec8-a202-d5face22921d	t	t
166	2019-08-22 00:41:59.586+00	2021-04-18 04:12:45.587687+00	observacoes	Observações	3	\N	\N	\N	162	19	1	\N	bf8b9f64-86c2-417d-8432-79e22c70747c	t	t
138	2019-08-19 02:28:28.753+00	2021-04-18 04:12:45.589625+00	orcamentos	Orçamentos	3	\N	\N	\N	134	15	2	\N	d9b65d1d-91be-4e62-a4f9-fb3ca6f74a91	t	t
139	2019-08-19 02:28:28.782+00	2021-04-18 04:12:45.592453+00	historico_1	Histórico	4	\N	\N	\N	134	15	2	\N	4997020a-973c-4af8-882d-f8e15ddedc0e	t	t
154	2019-08-20 01:47:35.228+00	2021-04-18 04:12:45.594319+00	observacao	Observação	4	\N	\N	\N	149	17	1	\N	3a9eb6fa-063d-4231-8806-aaafabe5da40	t	t
203	2019-08-27 01:31:18.499+00	2021-04-18 04:12:45.596073+00	lancamentosderecebiveis	Lançamentos de Recebíveis	10	\N	\N	\N	\N	26	1	752	2f424bc8-17a8-4f1a-8ab7-d4b5ceb50efe	t	t
182	2019-08-25 18:04:10.127+00	2021-04-18 04:12:45.597891+00	processoseletivo	Processo Seletivo	10	\N	\N	\N	\N	22	1	691	ffddd555-dc42-4ffa-bfcc-8843e5b4f038	t	t
142	2019-08-20 00:12:31.332+00	2021-04-18 04:12:45.599626+00	negocios	Negócios	11	\N	\N	\N	\N	16	1	598	8c70e427-677d-4afc-9255-7d9accd2eccb	t	t
162	2019-08-22 00:41:59.354+00	2021-04-18 04:12:45.601548+00	negocios	Negócios	11	\N	\N	\N	\N	19	1	640	d51d9672-8acd-4349-982f-c1305cf4b8e4	t	t
134	2019-08-19 02:28:28.606+00	2021-04-18 04:12:45.603212+00	pipelinedevendas	Pipeline de Vendas	11	\N	\N	\N	\N	15	1	582	0930b07a-5b52-4cf4-a02f-abf4219a55eb	t	t
149	2019-08-20 01:47:34.981+00	2021-04-18 04:12:45.605235+00	vendas	Vendas	11	\N	\N	\N	\N	17	1	606	48df0d27-42f8-4ef1-9d87-17d1c8cde9e0	t	t
176	2019-08-22 02:28:21.637+00	2021-04-18 04:12:45.606928+00	cadastrodemanutencao	Manutenção	11	\N	\N	\N	\N	21	1	656	c11b116c-89d9-40fe-aa46-697b0ac95486	t	t
186	2019-08-25 18:04:10.372+00	2021-04-18 04:12:45.608642+00	cadastrodocandidato	Cadastro do Candidato	11	\N	\N	\N	\N	22	1	687	2ba7be37-230a-45f0-8dc7-8651c021fdce	t	t
207	2019-08-27 01:31:18.784+00	2021-04-18 04:12:45.611068+00	cadastrodeclientes	Cadastro de Clientes	11	\N	\N	\N	\N	26	1	750	afa9950e-7a3c-4b47-8712-d7d251aba1b7	t	t
147	2019-08-20 00:12:31.483+00	2021-04-18 04:12:45.612765+00	clientes_1	Clientes	12	\N	\N	\N	\N	16	1	596	6b19c1af-58db-4e38-b5ff-a117f67e1bfe	t	t
155	2019-08-20 01:47:35.266+00	2021-04-18 04:12:45.614459+00	clientes_2	Clientes	12	\N	\N	\N	\N	17	1	603	77f8b1fc-ef56-4778-be35-3f3beb2da736	t	t
180	2019-08-22 02:28:21.916+00	2021-04-18 04:12:45.616253+00	fornecedores	Fornecedores	12	\N	\N	\N	\N	21	1	660	fedba717-dc0b-4f56-bbd0-4037a238bc3f	t	t
167	2019-08-22 00:41:59.674+00	2021-04-18 04:12:45.619027+00	clientes_1	Clientes	12	\N	\N	\N	\N	19	1	637	94674615-749c-4787-9307-116646c92143	t	t
140	2019-08-19 02:28:28.828+00	2021-04-18 04:12:45.620715+00	segurados_1	Segurados	12	\N	\N	\N	\N	15	1	580	2c71748c-91c9-4fd6-9ca3-81f30df11bb9	t	t
171	2019-08-22 00:42:00.058+00	2021-04-18 04:12:45.622384+00	imoveis	Imóveis	13	\N	\N	\N	\N	19	1	634	0b3d8318-ba96-4065-8500-677d66921dbd	t	t
\.


--
-- Data for Name: theme_formula_variable; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.theme_formula_variable (id, "order", field_id, variable_id) FROM stdin;
\.


--
-- Data for Name: theme_kanban_card; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.theme_kanban_card (id, created_at, updated_at, "default", theme_id) FROM stdin;
1	2019-07-17 13:33:13.994777+00	2019-07-17 13:33:13.995008+00	f	2
34	2019-08-19 02:28:28.802+00	2019-08-19 02:28:28.802+00	t	15
35	2019-08-20 00:12:31.462+00	2019-08-20 00:12:31.462+00	t	16
36	2019-08-20 01:47:35.245+00	2019-08-20 01:47:35.246+00	t	17
37	2019-08-21 01:27:57.428+00	2019-08-21 01:27:57.429+00	t	18
38	2019-08-22 00:41:59.626+00	2019-08-22 00:41:59.626+00	t	19
39	2019-08-22 00:41:59.941+00	2019-08-22 00:41:59.942+00	t	19
40	2019-08-22 00:42:00.256+00	2019-08-22 00:42:00.257+00	t	19
41	2019-08-22 00:58:55.049+00	2019-08-22 00:58:55.049+00	t	20
42	2019-08-22 02:28:21.877+00	2019-08-22 02:28:21.877+00	t	21
43	2019-08-25 18:04:10.337+00	2019-08-25 18:04:10.337+00	t	22
44	2019-08-25 19:18:33.673+00	2019-08-25 19:18:33.674+00	t	23
45	2019-08-25 19:55:22.358+00	2019-08-25 19:55:22.358+00	t	24
46	2019-08-27 00:44:26.346+00	2019-08-27 00:44:26.346+00	t	25
47	2019-08-27 01:31:18.732+00	2019-08-27 01:31:18.733+00	t	26
48	2019-08-27 02:28:02.432+00	2019-08-27 02:28:02.432+00	t	27
\.


--
-- Data for Name: theme_kanban_card_field; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.theme_kanban_card_field (id, created_at, updated_at, field_id, kanban_card_id, "order") FROM stdin;
141	2019-08-22 00:41:59.991+00	2019-08-22 00:41:59.991+00	407	39	0
142	2019-08-22 00:41:59.991+00	2019-08-22 00:41:59.994+00	411	39	0
143	2019-08-22 00:42:00.285+00	2019-08-22 00:42:00.286+00	413	40	0
144	2019-08-22 00:42:00.286+00	2019-08-22 00:42:00.286+00	414	40	0
145	2019-08-22 00:42:00.286+00	2019-08-22 00:42:00.286+00	415	40	0
146	2019-08-22 00:42:00.288+00	2019-08-22 00:42:00.289+00	418	40	0
147	2019-08-22 00:58:55.07+00	2019-08-22 00:58:55.07+00	421	41	0
148	2019-08-22 00:58:55.071+00	2019-08-22 00:58:55.071+00	422	41	0
149	2019-08-22 00:58:55.071+00	2019-08-22 00:58:55.071+00	423	41	0
150	2019-08-22 02:28:21.9+00	2019-08-22 02:28:21.9+00	426	42	0
151	2019-08-22 02:28:21.9+00	2019-08-22 02:28:21.9+00	430	42	0
152	2019-08-22 02:28:21.901+00	2019-08-22 02:28:21.901+00	427	42	0
153	2019-08-22 02:28:21.901+00	2019-08-22 02:28:21.901+00	428	42	0
154	2019-08-25 18:04:10.356+00	2019-08-25 18:04:10.356+00	437	43	0
155	2019-08-25 18:04:10.356+00	2019-08-25 18:04:10.356+00	438	43	0
156	2019-08-25 18:04:10.356+00	2019-08-25 18:04:10.357+00	439	43	0
157	2019-08-25 18:04:10.357+00	2019-08-25 18:04:10.357+00	440	43	0
158	2019-08-25 19:18:33.689+00	2019-08-25 19:18:33.689+00	455	44	0
159	2019-08-25 19:18:33.689+00	2019-08-25 19:18:33.689+00	456	44	0
160	2019-08-25 19:18:33.689+00	2019-08-25 19:18:33.689+00	453	44	0
161	2019-08-25 19:55:22.387+00	2019-08-25 19:55:22.387+00	462	45	0
162	2019-08-25 19:55:22.387+00	2019-08-25 19:55:22.387+00	463	45	0
163	2019-08-25 19:55:22.387+00	2019-08-25 19:55:22.388+00	464	45	0
164	2019-08-25 19:55:22.388+00	2019-08-25 19:55:22.388+00	465	45	0
165	2019-08-27 00:44:26.361+00	2019-08-27 00:44:26.361+00	472	46	0
166	2019-08-27 00:44:26.361+00	2019-08-27 00:44:26.361+00	473	46	0
167	2019-08-27 00:44:26.361+00	2019-08-27 00:44:26.362+00	474	46	0
168	2019-08-27 01:31:18.761+00	2019-08-27 01:31:18.761+00	476	47	0
169	2019-08-27 01:31:18.762+00	2019-08-27 01:31:18.762+00	477	47	0
170	2019-08-27 01:31:18.762+00	2019-08-27 01:31:18.762+00	479	47	0
171	2019-08-27 01:31:18.763+00	2019-08-27 01:31:18.764+00	478	47	0
172	2019-08-27 02:28:02.454+00	2019-08-27 02:28:02.454+00	488	48	0
173	2019-08-27 02:28:02.454+00	2019-08-27 02:28:02.454+00	490	48	0
174	2019-08-27 02:28:02.455+00	2019-08-27 02:28:02.455+00	492	48	0
124	2019-08-19 02:28:28.814+00	2019-08-19 02:28:28.814+00	335	34	0
125	2019-08-19 02:28:28.814+00	2019-08-19 02:28:28.814+00	336	34	0
126	2019-08-19 02:28:28.815+00	2019-08-19 02:28:28.815+00	337	34	0
127	2019-08-20 00:12:31.472+00	2019-08-20 00:12:31.472+00	351	35	0
128	2019-08-20 00:12:31.473+00	2019-08-20 00:12:31.473+00	352	35	0
129	2019-08-20 00:12:31.473+00	2019-08-20 00:12:31.473+00	353	35	0
130	2019-08-20 01:47:35.256+00	2019-08-20 01:47:35.256+00	363	36	0
131	2019-08-20 01:47:35.256+00	2019-08-20 01:47:35.256+00	364	36	0
132	2019-08-20 01:47:35.257+00	2019-08-20 01:47:35.257+00	365	36	0
133	2019-08-21 01:27:57.448+00	2019-08-21 01:27:57.449+00	391	37	0
134	2019-08-21 01:27:57.449+00	2019-08-21 01:27:57.449+00	386	37	0
135	2019-08-21 01:27:57.449+00	2019-08-21 01:27:57.449+00	387	37	0
136	2019-08-21 01:27:57.449+00	2019-08-21 01:27:57.449+00	390	37	0
137	2019-08-22 00:41:59.649+00	2019-08-22 00:41:59.649+00	397	38	0
138	2019-08-22 00:41:59.649+00	2019-08-22 00:41:59.649+00	395	38	0
139	2019-08-22 00:41:59.65+00	2019-08-22 00:41:59.65+00	396	38	0
140	2019-08-22 00:41:59.988+00	2019-08-22 00:41:59.991+00	403	39	0
\.


--
-- Data for Name: theme_kanban_default; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.theme_kanban_default (id, form_id, kanban_card_id, kanban_dimension_id, theme_id) FROM stdin;
1	209	48	491	27
2	200	46	471	25
3	195	45	466	24
4	190	44	458	23
5	158	37	391	18
6	174	41	424	20
7	203	47	481	26
8	182	43	441	22
9	149	36	366	17
10	134	34	339	15
11	142	35	354	16
12	176	42	429	21
13	162	38	398	19
14	167	39	410	19
15	171	40	417	19
\.


--
-- Data for Name: theme_kanban_dimension_order; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.theme_kanban_dimension_order (id, created_at, updated_at, options, "order", "default", dimension_id, theme_id) FROM stdin;
1	2019-07-17 13:33:14.35529+00	2019-07-17 13:33:14.355536+00	Prospecção	0	t	8	2
2	2019-07-17 13:33:14.361382+00	2019-07-17 13:33:14.361578+00	Análise	5	t	8	2
3	2019-07-17 13:33:14.3686+00	2019-07-17 13:33:14.368787+00	Perdido	4	t	8	2
4	2019-07-17 13:33:14.371633+00	2019-07-17 13:33:14.371867+00	Perdido	4	t	8	2
5	2019-07-17 13:33:14.374507+00	2019-07-17 13:33:14.374697+00	Perdido	4	t	8	2
6	2019-07-17 13:33:14.37754+00	2019-07-17 13:33:14.377752+00	Perdido	1	t	8	2
7	2019-07-17 13:33:14.380409+00	2019-07-17 13:33:14.380598+00	Fechado	2	t	8	2
138	2019-08-19 02:28:28.674+00	2019-08-19 02:28:28.674+00	1ª Cotação	1	t	339	15
139	2019-08-19 02:28:28.676+00	2019-08-19 02:28:28.677+00	Perdido	4	t	339	15
140	2019-08-19 02:28:28.678+00	2019-08-19 02:28:28.678+00	Negociação	2	t	339	15
141	2019-08-19 02:28:28.68+00	2019-08-19 02:28:28.68+00	Fechado	3	t	339	15
142	2019-08-19 02:28:28.681+00	2019-08-19 02:28:28.681+00	Prospecção	0	t	339	15
143	2019-08-20 00:12:31.385+00	2019-08-20 00:12:31.386+00	Cliente Potencial	0	t	354	16
144	2019-08-20 00:12:31.387+00	2019-08-20 00:12:31.387+00	Contatado	1	t	354	16
145	2019-08-20 00:12:31.389+00	2019-08-20 00:12:31.389+00	Reunião Marcada	2	t	354	16
146	2019-08-20 00:12:31.39+00	2019-08-20 00:12:31.391+00	Proposta Feita	3	t	354	16
147	2019-08-20 00:12:31.392+00	2019-08-20 00:12:31.392+00	Em negociação	4	t	354	16
148	2019-08-20 00:12:31.394+00	2019-08-20 00:12:31.394+00	Fechado	5	t	354	16
149	2019-08-20 00:12:31.395+00	2019-08-20 00:12:31.396+00	Perdido	6	t	354	16
181	2019-08-25 18:04:10.259+00	2019-08-25 18:04:10.259+00	Entrevista	2	t	441	22
182	2019-08-25 18:04:10.261+00	2019-08-25 18:04:10.261+00	Aprovado	3	t	441	22
183	2019-08-25 18:04:10.263+00	2019-08-25 18:04:10.263+00	Arquivado	4	t	441	22
184	2019-08-25 19:18:33.596+00	2019-08-25 19:18:33.596+00	Informado	0	t	458	23
185	2019-08-25 19:18:33.599+00	2019-08-25 19:18:33.599+00	Documentação	1	t	458	23
186	2019-08-25 19:18:33.601+00	2019-08-25 19:18:33.601+00	Entrevista	2	t	458	23
187	2019-08-25 19:18:33.603+00	2019-08-25 19:18:33.603+00	Concluído	3	t	458	23
189	2019-08-25 19:55:22.266+00	2019-08-25 19:55:22.266+00	Fazendo	1	t	466	24
190	2019-08-25 19:55:22.268+00	2019-08-25 19:55:22.268+00	Pendente	2	t	466	24
191	2019-08-25 19:55:22.271+00	2019-08-25 19:55:22.271+00	Concluído	3	t	466	24
192	2019-08-27 00:44:26.262+00	2019-08-27 00:44:26.263+00	Visita Comercial	0	t	471	25
193	2019-08-27 00:44:26.265+00	2019-08-27 00:44:26.265+00	Telefone	1	t	471	25
194	2019-08-27 00:44:26.267+00	2019-08-27 00:44:26.267+00	Energia	2	t	471	25
195	2019-08-27 00:44:26.269+00	2019-08-27 00:44:26.269+00	Equipamentos	3	t	471	25
196	2019-08-27 00:44:26.271+00	2019-08-27 00:44:26.272+00	Software	4	t	471	25
197	2019-08-27 00:44:26.274+00	2019-08-27 00:44:26.274+00	Salários	5	t	471	25
198	2019-08-27 00:44:26.276+00	2019-08-27 00:44:26.276+00	Contador	6	t	471	25
199	2019-08-27 00:44:26.278+00	2019-08-27 00:44:26.278+00	Advogado	7	t	471	25
200	2019-08-27 01:31:18.653+00	2019-08-27 01:31:18.653+00	Lançamento	0	t	481	26
201	2019-08-27 01:31:18.656+00	2019-08-27 01:31:18.656+00	Cobrado	1	t	481	26
202	2019-08-27 01:31:18.658+00	2019-08-27 01:31:18.658+00	Pendente	2	t	481	26
203	2019-08-27 01:31:18.66+00	2019-08-27 01:31:18.661+00	Pago	3	t	481	26
204	2019-08-27 02:28:02.233+00	2019-08-27 02:28:02.233+00	Criação	0	t	491	27
205	2019-08-27 02:28:02.237+00	2019-08-27 02:28:02.237+00	Planejamento	1	t	491	27
206	2019-08-27 02:28:02.243+00	2019-08-27 02:28:02.244+00	Redação	2	t	491	27
207	2019-08-27 02:28:02.248+00	2019-08-27 02:28:02.248+00	Aprovação	3	t	491	27
208	2019-08-27 02:28:02.252+00	2019-08-27 02:28:02.252+00	Publicado	4	t	491	27
209	2019-08-27 02:28:02.262+00	2019-08-27 02:28:02.263+00	Cancelado	5	t	491	27
150	2019-08-20 01:47:35.105+00	2019-08-20 01:47:35.105+00	Prospecção	0	t	366	17
151	2019-08-20 01:47:35.109+00	2019-08-20 01:47:35.11+00	Reunião	1	t	366	17
152	2019-08-20 01:47:35.111+00	2019-08-20 01:47:35.111+00	Negociação	2	t	366	17
153	2019-08-20 01:47:35.114+00	2019-08-20 01:47:35.114+00	Instalação	3	t	366	17
154	2019-08-20 01:47:35.118+00	2019-08-20 01:47:35.118+00	Fechado	4	t	366	17
155	2019-08-20 01:47:35.12+00	2019-08-20 01:47:35.12+00	Perdido	5	t	366	17
156	2019-08-21 01:27:57.385+00	2019-08-21 01:27:57.385+00	Aberto	0	t	391	18
157	2019-08-21 01:27:57.387+00	2019-08-21 01:27:57.387+00	Análise	1	t	391	18
158	2019-08-21 01:27:57.388+00	2019-08-21 01:27:57.389+00	Indenizado	2	t	391	18
159	2019-08-21 01:27:57.39+00	2019-08-21 01:27:57.39+00	Recusado	3	t	391	18
160	2019-08-22 00:41:59.474+00	2019-08-22 00:41:59.474+00	Perdido	4	t	398	19
161	2019-08-22 00:41:59.478+00	2019-08-22 00:41:59.478+00	Visita	1	t	398	19
162	2019-08-22 00:41:59.48+00	2019-08-22 00:41:59.48+00	Prospecção	0	t	398	19
163	2019-08-22 00:41:59.482+00	2019-08-22 00:41:59.483+00	Fechado	3	t	398	19
164	2019-08-22 00:41:59.485+00	2019-08-22 00:41:59.485+00	Proposta	2	t	398	19
165	2019-08-22 00:41:59.87+00	2019-08-22 00:41:59.87+00	Apartamento	0	t	410	19
166	2019-08-22 00:41:59.872+00	2019-08-22 00:41:59.873+00	Casa	1	t	410	19
167	2019-08-22 00:42:00.172+00	2019-08-22 00:42:00.172+00	Alugar	0	t	417	19
168	2019-08-22 00:42:00.174+00	2019-08-22 00:42:00.175+00	Vender	1	t	417	19
169	2019-08-22 00:42:00.177+00	2019-08-22 00:42:00.177+00	Alugado	2	t	417	19
170	2019-08-22 00:42:00.179+00	2019-08-22 00:42:00.179+00	Vendido	3	t	417	19
171	2019-08-22 00:58:54.994+00	2019-08-22 00:58:54.995+00	Backlog	0	t	424	20
172	2019-08-22 00:58:54.997+00	2019-08-22 00:58:54.997+00	Fazendo	1	t	424	20
173	2019-08-22 00:58:54.999+00	2019-08-22 00:58:54.999+00	Pausado	2	t	424	20
174	2019-08-22 00:58:55.005+00	2019-08-22 00:58:55.005+00	Feito	3	t	424	20
175	2019-08-22 02:28:21.754+00	2019-08-22 02:28:21.754+00	Finalizado	3	t	429	21
176	2019-08-22 02:28:21.757+00	2019-08-22 02:28:21.757+00	Atendimento	2	t	429	21
177	2019-08-22 02:28:21.759+00	2019-08-22 02:28:21.76+00	Orçamento	1	t	429	21
178	2019-08-22 02:28:21.762+00	2019-08-22 02:28:21.762+00	Identificado	0	t	429	21
179	2019-08-25 18:04:10.252+00	2019-08-25 18:04:10.253+00	Triagem	0	t	441	22
180	2019-08-25 18:04:10.257+00	2019-08-25 18:04:10.257+00	Dinâmica	1	t	441	22
188	2019-08-25 19:55:22.264+00	2019-08-25 19:55:22.264+00	Backlog	0	t	466	24
\.


--
-- Data for Name: theme_notification_configuration; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.theme_notification_configuration (id, created_at, updated_at, for_company, name, text, days_diff, field_id, form_id) FROM stdin;
1	2019-07-17 13:33:14.247146+00	2019-07-17 13:33:14.247413+00	t	Lembrete de previsão	A conta do/a {{nomedocliente}} esa prevista para hoje!	0	6	3
2	2019-07-17 13:33:14.253238+00	2019-07-17 13:33:14.253455+00	t	Lembrete de previsão	A conta do/a {{nomedocliente}} esta prevista para fechar hoje!	0	6	3
46	2019-08-19 02:28:28.748+00	2019-08-19 02:28:28.748+00	t	Conversão de Apólice	A conta do/a {{nome_1}} esta próxima do vencimento e pode ser convertida este ano!	-60	343	134
47	2019-08-20 01:47:35.066+00	2019-08-20 01:47:35.067+00	t	Previsão de Fechamento	A conta do/a {{cliente_2}} está prevista para fechar no dia {{previsaodefechamento_1}}	-10	364	149
48	2019-08-22 00:41:59.43+00	2019-08-22 00:41:59.431+00	t	Previsão de fechamento	Não se esqueça que a conta do/a {{cliente_2}} está prevista para fechar no dia {{previsaodefechamento_1}}!!	-7	396	162
49	2019-08-22 00:41:59.526+00	2019-08-22 00:41:59.526+00	t	Notificação de visita	Hoje é dia de visita com o/a {{cliente_2}} no imóvel {{imovel}}!	0	399	162
50	2019-08-25 18:04:10.291+00	2019-08-25 18:04:10.291+00	t	Lembrete de Entrevista	A entrevista com o/a {{candidato}} está marcado para hoje às {{horario}}!	0	442	182
51	2019-08-25 19:18:33.632+00	2019-08-25 19:18:33.632+00	t	Lembrete de Entrevista Demissional	A entrevista demissional do/a {{nomedocolaborador}} esta marcada para hoje às {{horario_1}}!	0	459	190
52	2019-08-25 19:55:22.244+00	2019-08-25 19:55:22.244+00	t	Lembrete de Conclusão	Você tem trabalho de prioridade {{prioridade_2}} para entregar até hoje!	0	465	195
53	2019-08-27 01:31:18.604+00	2019-08-27 01:31:18.605+00	t	Lembrete de Vencimentos	A fatura do/a {{cliente_2}} irá vencer no dia {{vencimentodafatura}}!	-3	479	203
54	2019-08-27 02:28:02.171+00	2019-08-27 02:28:02.172+00	t	Lembrete de Postagem	Não se esqueça que hoje é dia de postar o/a {{titulodopost}}!	0	490	209
\.


--
-- Data for Name: theme_notification_configuration_variable; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.theme_notification_configuration_variable (id, "order", field_id, notification_configuration_id) FROM stdin;
1	1	2	1
2	1	2	2
3	1	453	51
4	2	460	51
5	1	464	52
6	1	476	53
7	2	479	53
8	1	488	54
9	1	335	46
10	1	363	47
11	2	364	47
12	1	395	48
13	2	396	48
14	1	395	49
15	2	394	49
16	1	437	50
17	2	443	50
\.


--
-- Data for Name: theme_photos; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.theme_photos (id, image_name, url, theme_id) FROM stdin;
\.


--
-- Data for Name: theme_type; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.theme_type (id, name, label_name, "order") FROM stdin;
1	empty	Outro	1
2	sales	Vendas	1
3	development	T.I.	1
4	rh	Recursos Humanos	1
6	marketing	Marketing	1
7	operations	Operações	1
8	projects	Projetos	1
9	finance	Financeiro	1
\.


--
-- Data for Name: user_accessed_by; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.user_accessed_by (id, created_at, updated_at, field_id, user_id, user_option_id) FROM stdin;
\.


--
-- Data for Name: user_notification; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.user_notification (id, created_at, updated_at, notification_id, user_id, has_read, is_new) FROM stdin;
\.


--
-- Data for Name: users; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.users (id, password, last_login, is_superuser, username, first_name, last_name, email, is_staff, is_active, date_joined, phone, timezone, is_admin, temp_password, company_id, data_type_id, profile_id) FROM stdin;
18	pbkdf2_sha256$120000$LsI9UJ5mxt9F$1U+9PthPE937MkIAXD5Hbb0PtqfGyRnv8onp/nqMoBo=	\N	f	[18]nicolasmelo12@gmail.com	asdasdasd	Teste	nicolasmelo12@gmail.com	f	f	2019-05-07 17:57:32.143744+00	11111111	-3	f	\N	1	\N	3
12	pbkdf2_sha256$120000$BLU7k0dyVlYF$DenUAO2ujLjqxAPRqbG87WEFsvl+4FaG8IB/UQJJn08=	\N	f	justnava@hotmail.com	Naget	Melo	justnava@hotmail.com	f	t	2019-01-26 23:43:15.576961+00	11111111	-3	f	\N	3	\N	3
24	pbkdf2_sha256$150000$FceNIQGma28P$31E81Cl8hXfVp+vE4LJtoDtoR+bC84030UFIIWREpj4=	2019-11-05 16:48:35.416909+00	f	teste@teste123.com.br	Nicolas	Melo	teste@teste123.com.br	f	t	2019-11-05 16:48:17.065573+00	1123123123	-3	f	\N	8	\N	3
13	pbkdf2_sha256$120000$jfk4wQfTxwvz$xlPjptsdFfXvF3Go5WGcs9kYAKT3p/lVI8kYuptJzG0=	\N	f	lleal.melo@gmail.com	LUCAS	DE MELO	lleal.melo@gmail.com	f	t	2019-02-02 17:25:39.310883+00	11111111	-3	f	\N	3	\N	3
20	pbkdf2_sha256$150000$14glOygLdx26$e+hj9UNbbZ5cfCJ3mrx0va4nHwOxBDNKA7zWvE8DZcU=	2019-05-27 18:57:46.506701+00	f	nicolas.melo@usp.br	Reflow	Teste	nicolas.melo@usp.br	f	t	2019-05-07 19:18:33.2047+00	11111111	-3	f	\N	1	2	4
23	pbkdf2_sha256$150000$I0fvTQ7hi0Qx$+0bdjfkjvTWGXKwR2Aecpzabu9upl7zwLufAOGkNTKI=	\N	f	lleal.melo@outlook.com	asdasda	asdasdasd	lleal.melo@outlook.com	f	t	2019-07-29 19:00:39.579262+00	11111111	-3	f	\N	7	\N	3
9	pbkdf2_sha256$120000$Dogfa99vv3P1$hPT3z5DVQl4u9xKr7PZQ9XStCbaEL5JkCWcVcywG/DI=	2019-05-03 01:51:32.940119+00	t	[9]nicolasmelo12@gmail.com	Nicolas	Melo	nicolasmelo12@gmail.com	t	f	2018-07-18 06:50:19.733+00		-3	t	\N	1	\N	3
16	pbkdf2_sha256$120000$XYdlMFYFMJgX$0rXpIWvlQT1aJcTpKu2PqPbiX/NsfFlnGlbSZMGrAKQ=	\N	f	[16]nicolasmelo12@gmail.com	Nicolas	Melo	nicolasmelo12@gmail.com	f	f	2019-05-07 16:08:01.614617+00	11111111	-3	f	\N	1	\N	3
17	pbkdf2_sha256$120000$dcsYq81dTvFj$bCVQFNiG+hrofboavSNEpf6LMre+E1uriV4S19yAwSM=	\N	f	[17]nicolasmelo12@gmail.com	asdasdasd	Teste	nicolasmelo12@gmail.com	f	f	2019-05-07 16:23:13.391075+00	11111111	-3	f	\N	1	\N	3
22	pbkdf2_sha256$150000$iLkoiAYVAZeT$rnFa7WwOulx8gTN0FJ9JPurQzKULmluLyydUcb3xtK0=	2019-07-28 15:01:44.307286+00	f	reflow.crm@gmail.com	asdasdasdasd	asdasdasdasdasd	reflow.crm@gmail.com	f	t	2019-07-28 14:25:22.138575+00	11111111	-3	f	\N	6	\N	3
25		\N	f	barack.obama@gmail.com	Barack	Obama	barack.obama@gmail.com	f	t	2020-05-18 01:12:23.468094+00	\N	-3	f	pbkdf2_sha256$150000$UeaXCrNJN6Hx$WkVJb7Gp9+lcinWHjAc0l1AQwJFe8BeovisHo/4HiAQ=	1	\N	2
27		\N	f	nicolasmelo12@gmail.com	Nicolas	Melo	nicolasmelo12@gmail.com	f	t	2020-08-19 19:17:19.608669+00	\N	-3	f	eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpZCI6MjcsImV4cCI6MTU5Nzk1MTAzOSwidHlwZSI6ImFjY2VzcyJ9.tHUxE9tcC06DW6fnkvHLP8sC7vyeU95pHo-mS7ikdsg	1	\N	3
7	pbkdf2_sha256$120000$Hldnl21KrszQ$jEZT+4cFz7LnQ/Iuq3J4U428nKXFBULTLLA9krMNC30=	2019-01-03 06:15:43.131235+00	f	[7]nicolas.melo@99app.com	Nicolas Teste	Teste	nicolas.melo@99app.com	f	f	2019-01-03 06:14:50.851429+00	11111111	-3	f	\N	3	\N	2
6	pbkdf2_sha256$120000$v8EhCRTv8xum$7/j2RqzVzctp8R/xfMQO0zJbttmCiMM/Rc1WEdDVJn4=	\N	f	patricia.sbena@gmail.com	Patricia	Bena	patricia.sbena@gmail.com	f	t	2018-12-29 11:29:59.929555+00	11111111	-3	f	\N	3	\N	2
5	Luquinha123	2018-12-26 23:13:53+00	t	[5]luksinho1	Lucas	Leal	lleal_melo@hotmail.com	t	f	2018-12-26 23:13:36+00	11970852396	-3	t	\N	3	\N	2
11	pbkdf2_sha256$120000$6B49SSiHPEEt$w1rMdWE54UH31FGwcE++W0fXUaqOzlMMJIxh5zaZR/8=	2019-01-13 21:12:13.1123+00	f	[11]mbenevides@berkley.com.br	Marcelo	Benevides	mbenevides@berkley.com.br	f	f	2019-01-13 21:09:54.542836+00	11111111	-3	f	\N	3	\N	2
10	pbkdf2_sha256$120000$puMilRr2oXoD$wytSo5p9qnUOjznOMiG55WW6EKb9bzbP0VcsbIgG2yE=	\N	f	viviane.gennari@hotmail.com	Viviane	Gennari	viviane.gennari@hotmail.com	f	t	2019-01-05 18:35:45.532371+00	11111111	-3	f	\N	3	\N	2
8	pbkdf2_sha256$120000$RxHxxFpnsJoe$N/KX52vCgL2rgdp3DZZhYq1UFrHp4XqAMCN/JdVmmFc=	2019-02-21 14:12:23.556747+00	f	nicolas.melo@99app.com	Samuel Ribeiro	Leal	nicolas.melo@99app.com	f	t	2019-01-03 16:28:23.951029+00	11111111	-3	f	\N	3	\N	2
15	pbkdf2_sha256$120000$G6812SV2eIRG$FVjP0LANR3E4nuQEOHvYxVysMg/2ScVFiO/YRrO7v0I=	2019-04-21 19:31:23.646582+00	f	lleal_melo@hotmail.com	Lucas	Melo	lleal_melo@hotmail.com	f	t	2019-02-22 13:08:23.445408+00	11111111	-3	f	\N	3	\N	2
28	pbkdf2_sha256$216000$dXKkA5ZwjXaZ$WfkGqr01uVdyewbx2IwdtmaWJQLRm8BradISKXakJNM=	2020-10-04 01:52:41.537169+00	f	teste123@teste.com	teste	teste123	teste123@teste.com	f	t	2020-09-29 23:01:05.308641+00	11970852396	-3	f	\N	9	\N	3
1	pbkdf2_sha256$216000$YH66ExJGPLPO$KdZ/UNZW0qbdPub0o0ydXb7iAzQcWGcUSu1EacjqGdc=	2021-06-07 17:56:49.966382+00	t	reflow@reflow.com.br	reflow	admin	reflow@reflow.com.br	t	t	2019-03-20 21:23:25.369+00	\N	-3	t	eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpZCI6MSwiZXhwIjoxNTk4OTEzNTcxLCJ0eXBlIjoiYWNjZXNzIn0.6P0Kw-S2n3RMRGMLJsekwomjlghnDWw-X4bNM1OQ_98	1	2	3
\.


--
-- Data for Name: users_groups; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.users_groups (id, userextended_id, group_id) FROM stdin;
\.


--
-- Data for Name: users_user_permissions; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.users_user_permissions (id, userextended_id, permission_id) FROM stdin;
\.


--
-- Name: address_type_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.address_type_id_seq', 5570, true);


--
-- Name: aggregation_type_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.aggregation_type_id_seq', 6, true);


--
-- Name: app_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.app_id_seq', 3, true);


--
-- Name: attachments_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.attachments_id_seq', 72, true);


--
-- Name: auth_group_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.auth_group_id_seq', 1, false);


--
-- Name: auth_group_permissions_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.auth_group_permissions_id_seq', 1, false);


--
-- Name: auth_permission_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.auth_permission_id_seq', 1008, true);


--
-- Name: charge_frequency_type_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.charge_frequency_type_id_seq', 1, true);


--
-- Name: charge_type_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.charge_type_id_seq', 2, true);


--
-- Name: chart_type_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.chart_type_id_seq', 4, true);


--
-- Name: client_value_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.client_value_id_seq', 6212, true);


--
-- Name: companies_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.companies_id_seq', 9, true);


--
-- Name: company_billing_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.company_billing_id_seq', 6, true);


--
-- Name: company_charge_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.company_charge_id_seq', 8, true);


--
-- Name: company_coupon_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.company_coupon_id_seq', 1, false);


--
-- Name: company_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.company_id_seq', 1, false);


--
-- Name: company_invoice_mails_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.company_invoice_mails_id_seq', 25, true);


--
-- Name: company_type_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.company_type_id_seq', 9, true);


--
-- Name: company_type_id_seq1; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.company_type_id_seq1', 14, true);


--
-- Name: conditional_type_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.conditional_type_id_seq', 1, true);


--
-- Name: current_company_charge_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.current_company_charge_id_seq', 108, true);


--
-- Name: dashboard_chart_configuration_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.dashboard_chart_configuration_id_seq', 47, true);


--
-- Name: data_type_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.data_type_id_seq', 1, false);


--
-- Name: date_format_type_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.date_format_type_id_seq', 2, true);


--
-- Name: default_attachments_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.default_attachments_id_seq', 1, false);


--
-- Name: default_field_value_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.default_field_value_id_seq', 1, true);


--
-- Name: discount_by_individual_name_for_company_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.discount_by_individual_name_for_company_id_seq', 1, false);


--
-- Name: discount_by_individual_value_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.discount_by_individual_value_id_seq', 35, true);


--
-- Name: discount_coupon_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.discount_coupon_id_seq', 1, false);


--
-- Name: django_admin_log_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.django_admin_log_id_seq', 3, true);


--
-- Name: django_celery_results_taskresult_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.django_celery_results_taskresult_id_seq', 1, false);


--
-- Name: django_content_type_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.django_content_type_id_seq', 244, true);


--
-- Name: django_migrations_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.django_migrations_id_seq', 670, true);


--
-- Name: draft_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.draft_id_seq', 21, true);


--
-- Name: draft_type_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.draft_type_id_seq', 2, true);


--
-- Name: dynamic_forms_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.dynamic_forms_id_seq', 2109, true);


--
-- Name: extract_file_data_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.extract_file_data_id_seq', 57, true);


--
-- Name: field_date_format_type_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.field_date_format_type_id_seq', 1, false);


--
-- Name: field_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.field_id_seq', 764, true);


--
-- Name: field_number_format_type_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.field_number_format_type_id_seq', 3, true);


--
-- Name: field_options_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.field_options_id_seq', 2230, true);


--
-- Name: field_period_interval_type_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.field_period_interval_type_id_seq', 1, false);


--
-- Name: field_type_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.field_type_id_seq', 15, true);


--
-- Name: form_accessed_by_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.form_accessed_by_id_seq', 259, true);


--
-- Name: form_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.form_id_seq', 334, true);


--
-- Name: form_type_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.form_type_id_seq', 2, true);


--
-- Name: form_value_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.form_value_id_seq', 1, false);


--
-- Name: formula_attribute_type_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.formula_attribute_type_id_seq', 13, true);


--
-- Name: formula_context_attribute_type_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.formula_context_attribute_type_id_seq', 26, true);


--
-- Name: formula_context_for_company_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.formula_context_for_company_id_seq', 1, true);


--
-- Name: formula_context_type_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.formula_context_type_id_seq', 1, false);


--
-- Name: formula_parameters_type_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.formula_parameters_type_id_seq', 1, false);


--
-- Name: formula_variable_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.formula_variable_id_seq', 24, true);


--
-- Name: group_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.group_id_seq', 35, true);


--
-- Name: individual_charge_value_type_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.individual_charge_value_type_id_seq', 5, true);


--
-- Name: invoice_date_type_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.invoice_date_type_id_seq', 4, true);


--
-- Name: kanban_card_field_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.kanban_card_field_id_seq', 759, true);


--
-- Name: kanban_card_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.kanban_card_id_seq', 124, true);


--
-- Name: kanban_collapsed_option_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.kanban_collapsed_option_id_seq', 13, true);


--
-- Name: kanban_default_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.kanban_default_id_seq', 7, true);


--
-- Name: kanban_dimension_order_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.kanban_dimension_order_id_seq', 749, true);


--
-- Name: listing_selected_fields_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.listing_selected_fields_id_seq', 2327, true);


--
-- Name: notification_configuration_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.notification_configuration_id_seq', 33, true);


--
-- Name: notification_configuration_variable_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.notification_configuration_variable_id_seq', 33, true);


--
-- Name: notification_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.notification_id_seq', 330, true);


--
-- Name: option_accessed_by_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.option_accessed_by_id_seq', 9232, true);


--
-- Name: partner_default_and_discounts_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.partner_default_and_discounts_id_seq', 1, false);


--
-- Name: payment_method_type_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.payment_method_type_id_seq', 2, true);


--
-- Name: pdf_generated_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.pdf_generated_id_seq', 67, true);


--
-- Name: pdf_template_allowed_text_block_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.pdf_template_allowed_text_block_id_seq', 3, true);


--
-- Name: pdf_template_configuration_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.pdf_template_configuration_id_seq', 7, true);


--
-- Name: pdf_template_configuration_variables_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.pdf_template_configuration_variables_id_seq', 152, true);


--
-- Name: period_interval_type_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.period_interval_type_id_seq', 6, true);


--
-- Name: pre_notification_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.pre_notification_id_seq', 24756, true);


--
-- Name: profiles_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.profiles_id_seq', 4, true);


--
-- Name: public_access_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.public_access_id_seq', 1, true);


--
-- Name: public_field_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.public_field_id_seq', 37, true);


--
-- Name: public_form_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.public_form_id_seq', 10, true);


--
-- Name: push_notification_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.push_notification_id_seq', 8, true);


--
-- Name: push_notification_tag_type_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.push_notification_tag_type_id_seq', 1, true);


--
-- Name: raw_data_type_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.raw_data_type_id_seq', 1, false);


--
-- Name: read_notification_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.read_notification_id_seq', 321, true);


--
-- Name: text_alignment_type_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.text_alignment_type_id_seq', 3, true);


--
-- Name: text_block_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.text_block_id_seq', 336, true);


--
-- Name: text_block_type_can_contain_type_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.text_block_type_can_contain_type_id_seq', 2, true);


--
-- Name: text_block_type_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.text_block_type_id_seq', 4, true);


--
-- Name: text_content_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.text_content_id_seq', 1017, true);


--
-- Name: text_image_option_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.text_image_option_id_seq', 16, true);


--
-- Name: text_list_option_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.text_list_option_id_seq', 1, false);


--
-- Name: text_list_type_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.text_list_type_id_seq', 2, true);


--
-- Name: text_page_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.text_page_id_seq', 7, true);


--
-- Name: text_table_option_column_dimension_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.text_table_option_column_dimension_id_seq', 312, true);


--
-- Name: text_table_option_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.text_table_option_id_seq', 81, true);


--
-- Name: text_table_option_row_dimension_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.text_table_option_row_dimension_id_seq', 194, true);


--
-- Name: text_text_option_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.text_text_option_id_seq', 321, true);


--
-- Name: theme_dashboard_chart_configuration_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.theme_dashboard_chart_configuration_id_seq', 1, false);


--
-- Name: theme_field_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.theme_field_id_seq', 495, true);


--
-- Name: theme_field_options_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.theme_field_options_id_seq', 648, true);


--
-- Name: theme_form_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.theme_form_id_seq', 213, true);


--
-- Name: theme_formula_variable_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.theme_formula_variable_id_seq', 1, false);


--
-- Name: theme_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.theme_id_seq', 27, true);


--
-- Name: theme_kanban_card_field_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.theme_kanban_card_field_id_seq', 174, true);


--
-- Name: theme_kanban_card_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.theme_kanban_card_id_seq', 48, true);


--
-- Name: theme_kanban_default_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.theme_kanban_default_id_seq', 15, true);


--
-- Name: theme_kanban_dimension_order_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.theme_kanban_dimension_order_id_seq', 209, true);


--
-- Name: theme_notification_configuration_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.theme_notification_configuration_id_seq', 54, true);


--
-- Name: theme_notification_configuration_variable_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.theme_notification_configuration_variable_id_seq', 17, true);


--
-- Name: theme_photos_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.theme_photos_id_seq', 1, false);


--
-- Name: user_accessed_by_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.user_accessed_by_id_seq', 64, true);


--
-- Name: users_groups_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.users_groups_id_seq', 1, false);


--
-- Name: users_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.users_id_seq', 28, true);


--
-- Name: users_user_permissions_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.users_user_permissions_id_seq', 1, false);


--
-- Name: address_helper address_type_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.address_helper
    ADD CONSTRAINT address_type_pkey PRIMARY KEY (id);


--
-- Name: aggregation_type aggregation_type_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.aggregation_type
    ADD CONSTRAINT aggregation_type_pkey PRIMARY KEY (id);


--
-- Name: attachments attachments_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.attachments
    ADD CONSTRAINT attachments_pkey PRIMARY KEY (id);


--
-- Name: auth_group auth_group_name_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.auth_group
    ADD CONSTRAINT auth_group_name_key UNIQUE (name);


--
-- Name: auth_group_permissions auth_group_permissions_group_id_permission_id_0cd325b0_uniq; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.auth_group_permissions
    ADD CONSTRAINT auth_group_permissions_group_id_permission_id_0cd325b0_uniq UNIQUE (group_id, permission_id);


--
-- Name: auth_group_permissions auth_group_permissions_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.auth_group_permissions
    ADD CONSTRAINT auth_group_permissions_pkey PRIMARY KEY (id);


--
-- Name: auth_group auth_group_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.auth_group
    ADD CONSTRAINT auth_group_pkey PRIMARY KEY (id);


--
-- Name: auth_permission auth_permission_content_type_id_codename_01ab375a_uniq; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.auth_permission
    ADD CONSTRAINT auth_permission_content_type_id_codename_01ab375a_uniq UNIQUE (content_type_id, codename);


--
-- Name: auth_permission auth_permission_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.auth_permission
    ADD CONSTRAINT auth_permission_pkey PRIMARY KEY (id);


--
-- Name: charge_frequency_type charge_frequency_type_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.charge_frequency_type
    ADD CONSTRAINT charge_frequency_type_pkey PRIMARY KEY (id);


--
-- Name: charge_type charge_type_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.charge_type
    ADD CONSTRAINT charge_type_pkey PRIMARY KEY (id);


--
-- Name: chart_type chart_type_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.chart_type
    ADD CONSTRAINT chart_type_pkey PRIMARY KEY (id);


--
-- Name: company_billing company_billing_company_id_41cfc942_uniq; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.company_billing
    ADD CONSTRAINT company_billing_company_id_41cfc942_uniq UNIQUE (company_id);


--
-- Name: company_billing company_billing_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.company_billing
    ADD CONSTRAINT company_billing_pkey PRIMARY KEY (id);


--
-- Name: company_charge company_charge_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.company_charge
    ADD CONSTRAINT company_charge_pkey PRIMARY KEY (id);


--
-- Name: company_coupon company_coupon_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.company_coupon
    ADD CONSTRAINT company_coupon_pkey PRIMARY KEY (id);


--
-- Name: company_invoice_mails company_invoice_mails_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.company_invoice_mails
    ADD CONSTRAINT company_invoice_mails_pkey PRIMARY KEY (id);


--
-- Name: company company_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.company
    ADD CONSTRAINT company_pkey PRIMARY KEY (id);


--
-- Name: company_type company_type_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.company_type
    ADD CONSTRAINT company_type_pkey PRIMARY KEY (id);


--
-- Name: conditional_type conditional_type_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.conditional_type
    ADD CONSTRAINT conditional_type_pkey PRIMARY KEY (id);


--
-- Name: current_company_charge current_company_charge_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.current_company_charge
    ADD CONSTRAINT current_company_charge_pkey PRIMARY KEY (id);


--
-- Name: dashboard_chart_configuration dashboard_chart_configuration_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.dashboard_chart_configuration
    ADD CONSTRAINT dashboard_chart_configuration_pkey PRIMARY KEY (id);


--
-- Name: data_type data_type_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.data_type
    ADD CONSTRAINT data_type_pkey PRIMARY KEY (id);


--
-- Name: default_attachments default_attachments_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.default_attachments
    ADD CONSTRAINT default_attachments_pkey PRIMARY KEY (id);


--
-- Name: default_field_value default_field_value_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.default_field_value
    ADD CONSTRAINT default_field_value_pkey PRIMARY KEY (id);


--
-- Name: discount_by_individual_name_for_company discount_by_individual_name_for_company_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.discount_by_individual_name_for_company
    ADD CONSTRAINT discount_by_individual_name_for_company_pkey PRIMARY KEY (id);


--
-- Name: discount_by_individual_value_quantity discount_by_individual_value_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.discount_by_individual_value_quantity
    ADD CONSTRAINT discount_by_individual_value_pkey PRIMARY KEY (id);


--
-- Name: discount_coupon discount_coupon_name_1e6c0f03_uniq; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.discount_coupon
    ADD CONSTRAINT discount_coupon_name_1e6c0f03_uniq UNIQUE (name);


--
-- Name: discount_coupon discount_coupon_name_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.discount_coupon
    ADD CONSTRAINT discount_coupon_name_key UNIQUE (name);


--
-- Name: discount_coupon discount_coupon_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.discount_coupon
    ADD CONSTRAINT discount_coupon_pkey PRIMARY KEY (id);


--
-- Name: django_admin_log django_admin_log_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.django_admin_log
    ADD CONSTRAINT django_admin_log_pkey PRIMARY KEY (id);


--
-- Name: django_celery_results_taskresult django_celery_results_taskresult_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.django_celery_results_taskresult
    ADD CONSTRAINT django_celery_results_taskresult_pkey PRIMARY KEY (id);


--
-- Name: django_celery_results_taskresult django_celery_results_taskresult_task_id_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.django_celery_results_taskresult
    ADD CONSTRAINT django_celery_results_taskresult_task_id_key UNIQUE (task_id);


--
-- Name: django_content_type django_content_type_app_label_model_76bd3d3b_uniq; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.django_content_type
    ADD CONSTRAINT django_content_type_app_label_model_76bd3d3b_uniq UNIQUE (app_label, model);


--
-- Name: django_content_type django_content_type_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.django_content_type
    ADD CONSTRAINT django_content_type_pkey PRIMARY KEY (id);


--
-- Name: django_migrations django_migrations_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.django_migrations
    ADD CONSTRAINT django_migrations_pkey PRIMARY KEY (id);


--
-- Name: django_session django_session_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.django_session
    ADD CONSTRAINT django_session_pkey PRIMARY KEY (session_key);


--
-- Name: draft draft_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.draft
    ADD CONSTRAINT draft_pkey PRIMARY KEY (id);


--
-- Name: draft_type draft_type_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.draft_type
    ADD CONSTRAINT draft_type_pkey PRIMARY KEY (id);


--
-- Name: dynamic_forms dynamic_forms_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.dynamic_forms
    ADD CONSTRAINT dynamic_forms_pkey PRIMARY KEY (id);


--
-- Name: extract_file_data extract_file_data_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.extract_file_data
    ADD CONSTRAINT extract_file_data_pkey PRIMARY KEY (id);


--
-- Name: field_date_format_type field_date_format_type_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.field_date_format_type
    ADD CONSTRAINT field_date_format_type_pkey PRIMARY KEY (id);


--
-- Name: field_number_format_type field_number_format_type_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.field_number_format_type
    ADD CONSTRAINT field_number_format_type_pkey PRIMARY KEY (id);


--
-- Name: field_options field_options_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.field_options
    ADD CONSTRAINT field_options_pkey PRIMARY KEY (id);


--
-- Name: field_period_interval_type field_period_interval_type_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.field_period_interval_type
    ADD CONSTRAINT field_period_interval_type_pkey PRIMARY KEY (id);


--
-- Name: field field_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.field
    ADD CONSTRAINT field_pkey PRIMARY KEY (id);


--
-- Name: field_type field_type_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.field_type
    ADD CONSTRAINT field_type_pkey PRIMARY KEY (id);


--
-- Name: form_accessed_by form_accessed_by_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.form_accessed_by
    ADD CONSTRAINT form_accessed_by_pkey PRIMARY KEY (id);


--
-- Name: form form_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.form
    ADD CONSTRAINT form_pkey PRIMARY KEY (id);


--
-- Name: form_type form_type_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.form_type
    ADD CONSTRAINT form_type_pkey PRIMARY KEY (id);


--
-- Name: form_value form_value_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.form_value
    ADD CONSTRAINT form_value_pkey PRIMARY KEY (id);


--
-- Name: formula_attribute_type formula_attribute_type_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.formula_attribute_type
    ADD CONSTRAINT formula_attribute_type_pkey PRIMARY KEY (id);


--
-- Name: formula_context_attribute_type formula_context_attribute_type_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.formula_context_attribute_type
    ADD CONSTRAINT formula_context_attribute_type_pkey PRIMARY KEY (id);


--
-- Name: formula_context_for_company formula_context_for_company_company_id_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.formula_context_for_company
    ADD CONSTRAINT formula_context_for_company_company_id_key UNIQUE (company_id);


--
-- Name: formula_context_for_company formula_context_for_company_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.formula_context_for_company
    ADD CONSTRAINT formula_context_for_company_pkey PRIMARY KEY (id);


--
-- Name: formula_context_type formula_context_type_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.formula_context_type
    ADD CONSTRAINT formula_context_type_pkey PRIMARY KEY (id);


--
-- Name: formula_parameters_type formula_parameters_type_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.formula_parameters_type
    ADD CONSTRAINT formula_parameters_type_pkey PRIMARY KEY (id);


--
-- Name: formula_variable formula_variable_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.formula_variable
    ADD CONSTRAINT formula_variable_pkey PRIMARY KEY (id);


--
-- Name: group group_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."group"
    ADD CONSTRAINT group_pkey PRIMARY KEY (id);


--
-- Name: individual_charge_value_type individual_charge_value_type_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.individual_charge_value_type
    ADD CONSTRAINT individual_charge_value_type_pkey PRIMARY KEY (id);


--
-- Name: invoice_date_type invoice_date_type_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.invoice_date_type
    ADD CONSTRAINT invoice_date_type_pkey PRIMARY KEY (id);


--
-- Name: kanban_card_field kanban_card_field_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.kanban_card_field
    ADD CONSTRAINT kanban_card_field_pkey PRIMARY KEY (id);


--
-- Name: kanban_card kanban_card_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.kanban_card
    ADD CONSTRAINT kanban_card_pkey PRIMARY KEY (id);


--
-- Name: kanban_collapsed_option kanban_collapsed_option_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.kanban_collapsed_option
    ADD CONSTRAINT kanban_collapsed_option_pkey PRIMARY KEY (id);


--
-- Name: kanban_default kanban_default_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.kanban_default
    ADD CONSTRAINT kanban_default_pkey PRIMARY KEY (id);


--
-- Name: kanban_dimension_order kanban_dimension_order_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.kanban_dimension_order
    ADD CONSTRAINT kanban_dimension_order_pkey PRIMARY KEY (id);


--
-- Name: listing_selected_fields listing_selected_fields_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.listing_selected_fields
    ADD CONSTRAINT listing_selected_fields_pkey PRIMARY KEY (id);


--
-- Name: notification_configuration notification_configuration_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.notification_configuration
    ADD CONSTRAINT notification_configuration_pkey PRIMARY KEY (id);


--
-- Name: notification_configuration_variable notification_configuration_variable_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.notification_configuration_variable
    ADD CONSTRAINT notification_configuration_variable_pkey PRIMARY KEY (id);


--
-- Name: notification notification_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.notification
    ADD CONSTRAINT notification_pkey PRIMARY KEY (id);


--
-- Name: option_accessed_by option_accessed_by_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.option_accessed_by
    ADD CONSTRAINT option_accessed_by_pkey PRIMARY KEY (id);


--
-- Name: partner_default_and_discounts partner_default_and_discounts_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.partner_default_and_discounts
    ADD CONSTRAINT partner_default_and_discounts_pkey PRIMARY KEY (id);


--
-- Name: payment_method_type payment_method_type_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.payment_method_type
    ADD CONSTRAINT payment_method_type_pkey PRIMARY KEY (id);


--
-- Name: pdf_generated pdf_generated_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.pdf_generated
    ADD CONSTRAINT pdf_generated_pkey PRIMARY KEY (id);


--
-- Name: pdf_template_allowed_text_block pdf_template_allowed_text_block_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.pdf_template_allowed_text_block
    ADD CONSTRAINT pdf_template_allowed_text_block_pkey PRIMARY KEY (id);


--
-- Name: pdf_template_configuration pdf_template_configuration_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.pdf_template_configuration
    ADD CONSTRAINT pdf_template_configuration_pkey PRIMARY KEY (id);


--
-- Name: pdf_template_configuration_variables pdf_template_configuration_variables_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.pdf_template_configuration_variables
    ADD CONSTRAINT pdf_template_configuration_variables_pkey PRIMARY KEY (id);


--
-- Name: pre_notification pre_notification_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.pre_notification
    ADD CONSTRAINT pre_notification_pkey PRIMARY KEY (id);


--
-- Name: profiles profiles_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.profiles
    ADD CONSTRAINT profiles_pkey PRIMARY KEY (id);


--
-- Name: public_access public_access_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.public_access
    ADD CONSTRAINT public_access_pkey PRIMARY KEY (id);


--
-- Name: public_access public_access_user_id_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.public_access
    ADD CONSTRAINT public_access_user_id_key UNIQUE (user_id);


--
-- Name: public_access_field public_field_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.public_access_field
    ADD CONSTRAINT public_field_pkey PRIMARY KEY (id);


--
-- Name: public_access_form public_form_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.public_access_form
    ADD CONSTRAINT public_form_pkey PRIMARY KEY (id);


--
-- Name: push_notification push_notification_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.push_notification
    ADD CONSTRAINT push_notification_pkey PRIMARY KEY (id);


--
-- Name: push_notification_tag_type push_notification_tag_type_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.push_notification_tag_type
    ADD CONSTRAINT push_notification_tag_type_pkey PRIMARY KEY (id);


--
-- Name: raw_data_type raw_data_type_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.raw_data_type
    ADD CONSTRAINT raw_data_type_pkey PRIMARY KEY (id);


--
-- Name: user_notification read_notification_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.user_notification
    ADD CONSTRAINT read_notification_pkey PRIMARY KEY (id);


--
-- Name: text_alignment_type text_alignment_type_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.text_alignment_type
    ADD CONSTRAINT text_alignment_type_pkey PRIMARY KEY (id);


--
-- Name: text_block text_block_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.text_block
    ADD CONSTRAINT text_block_pkey PRIMARY KEY (id);


--
-- Name: text_block_type_can_contain_type text_block_type_can_contain_type_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.text_block_type_can_contain_type
    ADD CONSTRAINT text_block_type_can_contain_type_pkey PRIMARY KEY (id);


--
-- Name: text_block_type text_block_type_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.text_block_type
    ADD CONSTRAINT text_block_type_pkey PRIMARY KEY (id);


--
-- Name: text_content text_content_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.text_content
    ADD CONSTRAINT text_content_pkey PRIMARY KEY (id);


--
-- Name: text_image_option text_image_option_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.text_image_option
    ADD CONSTRAINT text_image_option_pkey PRIMARY KEY (id);


--
-- Name: text_list_option text_list_option_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.text_list_option
    ADD CONSTRAINT text_list_option_pkey PRIMARY KEY (id);


--
-- Name: text_list_type text_list_type_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.text_list_type
    ADD CONSTRAINT text_list_type_pkey PRIMARY KEY (id);


--
-- Name: text_page text_page_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.text_page
    ADD CONSTRAINT text_page_pkey PRIMARY KEY (id);


--
-- Name: text_table_option_column_dimension text_table_option_column_dimension_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.text_table_option_column_dimension
    ADD CONSTRAINT text_table_option_column_dimension_pkey PRIMARY KEY (id);


--
-- Name: text_table_option text_table_option_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.text_table_option
    ADD CONSTRAINT text_table_option_pkey PRIMARY KEY (id);


--
-- Name: text_table_option_row_dimension text_table_option_row_dimension_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.text_table_option_row_dimension
    ADD CONSTRAINT text_table_option_row_dimension_pkey PRIMARY KEY (id);


--
-- Name: text_text_option text_text_option_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.text_text_option
    ADD CONSTRAINT text_text_option_pkey PRIMARY KEY (id);


--
-- Name: theme_dashboard_chart_configuration theme_dashboard_chart_configuration_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.theme_dashboard_chart_configuration
    ADD CONSTRAINT theme_dashboard_chart_configuration_pkey PRIMARY KEY (id);


--
-- Name: theme_field_options theme_field_options_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.theme_field_options
    ADD CONSTRAINT theme_field_options_pkey PRIMARY KEY (id);


--
-- Name: theme_field theme_field_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.theme_field
    ADD CONSTRAINT theme_field_pkey PRIMARY KEY (id);


--
-- Name: theme_form theme_form_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.theme_form
    ADD CONSTRAINT theme_form_pkey PRIMARY KEY (id);


--
-- Name: theme_formula_variable theme_formula_variable_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.theme_formula_variable
    ADD CONSTRAINT theme_formula_variable_pkey PRIMARY KEY (id);


--
-- Name: theme_kanban_card_field theme_kanban_card_field_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.theme_kanban_card_field
    ADD CONSTRAINT theme_kanban_card_field_pkey PRIMARY KEY (id);


--
-- Name: theme_kanban_card theme_kanban_card_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.theme_kanban_card
    ADD CONSTRAINT theme_kanban_card_pkey PRIMARY KEY (id);


--
-- Name: theme_kanban_default theme_kanban_default_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.theme_kanban_default
    ADD CONSTRAINT theme_kanban_default_pkey PRIMARY KEY (id);


--
-- Name: theme_kanban_dimension_order theme_kanban_dimension_order_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.theme_kanban_dimension_order
    ADD CONSTRAINT theme_kanban_dimension_order_pkey PRIMARY KEY (id);


--
-- Name: theme_notification_configuration theme_notification_configuration_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.theme_notification_configuration
    ADD CONSTRAINT theme_notification_configuration_pkey PRIMARY KEY (id);


--
-- Name: theme_notification_configuration_variable theme_notification_configuration_variable_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.theme_notification_configuration_variable
    ADD CONSTRAINT theme_notification_configuration_variable_pkey PRIMARY KEY (id);


--
-- Name: theme_photos theme_photos_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.theme_photos
    ADD CONSTRAINT theme_photos_pkey PRIMARY KEY (id);


--
-- Name: theme theme_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.theme
    ADD CONSTRAINT theme_pkey PRIMARY KEY (id);


--
-- Name: user_accessed_by user_accessed_by_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.user_accessed_by
    ADD CONSTRAINT user_accessed_by_pkey PRIMARY KEY (id);


--
-- Name: users_groups users_groups_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.users_groups
    ADD CONSTRAINT users_groups_pkey PRIMARY KEY (id);


--
-- Name: users_groups users_groups_userextended_id_group_id_04b63ae6_uniq; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.users_groups
    ADD CONSTRAINT users_groups_userextended_id_group_id_04b63ae6_uniq UNIQUE (userextended_id, group_id);


--
-- Name: users users_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_pkey PRIMARY KEY (id);


--
-- Name: users_user_permissions users_user_permissions_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.users_user_permissions
    ADD CONSTRAINT users_user_permissions_pkey PRIMARY KEY (id);


--
-- Name: users_user_permissions users_user_permissions_userextended_id_permissi_0f974485_uniq; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.users_user_permissions
    ADD CONSTRAINT users_user_permissions_userextended_id_permissi_0f974485_uniq UNIQUE (userextended_id, permission_id);


--
-- Name: users users_username_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_username_key UNIQUE (username);


--
-- Name: attachments_field_id_55fdfd82; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX attachments_field_id_55fdfd82 ON public.attachments USING btree (field_id);


--
-- Name: attachments_form_id_5bdf972c; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX attachments_form_id_5bdf972c ON public.attachments USING btree (form_id);


--
-- Name: auth_group_name_a6ea08ec_like; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX auth_group_name_a6ea08ec_like ON public.auth_group USING btree (name varchar_pattern_ops);


--
-- Name: auth_group_permissions_group_id_b120cbf9; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX auth_group_permissions_group_id_b120cbf9 ON public.auth_group_permissions USING btree (group_id);


--
-- Name: auth_group_permissions_permission_id_84c5c92e; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX auth_group_permissions_permission_id_84c5c92e ON public.auth_group_permissions USING btree (permission_id);


--
-- Name: auth_permission_content_type_id_2f476e4b; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX auth_permission_content_type_id_2f476e4b ON public.auth_permission USING btree (content_type_id);


--
-- Name: client_value_field_id_3baf014f; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX client_value_field_id_3baf014f ON public.form_value USING btree (field_id);


--
-- Name: company_billing_charge_frequency_type_id_650785d2; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX company_billing_charge_frequency_type_id_650785d2 ON public.company_billing USING btree (charge_frequency_type_id);


--
-- Name: company_billing_invoice_date_type_id_c9c85363; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX company_billing_invoice_date_type_id_c9c85363 ON public.company_billing USING btree (invoice_date_type_id);


--
-- Name: company_billing_payment_method_type_id_dcc0a133; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX company_billing_payment_method_type_id_dcc0a133 ON public.company_billing USING btree (payment_method_type_id);


--
-- Name: company_billing_vindi_client_id_59d3a9a8; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX company_billing_vindi_client_id_59d3a9a8 ON public.company_billing USING btree (vindi_client_id);


--
-- Name: company_billing_vindi_client_id_59d3a9a8_like; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX company_billing_vindi_client_id_59d3a9a8_like ON public.company_billing USING btree (vindi_client_id varchar_pattern_ops);


--
-- Name: company_billing_vindi_payment_profile_id_b969ffa1; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX company_billing_vindi_payment_profile_id_b969ffa1 ON public.company_billing USING btree (vindi_payment_profile_id);


--
-- Name: company_billing_vindi_payment_profile_id_b969ffa1_like; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX company_billing_vindi_payment_profile_id_b969ffa1_like ON public.company_billing USING btree (vindi_payment_profile_id varchar_pattern_ops);


--
-- Name: company_billing_vindi_plan_id_25318798; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX company_billing_vindi_plan_id_25318798 ON public.company_billing USING btree (vindi_plan_id);


--
-- Name: company_billing_vindi_plan_id_25318798_like; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX company_billing_vindi_plan_id_25318798_like ON public.company_billing USING btree (vindi_plan_id varchar_pattern_ops);


--
-- Name: company_billing_vindi_product_id_9032af98; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX company_billing_vindi_product_id_9032af98 ON public.company_billing USING btree (vindi_product_id);


--
-- Name: company_billing_vindi_product_id_9032af98_like; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX company_billing_vindi_product_id_9032af98_like ON public.company_billing USING btree (vindi_product_id varchar_pattern_ops);


--
-- Name: company_billing_vindi_signature_id_ac5eca77; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX company_billing_vindi_signature_id_ac5eca77 ON public.company_billing USING btree (vindi_signature_id);


--
-- Name: company_billing_vindi_signature_id_ac5eca77_like; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX company_billing_vindi_signature_id_ac5eca77_like ON public.company_billing USING btree (vindi_signature_id varchar_pattern_ops);


--
-- Name: company_charge_company_id_feb35ee8; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX company_charge_company_id_feb35ee8 ON public.company_charge USING btree (company_id);


--
-- Name: company_company_type_id_49995cec; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX company_company_type_id_49995cec ON public.company USING btree (company_type_id);


--
-- Name: company_coupon_company_id_74464616; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX company_coupon_company_id_74464616 ON public.company_coupon USING btree (company_id);


--
-- Name: company_coupon_discount_coupon_id_43a83526; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX company_coupon_discount_coupon_id_43a83526 ON public.company_coupon USING btree (discount_coupon_id);


--
-- Name: company_endpoint_c1395016; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX company_endpoint_c1395016 ON public.company USING btree (endpoint);


--
-- Name: company_endpoint_c1395016_like; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX company_endpoint_c1395016_like ON public.company USING btree (endpoint varchar_pattern_ops);


--
-- Name: company_invoice_mails_company_id_eefef680; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX company_invoice_mails_company_id_eefef680 ON public.company_invoice_mails USING btree (company_id);


--
-- Name: company_is_active_e2114ea6; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX company_is_active_e2114ea6 ON public.company USING btree (is_active);


--
-- Name: company_name_5abe57d9; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX company_name_5abe57d9 ON public.company USING btree (name);


--
-- Name: company_name_5abe57d9_like; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX company_name_5abe57d9_like ON public.company USING btree (name varchar_pattern_ops);


--
-- Name: company_shared_by_id_9c427260; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX company_shared_by_id_9c427260 ON public.company USING btree (shared_by_id);


--
-- Name: conditional_type_type_2dd5d988; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX conditional_type_type_2dd5d988 ON public.conditional_type USING btree (type);


--
-- Name: conditional_type_type_2dd5d988_like; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX conditional_type_type_2dd5d988_like ON public.conditional_type USING btree (type varchar_pattern_ops);


--
-- Name: current_company_charge_company_id_3161bb10; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX current_company_charge_company_id_3161bb10 ON public.current_company_charge USING btree (company_id);


--
-- Name: current_company_charge_discount_by_individual_value_id_365faa60; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX current_company_charge_discount_by_individual_value_id_365faa60 ON public.current_company_charge USING btree (discount_by_individual_value_id);


--
-- Name: current_company_charge_individual_charge_value_type_id_cb192b02; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX current_company_charge_individual_charge_value_type_id_cb192b02 ON public.current_company_charge USING btree (individual_charge_value_type_id);


--
-- Name: dashboard_chart_configuration_aggregation_type_id_aeccf5b6; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX dashboard_chart_configuration_aggregation_type_id_aeccf5b6 ON public.dashboard_chart_configuration USING btree (aggregation_type_id);


--
-- Name: dashboard_chart_configuration_chart_type_id_2f0767e6; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX dashboard_chart_configuration_chart_type_id_2f0767e6 ON public.dashboard_chart_configuration USING btree (chart_type_id);


--
-- Name: dashboard_chart_configuration_company_id_a0fa9a47; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX dashboard_chart_configuration_company_id_a0fa9a47 ON public.dashboard_chart_configuration USING btree (company_id);


--
-- Name: dashboard_chart_configuration_form_id_7ce5f68f; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX dashboard_chart_configuration_form_id_7ce5f68f ON public.dashboard_chart_configuration USING btree (form_id);


--
-- Name: dashboard_chart_configuration_label_field_id_71e9f8ce; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX dashboard_chart_configuration_label_field_id_71e9f8ce ON public.dashboard_chart_configuration USING btree (label_field_id);


--
-- Name: dashboard_chart_configuration_number_format_type_id_2b3e5424; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX dashboard_chart_configuration_number_format_type_id_2b3e5424 ON public.dashboard_chart_configuration USING btree (number_format_type_id);


--
-- Name: dashboard_chart_configuration_user_id_0da2430a; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX dashboard_chart_configuration_user_id_0da2430a ON public.dashboard_chart_configuration USING btree (user_id);


--
-- Name: dashboard_chart_configuration_value_field_id_ca43ce88; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX dashboard_chart_configuration_value_field_id_ca43ce88 ON public.dashboard_chart_configuration USING btree (value_field_id);


--
-- Name: date_format_type_type_d09147c2; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX date_format_type_type_d09147c2 ON public.field_date_format_type USING btree (type);


--
-- Name: date_format_type_type_d09147c2_like; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX date_format_type_type_d09147c2_like ON public.field_date_format_type USING btree (type varchar_pattern_ops);


--
-- Name: default_field_value_default_attachment_id_a912c819; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX default_field_value_default_attachment_id_a912c819 ON public.default_field_value USING btree (default_attachment_id);


--
-- Name: default_field_value_field_id_af9c4985; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX default_field_value_field_id_af9c4985 ON public.default_field_value USING btree (field_id);


--
-- Name: discount_by_individual_nam_individual_charge_value_ty_961f5cd9; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX discount_by_individual_nam_individual_charge_value_ty_961f5cd9 ON public.discount_by_individual_name_for_company USING btree (individual_charge_value_type_id);


--
-- Name: discount_by_individual_name_for_company_company_id_b64759fa; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX discount_by_individual_name_for_company_company_id_b64759fa ON public.discount_by_individual_name_for_company USING btree (company_id);


--
-- Name: discount_by_individual_val_individual_charge_value_ty_6081625a; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX discount_by_individual_val_individual_charge_value_ty_6081625a ON public.discount_by_individual_value_quantity USING btree (individual_charge_value_type_id);


--
-- Name: discount_coupon_name_1e6c0f03_like; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX discount_coupon_name_1e6c0f03_like ON public.discount_coupon USING btree (name varchar_pattern_ops);


--
-- Name: django_admin_log_content_type_id_c4bce8eb; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX django_admin_log_content_type_id_c4bce8eb ON public.django_admin_log USING btree (content_type_id);


--
-- Name: django_admin_log_user_id_c564eba6; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX django_admin_log_user_id_c564eba6 ON public.django_admin_log USING btree (user_id);


--
-- Name: django_celery_results_taskresult_date_done_49edada6; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX django_celery_results_taskresult_date_done_49edada6 ON public.django_celery_results_taskresult USING btree (date_done);


--
-- Name: django_celery_results_taskresult_hidden_cd77412f; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX django_celery_results_taskresult_hidden_cd77412f ON public.django_celery_results_taskresult USING btree (hidden);


--
-- Name: django_celery_results_taskresult_status_cbbed23a; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX django_celery_results_taskresult_status_cbbed23a ON public.django_celery_results_taskresult USING btree (status);


--
-- Name: django_celery_results_taskresult_status_cbbed23a_like; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX django_celery_results_taskresult_status_cbbed23a_like ON public.django_celery_results_taskresult USING btree (status varchar_pattern_ops);


--
-- Name: django_celery_results_taskresult_task_id_de0d95bf_like; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX django_celery_results_taskresult_task_id_de0d95bf_like ON public.django_celery_results_taskresult USING btree (task_id varchar_pattern_ops);


--
-- Name: django_celery_results_taskresult_task_name_90987df3; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX django_celery_results_taskresult_task_name_90987df3 ON public.django_celery_results_taskresult USING btree (task_name);


--
-- Name: django_celery_results_taskresult_task_name_90987df3_like; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX django_celery_results_taskresult_task_name_90987df3_like ON public.django_celery_results_taskresult USING btree (task_name varchar_pattern_ops);


--
-- Name: django_session_expire_date_a5c62663; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX django_session_expire_date_a5c62663 ON public.django_session USING btree (expire_date);


--
-- Name: django_session_session_key_c0390e0f_like; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX django_session_session_key_c0390e0f_like ON public.django_session USING btree (session_key varchar_pattern_ops);


--
-- Name: draft_company_id_012e59c5; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX draft_company_id_012e59c5 ON public.draft USING btree (company_id);


--
-- Name: draft_draft_type_id_0c28fdfb; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX draft_draft_type_id_0c28fdfb ON public.draft USING btree (draft_type_id);


--
-- Name: draft_user_id_8443874d; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX draft_user_id_8443874d ON public.draft USING btree (user_id);


--
-- Name: dynamic_forms_company_id_90ceb630; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX dynamic_forms_company_id_90ceb630 ON public.dynamic_forms USING btree (company_id);


--
-- Name: dynamic_forms_depends_on_id_afad9c4d; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX dynamic_forms_depends_on_id_afad9c4d ON public.dynamic_forms USING btree (depends_on_id);


--
-- Name: dynamic_forms_form_id_9a55a4de; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX dynamic_forms_form_id_9a55a4de ON public.dynamic_forms USING btree (form_id);


--
-- Name: dynamic_forms_user_id_ff8e8c6b; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX dynamic_forms_user_id_ff8e8c6b ON public.dynamic_forms USING btree (user_id);


--
-- Name: dynamic_forms_uuid_90126496; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX dynamic_forms_uuid_90126496 ON public.dynamic_forms USING btree (uuid);


--
-- Name: extract_file_data_company_id_95ab6e22; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX extract_file_data_company_id_95ab6e22 ON public.extract_file_data USING btree (company_id);


--
-- Name: extract_file_data_form_id_309fe470; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX extract_file_data_form_id_309fe470 ON public.extract_file_data USING btree (form_id);


--
-- Name: extract_file_data_user_id_55975de3; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX extract_file_data_user_id_55975de3 ON public.extract_file_data USING btree (user_id);


--
-- Name: field_date_configuration_date_format_type_id_ccea048c; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX field_date_configuration_date_format_type_id_ccea048c ON public.field USING btree (date_configuration_date_format_type_id);


--
-- Name: field_date_format_type_type_c330157a; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX field_date_format_type_type_c330157a ON public.field_date_format_type USING btree (type);


--
-- Name: field_date_format_type_type_c330157a_like; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX field_date_format_type_type_c330157a_like ON public.field_date_format_type USING btree (type varchar_pattern_ops);


--
-- Name: field_enabled_9d39cb49; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX field_enabled_9d39cb49 ON public.field USING btree (enabled);


--
-- Name: field_form_field_as_option_id_790da294; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX field_form_field_as_option_id_790da294 ON public.field USING btree (form_field_as_option_id);


--
-- Name: field_form_id_f6498ce2; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX field_form_id_f6498ce2 ON public.field USING btree (form_id);


--
-- Name: field_name_d1148ee8; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX field_name_d1148ee8 ON public.field USING btree (name);


--
-- Name: field_name_d1148ee8_like; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX field_name_d1148ee8_like ON public.field USING btree (name varchar_pattern_ops);


--
-- Name: field_number_configuration_number_format_type_id_fab9ea10; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX field_number_configuration_number_format_type_id_fab9ea10 ON public.field USING btree (number_configuration_number_format_type_id);


--
-- Name: field_number_format_type_type_5c14f471; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX field_number_format_type_type_5c14f471 ON public.field_number_format_type USING btree (type);


--
-- Name: field_number_format_type_type_5c14f471_like; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX field_number_format_type_type_5c14f471_like ON public.field_number_format_type USING btree (type varchar_pattern_ops);


--
-- Name: field_options_field_id_6b8a308b; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX field_options_field_id_6b8a308b ON public.field_options USING btree (field_id);


--
-- Name: field_options_option_fa45a392; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX field_options_option_fa45a392 ON public.field_options USING btree (option);


--
-- Name: field_options_option_fa45a392_like; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX field_options_option_fa45a392_like ON public.field_options USING btree (option varchar_pattern_ops);


--
-- Name: field_period_configuration_period_interval_type_id_4f8c8b02; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX field_period_configuration_period_interval_type_id_4f8c8b02 ON public.field USING btree (period_configuration_period_interval_type_id);


--
-- Name: field_period_interval_type_type_a05d7b19; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX field_period_interval_type_type_a05d7b19 ON public.field_period_interval_type USING btree (type);


--
-- Name: field_period_interval_type_type_a05d7b19_like; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX field_period_interval_type_type_a05d7b19_like ON public.field_period_interval_type USING btree (type varchar_pattern_ops);


--
-- Name: field_type_id_381a7c0e; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX field_type_id_381a7c0e ON public.field USING btree (type_id);


--
-- Name: field_type_type_5ae31dfb; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX field_type_type_5ae31dfb ON public.field_type USING btree (type);


--
-- Name: field_type_type_5ae31dfb_like; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX field_type_type_5ae31dfb_like ON public.field_type USING btree (type varchar_pattern_ops);


--
-- Name: form_accessed_by_form_id_58286c27; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX form_accessed_by_form_id_58286c27 ON public.form_accessed_by USING btree (form_id);


--
-- Name: form_accessed_by_user_id_d8d74f36; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX form_accessed_by_user_id_d8d74f36 ON public.form_accessed_by USING btree (user_id);


--
-- Name: form_company_id_7c58249b; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX form_company_id_7c58249b ON public.form USING btree (company_id);


--
-- Name: form_conditional_on_field_id_23d83574; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX form_conditional_on_field_id_23d83574 ON public.form USING btree (conditional_on_field_id);


--
-- Name: form_conditional_type_id_9cf60a7e; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX form_conditional_type_id_9cf60a7e ON public.form USING btree (conditional_type_id);


--
-- Name: form_depends_on_id_3e8981a6; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX form_depends_on_id_3e8981a6 ON public.form USING btree (depends_on_id);


--
-- Name: form_form_name_57cd55b1; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX form_form_name_57cd55b1 ON public.form USING btree (form_name);


--
-- Name: form_form_name_57cd55b1_like; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX form_form_name_57cd55b1_like ON public.form USING btree (form_name varchar_pattern_ops);


--
-- Name: form_group_id_c3bfdf09; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX form_group_id_c3bfdf09 ON public.form USING btree (group_id);


--
-- Name: form_type_id_11618d02; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX form_type_id_11618d02 ON public.form USING btree (type_id);


--
-- Name: form_type_type_7afb2c09; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX form_type_type_7afb2c09 ON public.form_type USING btree (type);


--
-- Name: form_type_type_7afb2c09_like; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX form_type_type_7afb2c09_like ON public.form_type USING btree (type varchar_pattern_ops);


--
-- Name: form_value_company_id_a82640de; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX form_value_company_id_a82640de ON public.form_value USING btree (company_id);


--
-- Name: form_value_date_configuration_date_format_type_id_44da5d52; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX form_value_date_configuration_date_format_type_id_44da5d52 ON public.form_value USING btree (date_configuration_date_format_type_id);


--
-- Name: form_value_date_format_type_id_29e254d1; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX form_value_date_format_type_id_29e254d1 ON public.form_value USING btree (date_configuration_date_format_type_id);


--
-- Name: form_value_field_id_9fa432fe; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX form_value_field_id_9fa432fe ON public.form_value USING btree (field_id);


--
-- Name: form_value_field_type_id_6f20e5ea; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX form_value_field_type_id_6f20e5ea ON public.form_value USING btree (field_type_id);


--
-- Name: form_value_form_field_as_option_id_b768e543; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX form_value_form_field_as_option_id_b768e543 ON public.form_value USING btree (form_field_as_option_id);


--
-- Name: form_value_form_id_c08e4676; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX form_value_form_id_c08e4676 ON public.form_value USING btree (form_id);


--
-- Name: form_value_number_configuration_number_format_type_id_a91154d8; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX form_value_number_configuration_number_format_type_id_a91154d8 ON public.form_value USING btree (number_configuration_number_format_type_id);


--
-- Name: form_value_period_configuration_perio_2f38b2dd; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX form_value_period_configuration_perio_2f38b2dd ON public.form_value USING btree (period_configuration_period_interval_type_id);


--
-- Name: form_value_period_interval_type_id_395ee092; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX form_value_period_interval_type_id_395ee092 ON public.form_value USING btree (period_configuration_period_interval_type_id);


--
-- Name: formula_context_attribute_type_attribute_type_id_0d76f692; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX formula_context_attribute_type_attribute_type_id_0d76f692 ON public.formula_context_attribute_type USING btree (attribute_type_id);


--
-- Name: formula_context_attribute_type_context_type_id_fe8c0a50; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX formula_context_attribute_type_context_type_id_fe8c0a50 ON public.formula_context_attribute_type USING btree (context_type_id);


--
-- Name: formula_context_for_company_context_type_id_702ab3dc; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX formula_context_for_company_context_type_id_702ab3dc ON public.formula_context_for_company USING btree (context_type_id);


--
-- Name: formula_parameters_type_formula_type_id_ae2a8404; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX formula_parameters_type_formula_type_id_ae2a8404 ON public.formula_parameters_type USING btree (formula_type_id);


--
-- Name: formula_parameters_type_raw_data_type_id_c92e728a; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX formula_parameters_type_raw_data_type_id_c92e728a ON public.formula_parameters_type USING btree (raw_data_type_id);


--
-- Name: formula_variable_field_id_1e593a29; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX formula_variable_field_id_1e593a29 ON public.formula_variable USING btree (field_id);


--
-- Name: formula_variable_variable_id_01badc58; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX formula_variable_variable_id_01badc58 ON public.formula_variable USING btree (variable_id);


--
-- Name: group_company_id_2f2f8544; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX group_company_id_2f2f8544 ON public."group" USING btree (company_id);


--
-- Name: individual_charge_value_type_charge_frequency_type_id_327bdc4b; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX individual_charge_value_type_charge_frequency_type_id_327bdc4b ON public.individual_charge_value_type USING btree (charge_frequency_type_id);


--
-- Name: individual_charge_value_type_charge_type_id_5a999b80; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX individual_charge_value_type_charge_type_id_5a999b80 ON public.individual_charge_value_type USING btree (charge_type_id);


--
-- Name: kanban_card_company_id_04a5dc79; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX kanban_card_company_id_04a5dc79 ON public.kanban_card USING btree (company_id);


--
-- Name: kanban_card_field_field_id_ef99ecd8; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX kanban_card_field_field_id_ef99ecd8 ON public.kanban_card_field USING btree (field_id);


--
-- Name: kanban_card_field_kanban_card_id_ee60c842; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX kanban_card_field_kanban_card_id_ee60c842 ON public.kanban_card_field USING btree (kanban_card_id);


--
-- Name: kanban_card_form_id_7ef5ffcb; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX kanban_card_form_id_7ef5ffcb ON public.kanban_card USING btree (form_id);


--
-- Name: kanban_card_user_id_080c1fad; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX kanban_card_user_id_080c1fad ON public.kanban_card USING btree (user_id);


--
-- Name: kanban_collapsed_option_company_id_315c2003; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX kanban_collapsed_option_company_id_315c2003 ON public.kanban_collapsed_option USING btree (company_id);


--
-- Name: kanban_collapsed_option_options_id_0d430dc9; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX kanban_collapsed_option_options_id_0d430dc9 ON public.kanban_collapsed_option USING btree (field_option_id);


--
-- Name: kanban_collapsed_option_user_id_a9512aa8; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX kanban_collapsed_option_user_id_a9512aa8 ON public.kanban_collapsed_option USING btree (user_id);


--
-- Name: kanban_default_company_id_5180899b; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX kanban_default_company_id_5180899b ON public.kanban_default USING btree (company_id);


--
-- Name: kanban_default_form_id_cee65b7a; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX kanban_default_form_id_cee65b7a ON public.kanban_default USING btree (form_id);


--
-- Name: kanban_default_kanban_card_id_bb2c6660; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX kanban_default_kanban_card_id_bb2c6660 ON public.kanban_default USING btree (kanban_card_id);


--
-- Name: kanban_default_kanban_dimension_id_292c6e3f; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX kanban_default_kanban_dimension_id_292c6e3f ON public.kanban_default USING btree (kanban_dimension_id);


--
-- Name: kanban_default_user_id_7e7d4ea4; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX kanban_default_user_id_7e7d4ea4 ON public.kanban_default USING btree (user_id);


--
-- Name: kanban_dimension_order_dimension_id_811c5433; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX kanban_dimension_order_dimension_id_811c5433 ON public.kanban_dimension_order USING btree (dimension_id);


--
-- Name: kanban_dimension_order_user_id_24a5dcc4; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX kanban_dimension_order_user_id_24a5dcc4 ON public.kanban_dimension_order USING btree (user_id);


--
-- Name: listing_selected_fields_field_id_72001c52; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX listing_selected_fields_field_id_72001c52 ON public.listing_selected_fields USING btree (field_id);


--
-- Name: listing_selected_fields_user_id_8b799c65; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX listing_selected_fields_user_id_8b799c65 ON public.listing_selected_fields USING btree (user_id);


--
-- Name: notification_configuration_days_diff_8ed8c1ee; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX notification_configuration_days_diff_8ed8c1ee ON public.notification_configuration USING btree (days_diff);


--
-- Name: notification_configuration_days_diff_8ed8c1ee_like; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX notification_configuration_days_diff_8ed8c1ee_like ON public.notification_configuration USING btree (days_diff varchar_pattern_ops);


--
-- Name: notification_configuration_field_id_557c4e2d; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX notification_configuration_field_id_557c4e2d ON public.notification_configuration USING btree (field_id);


--
-- Name: notification_configuration_form_id_2f860863; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX notification_configuration_form_id_2f860863 ON public.notification_configuration USING btree (form_id);


--
-- Name: notification_configuration_notification_configuration_b14b5183; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX notification_configuration_notification_configuration_b14b5183 ON public.notification_configuration_variable USING btree (notification_configuration_id);


--
-- Name: notification_configuration_user_id_439ec0f7; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX notification_configuration_user_id_439ec0f7 ON public.notification_configuration USING btree (user_id);


--
-- Name: notification_configuration_variable_field_id_7c30a815; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX notification_configuration_variable_field_id_7c30a815 ON public.notification_configuration_variable USING btree (field_id);


--
-- Name: notification_form_id_6c692edb; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX notification_form_id_6c692edb ON public.notification USING btree (form_id);


--
-- Name: notification_notification_configuration_id_b91fecd8; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX notification_notification_configuration_id_b91fecd8 ON public.notification USING btree (notification_configuration_id);


--
-- Name: notification_user_id_1002fc38; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX notification_user_id_1002fc38 ON public.notification USING btree (user_id);


--
-- Name: option_accessed_by_field_option_id_eecb860e; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX option_accessed_by_field_option_id_eecb860e ON public.option_accessed_by USING btree (field_option_id);


--
-- Name: option_accessed_by_user_id_ce4ac9c6; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX option_accessed_by_user_id_ce4ac9c6 ON public.option_accessed_by USING btree (user_id);


--
-- Name: partner_default_and_discou_individual_charge_value_ty_aeb75e21; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX partner_default_and_discou_individual_charge_value_ty_aeb75e21 ON public.partner_default_and_discounts USING btree (individual_charge_value_type_id);


--
-- Name: pdf_generated_company_id_3c1c32c2; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX pdf_generated_company_id_3c1c32c2 ON public.pdf_generated USING btree (company_id);


--
-- Name: pdf_generated_pdf_template_id_c6d92617; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX pdf_generated_pdf_template_id_c6d92617 ON public.pdf_generated USING btree (pdf_template_id);


--
-- Name: pdf_generated_user_id_048f0892; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX pdf_generated_user_id_048f0892 ON public.pdf_generated USING btree (user_id);


--
-- Name: pdf_template_allowed_text_block_block_id_5a06c389; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX pdf_template_allowed_text_block_block_id_5a06c389 ON public.pdf_template_allowed_text_block USING btree (block_id);


--
-- Name: pdf_template_configuration_company_id_31b02fed; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX pdf_template_configuration_company_id_31b02fed ON public.pdf_template_configuration USING btree (company_id);


--
-- Name: pdf_template_configuration_form_id_4c85a2fc; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX pdf_template_configuration_form_id_4c85a2fc ON public.pdf_template_configuration USING btree (form_id);


--
-- Name: pdf_template_configuration_rich_text_id_2d3f78c9; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX pdf_template_configuration_rich_text_id_2d3f78c9 ON public.pdf_template_configuration USING btree (rich_text_page_id);


--
-- Name: pdf_template_configuration_user_id_c8eba5ed; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX pdf_template_configuration_user_id_c8eba5ed ON public.pdf_template_configuration USING btree (user_id);


--
-- Name: pdf_template_configuration_variables_field_id_25245e76; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX pdf_template_configuration_variables_field_id_25245e76 ON public.pdf_template_configuration_variables USING btree (field_id);


--
-- Name: pdf_template_configuration_variables_pdf_template_id_db06b600; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX pdf_template_configuration_variables_pdf_template_id_db06b600 ON public.pdf_template_configuration_variables USING btree (pdf_template_id);


--
-- Name: period_interval_type_type_e942d75c; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX period_interval_type_type_e942d75c ON public.field_period_interval_type USING btree (type);


--
-- Name: period_interval_type_type_e942d75c_like; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX period_interval_type_type_e942d75c_like ON public.field_period_interval_type USING btree (type varchar_pattern_ops);


--
-- Name: pre_notification_dynamic_form_id_913c4ad7; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX pre_notification_dynamic_form_id_913c4ad7 ON public.pre_notification USING btree (dynamic_form_id);


--
-- Name: pre_notification_notification_configuration_id_d65be96c; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX pre_notification_notification_configuration_id_d65be96c ON public.pre_notification USING btree (notification_configuration_id);


--
-- Name: pre_notification_user_id_5b8b68ac; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX pre_notification_user_id_5b8b68ac ON public.pre_notification USING btree (user_id);


--
-- Name: public_access_company_id_5ee02e79; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX public_access_company_id_5ee02e79 ON public.public_access USING btree (company_id);


--
-- Name: public_access_public_key_c7337bb3; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX public_access_public_key_c7337bb3 ON public.public_access USING btree (public_key);


--
-- Name: public_field_form_id_abe24530; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX public_field_form_id_abe24530 ON public.public_access_field USING btree (field_id);


--
-- Name: public_field_public_access_id_e842b051; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX public_field_public_access_id_e842b051 ON public.public_access_field USING btree (public_access_id);


--
-- Name: public_field_public_form_id_a974cad8; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX public_field_public_form_id_a974cad8 ON public.public_access_field USING btree (public_form_id);


--
-- Name: public_form_form_id_a176af65; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX public_form_form_id_a176af65 ON public.public_access_form USING btree (form_id);


--
-- Name: public_form_public_access_id_5d292c70; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX public_form_public_access_id_5d292c70 ON public.public_access_form USING btree (public_access_id);


--
-- Name: push_notification_push_notification_tag_type_id_e42bfbc0; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX push_notification_push_notification_tag_type_id_e42bfbc0 ON public.push_notification USING btree (push_notification_tag_type_id);


--
-- Name: push_notification_user_id_3ed35132; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX push_notification_user_id_3ed35132 ON public.push_notification USING btree (user_id);


--
-- Name: read_notification_notification_id_e4e1de6d; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX read_notification_notification_id_e4e1de6d ON public.user_notification USING btree (notification_id);


--
-- Name: read_notification_user_id_fc1a8b5b; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX read_notification_user_id_fc1a8b5b ON public.user_notification USING btree (user_id);


--
-- Name: text_block_block_type_id_456e6e02; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX text_block_block_type_id_456e6e02 ON public.text_block USING btree (block_type_id);


--
-- Name: text_block_depends_on_id_d159e181; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX text_block_depends_on_id_d159e181 ON public.text_block USING btree (depends_on_id);


--
-- Name: text_block_image_option_id_7564dcd9; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX text_block_image_option_id_7564dcd9 ON public.text_block USING btree (image_option_id);


--
-- Name: text_block_list_option_id_12b54060; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX text_block_list_option_id_12b54060 ON public.text_block USING btree (list_option_id);


--
-- Name: text_block_page_id_754b5d95; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX text_block_page_id_754b5d95 ON public.text_block USING btree (page_id);


--
-- Name: text_block_table_option_id_e54921bf; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX text_block_table_option_id_e54921bf ON public.text_block USING btree (table_option_id);


--
-- Name: text_block_text_option_id_e0386baa; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX text_block_text_option_id_e0386baa ON public.text_block USING btree (text_option_id);


--
-- Name: text_block_type_can_contain_type_block_id_6883c6c0; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX text_block_type_can_contain_type_block_id_6883c6c0 ON public.text_block_type_can_contain_type USING btree (block_id);


--
-- Name: text_block_type_can_contain_type_contain_id_407b77b2; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX text_block_type_can_contain_type_contain_id_407b77b2 ON public.text_block_type_can_contain_type USING btree (contain_id);


--
-- Name: text_block_uuid_81a7617d; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX text_block_uuid_81a7617d ON public.text_block USING btree (uuid);


--
-- Name: text_content_block_id_fcf310b6; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX text_content_block_id_fcf310b6 ON public.text_content USING btree (block_id);


--
-- Name: text_content_uuid_eccafae3; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX text_content_uuid_eccafae3 ON public.text_content USING btree (uuid);


--
-- Name: text_image_option_file_image_uuid_a2b99eec; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX text_image_option_file_image_uuid_a2b99eec ON public.text_image_option USING btree (file_image_uuid);


--
-- Name: text_list_option_list_type_id_6594d736; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX text_list_option_list_type_id_6594d736 ON public.text_list_option USING btree (list_type_id);


--
-- Name: text_page_company_id_29e50b4e; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX text_page_company_id_29e50b4e ON public.text_page USING btree (company_id);


--
-- Name: text_page_user_id_c020e567; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX text_page_user_id_c020e567 ON public.text_page USING btree (user_id);


--
-- Name: text_table_option_column_d_text_table_option_id_162822d8; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX text_table_option_column_d_text_table_option_id_162822d8 ON public.text_table_option_column_dimension USING btree (text_table_option_id);


--
-- Name: text_table_option_row_dimension_text_table_option_id_530f5664; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX text_table_option_row_dimension_text_table_option_id_530f5664 ON public.text_table_option_row_dimension USING btree (text_table_option_id);


--
-- Name: text_text_option_alignment_type_id_743cafc3; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX text_text_option_alignment_type_id_743cafc3 ON public.text_text_option USING btree (alignment_type_id);


--
-- Name: theme_company_id_f4947892; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX theme_company_id_f4947892 ON public.theme USING btree (company_id);


--
-- Name: theme_company_type_id_55ba6521; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX theme_company_type_id_55ba6521 ON public.theme USING btree (theme_type_id);


--
-- Name: theme_dashboard_chart_conf_aggregation_type_id_5b260d82; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX theme_dashboard_chart_conf_aggregation_type_id_5b260d82 ON public.theme_dashboard_chart_configuration USING btree (aggregation_type_id);


--
-- Name: theme_dashboard_chart_conf_number_format_type_id_6d099b38; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX theme_dashboard_chart_conf_number_format_type_id_6d099b38 ON public.theme_dashboard_chart_configuration USING btree (number_format_type_id);


--
-- Name: theme_dashboard_chart_configuration_chart_type_id_0bd7cd7c; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX theme_dashboard_chart_configuration_chart_type_id_0bd7cd7c ON public.theme_dashboard_chart_configuration USING btree (chart_type_id);


--
-- Name: theme_dashboard_chart_configuration_form_id_028f6eaf; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX theme_dashboard_chart_configuration_form_id_028f6eaf ON public.theme_dashboard_chart_configuration USING btree (form_id);


--
-- Name: theme_dashboard_chart_configuration_label_field_id_b9b8dc8e; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX theme_dashboard_chart_configuration_label_field_id_b9b8dc8e ON public.theme_dashboard_chart_configuration USING btree (label_field_id);


--
-- Name: theme_dashboard_chart_configuration_theme_id_47624a66; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX theme_dashboard_chart_configuration_theme_id_47624a66 ON public.theme_dashboard_chart_configuration USING btree (theme_id);


--
-- Name: theme_dashboard_chart_configuration_value_field_id_2fdc2fac; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX theme_dashboard_chart_configuration_value_field_id_2fdc2fac ON public.theme_dashboard_chart_configuration USING btree (value_field_id);


--
-- Name: theme_field_date_configuration_date_format_type_id_1ccb4d8f; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX theme_field_date_configuration_date_format_type_id_1ccb4d8f ON public.theme_field USING btree (date_configuration_date_format_type_id);


--
-- Name: theme_field_form_field_as_option_id_8fd62607; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX theme_field_form_field_as_option_id_8fd62607 ON public.theme_field USING btree (form_field_as_option_id);


--
-- Name: theme_field_form_id_1989d247; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX theme_field_form_id_1989d247 ON public.theme_field USING btree (form_id);


--
-- Name: theme_field_name_7539970b; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX theme_field_name_7539970b ON public.theme_field USING btree (name);


--
-- Name: theme_field_name_7539970b_like; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX theme_field_name_7539970b_like ON public.theme_field USING btree (name varchar_pattern_ops);


--
-- Name: theme_field_number_configuration_number_format_type_id_a1ccb8a5; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX theme_field_number_configuration_number_format_type_id_a1ccb8a5 ON public.theme_field USING btree (number_configuration_number_format_type_id);


--
-- Name: theme_field_options_field_id_f05e2744; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX theme_field_options_field_id_f05e2744 ON public.theme_field_options USING btree (field_id);


--
-- Name: theme_field_options_option_28f94a7f; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX theme_field_options_option_28f94a7f ON public.theme_field_options USING btree (option);


--
-- Name: theme_field_options_option_28f94a7f_like; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX theme_field_options_option_28f94a7f_like ON public.theme_field_options USING btree (option varchar_pattern_ops);


--
-- Name: theme_field_period_configuration_perio_30743340; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX theme_field_period_configuration_perio_30743340 ON public.theme_field USING btree (period_configuration_period_interval_type_id);


--
-- Name: theme_field_type_id_e61914b1; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX theme_field_type_id_e61914b1 ON public.theme_field USING btree (type_id);


--
-- Name: theme_form_conditional_on_field_id_e50652f8; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX theme_form_conditional_on_field_id_e50652f8 ON public.theme_form USING btree (conditional_on_field_id);


--
-- Name: theme_form_conditional_type_id_208792dd; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX theme_form_conditional_type_id_208792dd ON public.theme_form USING btree (conditional_type_id);


--
-- Name: theme_form_depends_on_id_a15f89bc; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX theme_form_depends_on_id_a15f89bc ON public.theme_form USING btree (depends_on_id);


--
-- Name: theme_form_form_name_ccaf558e; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX theme_form_form_name_ccaf558e ON public.theme_form USING btree (form_name);


--
-- Name: theme_form_form_name_ccaf558e_like; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX theme_form_form_name_ccaf558e_like ON public.theme_form USING btree (form_name varchar_pattern_ops);


--
-- Name: theme_form_theme_id_3fc4fb3f; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX theme_form_theme_id_3fc4fb3f ON public.theme_form USING btree (theme_id);


--
-- Name: theme_form_type_id_4bac8752; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX theme_form_type_id_4bac8752 ON public.theme_form USING btree (type_id);


--
-- Name: theme_formula_variable_field_id_7bb08f75; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX theme_formula_variable_field_id_7bb08f75 ON public.theme_formula_variable USING btree (field_id);


--
-- Name: theme_formula_variable_variable_id_c787db1f; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX theme_formula_variable_variable_id_c787db1f ON public.theme_formula_variable USING btree (variable_id);


--
-- Name: theme_kanban_card_field_field_id_b38ea031; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX theme_kanban_card_field_field_id_b38ea031 ON public.theme_kanban_card_field USING btree (field_id);


--
-- Name: theme_kanban_card_field_kanban_card_id_ac80ab91; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX theme_kanban_card_field_kanban_card_id_ac80ab91 ON public.theme_kanban_card_field USING btree (kanban_card_id);


--
-- Name: theme_kanban_card_theme_id_72798ebc; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX theme_kanban_card_theme_id_72798ebc ON public.theme_kanban_card USING btree (theme_id);


--
-- Name: theme_kanban_default_form_id_3011eded; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX theme_kanban_default_form_id_3011eded ON public.theme_kanban_default USING btree (form_id);


--
-- Name: theme_kanban_default_kanban_card_id_8b4bd403; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX theme_kanban_default_kanban_card_id_8b4bd403 ON public.theme_kanban_default USING btree (kanban_card_id);


--
-- Name: theme_kanban_default_kanban_dimension_id_89d625a7; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX theme_kanban_default_kanban_dimension_id_89d625a7 ON public.theme_kanban_default USING btree (kanban_dimension_id);


--
-- Name: theme_kanban_default_theme_id_ebc49039; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX theme_kanban_default_theme_id_ebc49039 ON public.theme_kanban_default USING btree (theme_id);


--
-- Name: theme_kanban_dimension_order_dimension_id_f88ad393; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX theme_kanban_dimension_order_dimension_id_f88ad393 ON public.theme_kanban_dimension_order USING btree (dimension_id);


--
-- Name: theme_kanban_dimension_order_theme_id_87c7ef72; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX theme_kanban_dimension_order_theme_id_87c7ef72 ON public.theme_kanban_dimension_order USING btree (theme_id);


--
-- Name: theme_notification_configu_notification_configuration_c198dfd1; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX theme_notification_configu_notification_configuration_c198dfd1 ON public.theme_notification_configuration_variable USING btree (notification_configuration_id);


--
-- Name: theme_notification_configuration_days_diff_3f22c879; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX theme_notification_configuration_days_diff_3f22c879 ON public.theme_notification_configuration USING btree (days_diff);


--
-- Name: theme_notification_configuration_days_diff_3f22c879_like; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX theme_notification_configuration_days_diff_3f22c879_like ON public.theme_notification_configuration USING btree (days_diff varchar_pattern_ops);


--
-- Name: theme_notification_configuration_field_id_bef76fb9; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX theme_notification_configuration_field_id_bef76fb9 ON public.theme_notification_configuration USING btree (field_id);


--
-- Name: theme_notification_configuration_form_id_54bf7476; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX theme_notification_configuration_form_id_54bf7476 ON public.theme_notification_configuration USING btree (form_id);


--
-- Name: theme_notification_configuration_variable_field_id_6ba0f96f; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX theme_notification_configuration_variable_field_id_6ba0f96f ON public.theme_notification_configuration_variable USING btree (field_id);


--
-- Name: theme_photos_theme_id_a48cfec5; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX theme_photos_theme_id_a48cfec5 ON public.theme_photos USING btree (theme_id);


--
-- Name: theme_user_id_cc7347f5; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX theme_user_id_cc7347f5 ON public.theme USING btree (user_id);


--
-- Name: user_accessed_by_field_id_b6445bc8; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX user_accessed_by_field_id_b6445bc8 ON public.user_accessed_by USING btree (field_id);


--
-- Name: user_accessed_by_user_id_27df8981; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX user_accessed_by_user_id_27df8981 ON public.user_accessed_by USING btree (user_id);


--
-- Name: user_accessed_by_user_option_id_6b9e5322; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX user_accessed_by_user_option_id_6b9e5322 ON public.user_accessed_by USING btree (user_option_id);


--
-- Name: users_company_id_23a5e9c4; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX users_company_id_23a5e9c4 ON public.users USING btree (company_id);


--
-- Name: users_data_type_id_2279beb4; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX users_data_type_id_2279beb4 ON public.users USING btree (data_type_id);


--
-- Name: users_groups_group_id_2f3517aa; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX users_groups_group_id_2f3517aa ON public.users_groups USING btree (group_id);


--
-- Name: users_groups_userextended_id_037e2530; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX users_groups_userextended_id_037e2530 ON public.users_groups USING btree (userextended_id);


--
-- Name: users_profile_id_d5052114; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX users_profile_id_d5052114 ON public.users USING btree (profile_id);


--
-- Name: users_user_permissions_permission_id_6d08dcd2; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX users_user_permissions_permission_id_6d08dcd2 ON public.users_user_permissions USING btree (permission_id);


--
-- Name: users_user_permissions_userextended_id_3a96f18f; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX users_user_permissions_userextended_id_3a96f18f ON public.users_user_permissions USING btree (userextended_id);


--
-- Name: users_username_e8658fc8_like; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX users_username_e8658fc8_like ON public.users USING btree (username varchar_pattern_ops);


--
-- Name: attachments attachments_field_id_55fdfd82_fk_field_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.attachments
    ADD CONSTRAINT attachments_field_id_55fdfd82_fk_field_id FOREIGN KEY (field_id) REFERENCES public.field(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: attachments attachments_form_id_5bdf972c_fk_dynamic_forms_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.attachments
    ADD CONSTRAINT attachments_form_id_5bdf972c_fk_dynamic_forms_id FOREIGN KEY (form_id) REFERENCES public.dynamic_forms(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: auth_group_permissions auth_group_permissio_permission_id_84c5c92e_fk_auth_perm; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.auth_group_permissions
    ADD CONSTRAINT auth_group_permissio_permission_id_84c5c92e_fk_auth_perm FOREIGN KEY (permission_id) REFERENCES public.auth_permission(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: auth_group_permissions auth_group_permissions_group_id_b120cbf9_fk_auth_group_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.auth_group_permissions
    ADD CONSTRAINT auth_group_permissions_group_id_b120cbf9_fk_auth_group_id FOREIGN KEY (group_id) REFERENCES public.auth_group(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: auth_permission auth_permission_content_type_id_2f476e4b_fk_django_co; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.auth_permission
    ADD CONSTRAINT auth_permission_content_type_id_2f476e4b_fk_django_co FOREIGN KEY (content_type_id) REFERENCES public.django_content_type(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: company_billing company_billing_charge_frequency_typ_650785d2_fk_charge_fr; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.company_billing
    ADD CONSTRAINT company_billing_charge_frequency_typ_650785d2_fk_charge_fr FOREIGN KEY (charge_frequency_type_id) REFERENCES public.charge_frequency_type(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: company_billing company_billing_company_id_41cfc942_fk_company_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.company_billing
    ADD CONSTRAINT company_billing_company_id_41cfc942_fk_company_id FOREIGN KEY (company_id) REFERENCES public.company(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: company_billing company_billing_invoice_date_type_id_c9c85363_fk_invoice_d; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.company_billing
    ADD CONSTRAINT company_billing_invoice_date_type_id_c9c85363_fk_invoice_d FOREIGN KEY (invoice_date_type_id) REFERENCES public.invoice_date_type(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: company_billing company_billing_payment_method_type__dcc0a133_fk_payment_m; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.company_billing
    ADD CONSTRAINT company_billing_payment_method_type__dcc0a133_fk_payment_m FOREIGN KEY (payment_method_type_id) REFERENCES public.payment_method_type(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: company_charge company_charge_company_id_feb35ee8_fk_company_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.company_charge
    ADD CONSTRAINT company_charge_company_id_feb35ee8_fk_company_id FOREIGN KEY (company_id) REFERENCES public.company(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: company company_company_type_id_49995cec_fk_company_type_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.company
    ADD CONSTRAINT company_company_type_id_49995cec_fk_company_type_id FOREIGN KEY (company_type_id) REFERENCES public.company_type(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: company_coupon company_coupon_company_id_74464616_fk_company_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.company_coupon
    ADD CONSTRAINT company_coupon_company_id_74464616_fk_company_id FOREIGN KEY (company_id) REFERENCES public.company(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: company_coupon company_coupon_discount_coupon_id_43a83526_fk_discount_; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.company_coupon
    ADD CONSTRAINT company_coupon_discount_coupon_id_43a83526_fk_discount_ FOREIGN KEY (discount_coupon_id) REFERENCES public.discount_coupon(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: company_invoice_mails company_invoice_mails_company_id_eefef680_fk_company_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.company_invoice_mails
    ADD CONSTRAINT company_invoice_mails_company_id_eefef680_fk_company_id FOREIGN KEY (company_id) REFERENCES public.company(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: company company_shared_by_id_9c427260_fk_company_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.company
    ADD CONSTRAINT company_shared_by_id_9c427260_fk_company_id FOREIGN KEY (shared_by_id) REFERENCES public.company(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: current_company_charge current_company_char_discount_by_individu_365faa60_fk_discount_; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.current_company_charge
    ADD CONSTRAINT current_company_char_discount_by_individu_365faa60_fk_discount_ FOREIGN KEY (discount_by_individual_value_id) REFERENCES public.discount_by_individual_value_quantity(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: current_company_charge current_company_char_individual_charge_va_cb192b02_fk_individua; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.current_company_charge
    ADD CONSTRAINT current_company_char_individual_charge_va_cb192b02_fk_individua FOREIGN KEY (individual_charge_value_type_id) REFERENCES public.individual_charge_value_type(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: current_company_charge current_company_charge_company_id_3161bb10_fk_company_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.current_company_charge
    ADD CONSTRAINT current_company_charge_company_id_3161bb10_fk_company_id FOREIGN KEY (company_id) REFERENCES public.company(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: dashboard_chart_configuration dashboard_chart_conf_aggregation_type_id_aeccf5b6_fk_aggregati; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.dashboard_chart_configuration
    ADD CONSTRAINT dashboard_chart_conf_aggregation_type_id_aeccf5b6_fk_aggregati FOREIGN KEY (aggregation_type_id) REFERENCES public.aggregation_type(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: dashboard_chart_configuration dashboard_chart_conf_chart_type_id_2f0767e6_fk_chart_typ; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.dashboard_chart_configuration
    ADD CONSTRAINT dashboard_chart_conf_chart_type_id_2f0767e6_fk_chart_typ FOREIGN KEY (chart_type_id) REFERENCES public.chart_type(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: dashboard_chart_configuration dashboard_chart_conf_label_field_id_71e9f8ce_fk_field_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.dashboard_chart_configuration
    ADD CONSTRAINT dashboard_chart_conf_label_field_id_71e9f8ce_fk_field_id FOREIGN KEY (label_field_id) REFERENCES public.field(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: dashboard_chart_configuration dashboard_chart_conf_number_format_type_i_2b3e5424_fk_field_num; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.dashboard_chart_configuration
    ADD CONSTRAINT dashboard_chart_conf_number_format_type_i_2b3e5424_fk_field_num FOREIGN KEY (number_format_type_id) REFERENCES public.field_number_format_type(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: dashboard_chart_configuration dashboard_chart_conf_value_field_id_ca43ce88_fk_field_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.dashboard_chart_configuration
    ADD CONSTRAINT dashboard_chart_conf_value_field_id_ca43ce88_fk_field_id FOREIGN KEY (value_field_id) REFERENCES public.field(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: dashboard_chart_configuration dashboard_chart_configuration_company_id_a0fa9a47_fk_company_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.dashboard_chart_configuration
    ADD CONSTRAINT dashboard_chart_configuration_company_id_a0fa9a47_fk_company_id FOREIGN KEY (company_id) REFERENCES public.company(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: dashboard_chart_configuration dashboard_chart_configuration_form_id_7ce5f68f_fk_form_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.dashboard_chart_configuration
    ADD CONSTRAINT dashboard_chart_configuration_form_id_7ce5f68f_fk_form_id FOREIGN KEY (form_id) REFERENCES public.form(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: dashboard_chart_configuration dashboard_chart_configuration_user_id_0da2430a_fk_users_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.dashboard_chart_configuration
    ADD CONSTRAINT dashboard_chart_configuration_user_id_0da2430a_fk_users_id FOREIGN KEY (user_id) REFERENCES public.users(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: default_field_value default_field_value_default_attachment_i_a912c819_fk_default_a; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.default_field_value
    ADD CONSTRAINT default_field_value_default_attachment_i_a912c819_fk_default_a FOREIGN KEY (default_attachment_id) REFERENCES public.default_attachments(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: default_field_value default_field_value_field_id_af9c4985_fk_field_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.default_field_value
    ADD CONSTRAINT default_field_value_field_id_af9c4985_fk_field_id FOREIGN KEY (field_id) REFERENCES public.field(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: discount_by_individual_name_for_company discount_by_individu_company_id_b64759fa_fk_company_i; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.discount_by_individual_name_for_company
    ADD CONSTRAINT discount_by_individu_company_id_b64759fa_fk_company_i FOREIGN KEY (company_id) REFERENCES public.company(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: discount_by_individual_value_quantity discount_by_individu_individual_charge_va_6081625a_fk_individua; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.discount_by_individual_value_quantity
    ADD CONSTRAINT discount_by_individu_individual_charge_va_6081625a_fk_individua FOREIGN KEY (individual_charge_value_type_id) REFERENCES public.individual_charge_value_type(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: discount_by_individual_name_for_company discount_by_individu_individual_charge_va_961f5cd9_fk_individua; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.discount_by_individual_name_for_company
    ADD CONSTRAINT discount_by_individu_individual_charge_va_961f5cd9_fk_individua FOREIGN KEY (individual_charge_value_type_id) REFERENCES public.individual_charge_value_type(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: django_admin_log django_admin_log_content_type_id_c4bce8eb_fk_django_co; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.django_admin_log
    ADD CONSTRAINT django_admin_log_content_type_id_c4bce8eb_fk_django_co FOREIGN KEY (content_type_id) REFERENCES public.django_content_type(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: django_admin_log django_admin_log_user_id_c564eba6_fk_users_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.django_admin_log
    ADD CONSTRAINT django_admin_log_user_id_c564eba6_fk_users_id FOREIGN KEY (user_id) REFERENCES public.users(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: draft draft_company_id_012e59c5_fk_company_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.draft
    ADD CONSTRAINT draft_company_id_012e59c5_fk_company_id FOREIGN KEY (company_id) REFERENCES public.company(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: draft draft_draft_type_id_0c28fdfb_fk_draft_type_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.draft
    ADD CONSTRAINT draft_draft_type_id_0c28fdfb_fk_draft_type_id FOREIGN KEY (draft_type_id) REFERENCES public.draft_type(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: draft draft_user_id_8443874d_fk_users_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.draft
    ADD CONSTRAINT draft_user_id_8443874d_fk_users_id FOREIGN KEY (user_id) REFERENCES public.users(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: dynamic_forms dynamic_forms_company_id_90ceb630_fk_company_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.dynamic_forms
    ADD CONSTRAINT dynamic_forms_company_id_90ceb630_fk_company_id FOREIGN KEY (company_id) REFERENCES public.company(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: dynamic_forms dynamic_forms_depends_on_id_afad9c4d_fk_dynamic_forms_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.dynamic_forms
    ADD CONSTRAINT dynamic_forms_depends_on_id_afad9c4d_fk_dynamic_forms_id FOREIGN KEY (depends_on_id) REFERENCES public.dynamic_forms(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: dynamic_forms dynamic_forms_form_id_9a55a4de_fk_form_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.dynamic_forms
    ADD CONSTRAINT dynamic_forms_form_id_9a55a4de_fk_form_id FOREIGN KEY (form_id) REFERENCES public.form(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: dynamic_forms dynamic_forms_user_id_ff8e8c6b_fk_users_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.dynamic_forms
    ADD CONSTRAINT dynamic_forms_user_id_ff8e8c6b_fk_users_id FOREIGN KEY (user_id) REFERENCES public.users(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: extract_file_data extract_file_data_company_id_95ab6e22_fk_company_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.extract_file_data
    ADD CONSTRAINT extract_file_data_company_id_95ab6e22_fk_company_id FOREIGN KEY (company_id) REFERENCES public.company(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: extract_file_data extract_file_data_form_id_309fe470_fk_form_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.extract_file_data
    ADD CONSTRAINT extract_file_data_form_id_309fe470_fk_form_id FOREIGN KEY (form_id) REFERENCES public.form(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: extract_file_data extract_file_data_user_id_55975de3_fk_users_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.extract_file_data
    ADD CONSTRAINT extract_file_data_user_id_55975de3_fk_users_id FOREIGN KEY (user_id) REFERENCES public.users(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: field field_date_configuration_d_ccea048c_fk_field_dat; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.field
    ADD CONSTRAINT field_date_configuration_d_ccea048c_fk_field_dat FOREIGN KEY (date_configuration_date_format_type_id) REFERENCES public.field_date_format_type(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: field field_form_field_as_option_id_790da294_fk_field_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.field
    ADD CONSTRAINT field_form_field_as_option_id_790da294_fk_field_id FOREIGN KEY (form_field_as_option_id) REFERENCES public.field(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: field field_form_id_f6498ce2_fk_form_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.field
    ADD CONSTRAINT field_form_id_f6498ce2_fk_form_id FOREIGN KEY (form_id) REFERENCES public.form(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: field field_number_configuration_fab9ea10_fk_field_num; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.field
    ADD CONSTRAINT field_number_configuration_fab9ea10_fk_field_num FOREIGN KEY (number_configuration_number_format_type_id) REFERENCES public.field_number_format_type(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: field_options field_options_field_id_6b8a308b_fk_field_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.field_options
    ADD CONSTRAINT field_options_field_id_6b8a308b_fk_field_id FOREIGN KEY (field_id) REFERENCES public.field(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: field field_period_configuration_4f8c8b02_fk_field_per; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.field
    ADD CONSTRAINT field_period_configuration_4f8c8b02_fk_field_per FOREIGN KEY (period_configuration_period_interval_type_id) REFERENCES public.field_period_interval_type(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: field field_type_id_381a7c0e_fk_field_type_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.field
    ADD CONSTRAINT field_type_id_381a7c0e_fk_field_type_id FOREIGN KEY (type_id) REFERENCES public.field_type(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: form_accessed_by form_accessed_by_form_id_58286c27_fk_form_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.form_accessed_by
    ADD CONSTRAINT form_accessed_by_form_id_58286c27_fk_form_id FOREIGN KEY (form_id) REFERENCES public.form(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: form_accessed_by form_accessed_by_user_id_d8d74f36_fk_users_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.form_accessed_by
    ADD CONSTRAINT form_accessed_by_user_id_d8d74f36_fk_users_id FOREIGN KEY (user_id) REFERENCES public.users(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: form form_company_id_7c58249b_fk_company_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.form
    ADD CONSTRAINT form_company_id_7c58249b_fk_company_id FOREIGN KEY (company_id) REFERENCES public.company(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: form form_conditional_on_field_id_23d83574_fk_field_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.form
    ADD CONSTRAINT form_conditional_on_field_id_23d83574_fk_field_id FOREIGN KEY (conditional_on_field_id) REFERENCES public.field(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: form form_conditional_type_id_9cf60a7e_fk_conditional_type_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.form
    ADD CONSTRAINT form_conditional_type_id_9cf60a7e_fk_conditional_type_id FOREIGN KEY (conditional_type_id) REFERENCES public.conditional_type(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: form form_depends_on_id_3e8981a6_fk_form_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.form
    ADD CONSTRAINT form_depends_on_id_3e8981a6_fk_form_id FOREIGN KEY (depends_on_id) REFERENCES public.form(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: form form_group_id_c3bfdf09_fk_group_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.form
    ADD CONSTRAINT form_group_id_c3bfdf09_fk_group_id FOREIGN KEY (group_id) REFERENCES public."group"(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: form form_type_id_11618d02_fk_form_type_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.form
    ADD CONSTRAINT form_type_id_11618d02_fk_form_type_id FOREIGN KEY (type_id) REFERENCES public.form_type(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: form_value form_value_company_id_a82640de_fk_company_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.form_value
    ADD CONSTRAINT form_value_company_id_a82640de_fk_company_id FOREIGN KEY (company_id) REFERENCES public.company(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: form_value form_value_date_configuration_d_44da5d52_fk_field_dat; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.form_value
    ADD CONSTRAINT form_value_date_configuration_d_44da5d52_fk_field_dat FOREIGN KEY (date_configuration_date_format_type_id) REFERENCES public.field_date_format_type(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: form_value form_value_field_id_9fa432fe_fk_field_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.form_value
    ADD CONSTRAINT form_value_field_id_9fa432fe_fk_field_id FOREIGN KEY (field_id) REFERENCES public.field(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: form_value form_value_field_type_id_6f20e5ea_fk_field_type_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.form_value
    ADD CONSTRAINT form_value_field_type_id_6f20e5ea_fk_field_type_id FOREIGN KEY (field_type_id) REFERENCES public.field_type(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: form_value form_value_form_field_as_option_id_b768e543_fk_field_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.form_value
    ADD CONSTRAINT form_value_form_field_as_option_id_b768e543_fk_field_id FOREIGN KEY (form_field_as_option_id) REFERENCES public.field(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: form_value form_value_form_id_c08e4676_fk_dynamic_forms_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.form_value
    ADD CONSTRAINT form_value_form_id_c08e4676_fk_dynamic_forms_id FOREIGN KEY (form_id) REFERENCES public.dynamic_forms(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: form_value form_value_number_configuration_a91154d8_fk_field_num; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.form_value
    ADD CONSTRAINT form_value_number_configuration_a91154d8_fk_field_num FOREIGN KEY (number_configuration_number_format_type_id) REFERENCES public.field_number_format_type(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: form_value form_value_period_configuration_2f38b2dd_fk_field_per; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.form_value
    ADD CONSTRAINT form_value_period_configuration_2f38b2dd_fk_field_per FOREIGN KEY (period_configuration_period_interval_type_id) REFERENCES public.field_period_interval_type(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: formula_context_attribute_type formula_context_attr_attribute_type_id_0d76f692_fk_formula_a; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.formula_context_attribute_type
    ADD CONSTRAINT formula_context_attr_attribute_type_id_0d76f692_fk_formula_a FOREIGN KEY (attribute_type_id) REFERENCES public.formula_attribute_type(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: formula_context_attribute_type formula_context_attr_context_type_id_fe8c0a50_fk_formula_c; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.formula_context_attribute_type
    ADD CONSTRAINT formula_context_attr_context_type_id_fe8c0a50_fk_formula_c FOREIGN KEY (context_type_id) REFERENCES public.formula_context_type(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: formula_context_for_company formula_context_for__context_type_id_702ab3dc_fk_formula_c; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.formula_context_for_company
    ADD CONSTRAINT formula_context_for__context_type_id_702ab3dc_fk_formula_c FOREIGN KEY (context_type_id) REFERENCES public.formula_context_type(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: formula_context_for_company formula_context_for_company_company_id_85894e11_fk_company_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.formula_context_for_company
    ADD CONSTRAINT formula_context_for_company_company_id_85894e11_fk_company_id FOREIGN KEY (company_id) REFERENCES public.company(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: formula_parameters_type formula_parameters_t_raw_data_type_id_c92e728a_fk_raw_data_; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.formula_parameters_type
    ADD CONSTRAINT formula_parameters_t_raw_data_type_id_c92e728a_fk_raw_data_ FOREIGN KEY (raw_data_type_id) REFERENCES public.raw_data_type(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: formula_variable formula_variable_field_id_1e593a29_fk_field_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.formula_variable
    ADD CONSTRAINT formula_variable_field_id_1e593a29_fk_field_id FOREIGN KEY (field_id) REFERENCES public.field(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: formula_variable formula_variable_variable_id_01badc58_fk_field_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.formula_variable
    ADD CONSTRAINT formula_variable_variable_id_01badc58_fk_field_id FOREIGN KEY (variable_id) REFERENCES public.field(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: group group_company_id_2f2f8544_fk_company_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."group"
    ADD CONSTRAINT group_company_id_2f2f8544_fk_company_id FOREIGN KEY (company_id) REFERENCES public.company(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: individual_charge_value_type individual_charge_va_charge_frequency_typ_327bdc4b_fk_charge_fr; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.individual_charge_value_type
    ADD CONSTRAINT individual_charge_va_charge_frequency_typ_327bdc4b_fk_charge_fr FOREIGN KEY (charge_frequency_type_id) REFERENCES public.charge_frequency_type(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: individual_charge_value_type individual_charge_va_charge_type_id_5a999b80_fk_charge_ty; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.individual_charge_value_type
    ADD CONSTRAINT individual_charge_va_charge_type_id_5a999b80_fk_charge_ty FOREIGN KEY (charge_type_id) REFERENCES public.charge_type(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: kanban_card kanban_card_company_id_04a5dc79_fk_company_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.kanban_card
    ADD CONSTRAINT kanban_card_company_id_04a5dc79_fk_company_id FOREIGN KEY (company_id) REFERENCES public.company(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: kanban_card_field kanban_card_field_field_id_ef99ecd8_fk_field_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.kanban_card_field
    ADD CONSTRAINT kanban_card_field_field_id_ef99ecd8_fk_field_id FOREIGN KEY (field_id) REFERENCES public.field(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: kanban_card_field kanban_card_field_kanban_card_id_ee60c842_fk_kanban_card_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.kanban_card_field
    ADD CONSTRAINT kanban_card_field_kanban_card_id_ee60c842_fk_kanban_card_id FOREIGN KEY (kanban_card_id) REFERENCES public.kanban_card(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: kanban_card kanban_card_form_id_7ef5ffcb_fk_form_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.kanban_card
    ADD CONSTRAINT kanban_card_form_id_7ef5ffcb_fk_form_id FOREIGN KEY (form_id) REFERENCES public.form(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: kanban_card kanban_card_user_id_080c1fad_fk_users_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.kanban_card
    ADD CONSTRAINT kanban_card_user_id_080c1fad_fk_users_id FOREIGN KEY (user_id) REFERENCES public.users(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: kanban_collapsed_option kanban_collapsed_opt_field_option_id_74f3fd44_fk_field_opt; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.kanban_collapsed_option
    ADD CONSTRAINT kanban_collapsed_opt_field_option_id_74f3fd44_fk_field_opt FOREIGN KEY (field_option_id) REFERENCES public.field_options(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: kanban_collapsed_option kanban_collapsed_option_company_id_315c2003_fk_company_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.kanban_collapsed_option
    ADD CONSTRAINT kanban_collapsed_option_company_id_315c2003_fk_company_id FOREIGN KEY (company_id) REFERENCES public.company(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: kanban_collapsed_option kanban_collapsed_option_user_id_a9512aa8_fk_users_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.kanban_collapsed_option
    ADD CONSTRAINT kanban_collapsed_option_user_id_a9512aa8_fk_users_id FOREIGN KEY (user_id) REFERENCES public.users(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: kanban_default kanban_default_company_id_5180899b_fk_company_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.kanban_default
    ADD CONSTRAINT kanban_default_company_id_5180899b_fk_company_id FOREIGN KEY (company_id) REFERENCES public.company(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: kanban_default kanban_default_form_id_cee65b7a_fk_form_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.kanban_default
    ADD CONSTRAINT kanban_default_form_id_cee65b7a_fk_form_id FOREIGN KEY (form_id) REFERENCES public.form(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: kanban_default kanban_default_kanban_card_id_bb2c6660_fk_kanban_card_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.kanban_default
    ADD CONSTRAINT kanban_default_kanban_card_id_bb2c6660_fk_kanban_card_id FOREIGN KEY (kanban_card_id) REFERENCES public.kanban_card(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: kanban_default kanban_default_kanban_dimension_id_292c6e3f_fk_field_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.kanban_default
    ADD CONSTRAINT kanban_default_kanban_dimension_id_292c6e3f_fk_field_id FOREIGN KEY (kanban_dimension_id) REFERENCES public.field(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: kanban_default kanban_default_user_id_7e7d4ea4_fk_users_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.kanban_default
    ADD CONSTRAINT kanban_default_user_id_7e7d4ea4_fk_users_id FOREIGN KEY (user_id) REFERENCES public.users(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: kanban_dimension_order kanban_dimension_order_dimension_id_811c5433_fk_field_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.kanban_dimension_order
    ADD CONSTRAINT kanban_dimension_order_dimension_id_811c5433_fk_field_id FOREIGN KEY (dimension_id) REFERENCES public.field(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: kanban_dimension_order kanban_dimension_order_user_id_24a5dcc4_fk_users_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.kanban_dimension_order
    ADD CONSTRAINT kanban_dimension_order_user_id_24a5dcc4_fk_users_id FOREIGN KEY (user_id) REFERENCES public.users(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: listing_selected_fields listing_selected_fields_user_id_8b799c65_fk_users_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.listing_selected_fields
    ADD CONSTRAINT listing_selected_fields_user_id_8b799c65_fk_users_id FOREIGN KEY (user_id) REFERENCES public.users(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: notification_configuration_variable notification_configu_notification_configu_b14b5183_fk_notificat; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.notification_configuration_variable
    ADD CONSTRAINT notification_configu_notification_configu_b14b5183_fk_notificat FOREIGN KEY (notification_configuration_id) REFERENCES public.notification_configuration(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: notification_configuration notification_configuration_user_id_439ec0f7_fk_users_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.notification_configuration
    ADD CONSTRAINT notification_configuration_user_id_439ec0f7_fk_users_id FOREIGN KEY (user_id) REFERENCES public.users(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: notification notification_form_id_6c692edb_fk_dynamic_forms_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.notification
    ADD CONSTRAINT notification_form_id_6c692edb_fk_dynamic_forms_id FOREIGN KEY (form_id) REFERENCES public.dynamic_forms(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: notification notification_notification_configu_b91fecd8_fk_notificat; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.notification
    ADD CONSTRAINT notification_notification_configu_b91fecd8_fk_notificat FOREIGN KEY (notification_configuration_id) REFERENCES public.notification_configuration(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: notification notification_user_id_1002fc38_fk_users_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.notification
    ADD CONSTRAINT notification_user_id_1002fc38_fk_users_id FOREIGN KEY (user_id) REFERENCES public.users(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: option_accessed_by option_accessed_by_field_option_id_eecb860e_fk_field_options_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.option_accessed_by
    ADD CONSTRAINT option_accessed_by_field_option_id_eecb860e_fk_field_options_id FOREIGN KEY (field_option_id) REFERENCES public.field_options(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: option_accessed_by option_accessed_by_user_id_ce4ac9c6_fk_users_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.option_accessed_by
    ADD CONSTRAINT option_accessed_by_user_id_ce4ac9c6_fk_users_id FOREIGN KEY (user_id) REFERENCES public.users(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: partner_default_and_discounts partner_default_and__individual_charge_va_aeb75e21_fk_individua; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.partner_default_and_discounts
    ADD CONSTRAINT partner_default_and__individual_charge_va_aeb75e21_fk_individua FOREIGN KEY (individual_charge_value_type_id) REFERENCES public.individual_charge_value_type(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: pdf_generated pdf_generated_company_id_3c1c32c2_fk_company_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.pdf_generated
    ADD CONSTRAINT pdf_generated_company_id_3c1c32c2_fk_company_id FOREIGN KEY (company_id) REFERENCES public.company(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: pdf_generated pdf_generated_pdf_template_id_c6d92617_fk_pdf_templ; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.pdf_generated
    ADD CONSTRAINT pdf_generated_pdf_template_id_c6d92617_fk_pdf_templ FOREIGN KEY (pdf_template_id) REFERENCES public.pdf_template_configuration(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: pdf_generated pdf_generated_user_id_048f0892_fk_users_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.pdf_generated
    ADD CONSTRAINT pdf_generated_user_id_048f0892_fk_users_id FOREIGN KEY (user_id) REFERENCES public.users(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: pdf_template_allowed_text_block pdf_template_allowed_block_id_5a06c389_fk_text_bloc; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.pdf_template_allowed_text_block
    ADD CONSTRAINT pdf_template_allowed_block_id_5a06c389_fk_text_bloc FOREIGN KEY (block_id) REFERENCES public.text_block_type(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: pdf_template_configuration_variables pdf_template_configu_pdf_template_id_db06b600_fk_pdf_templ; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.pdf_template_configuration_variables
    ADD CONSTRAINT pdf_template_configu_pdf_template_id_db06b600_fk_pdf_templ FOREIGN KEY (pdf_template_id) REFERENCES public.pdf_template_configuration(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: pdf_template_configuration pdf_template_configu_rich_text_page_id_b21498de_fk_text_page; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.pdf_template_configuration
    ADD CONSTRAINT pdf_template_configu_rich_text_page_id_b21498de_fk_text_page FOREIGN KEY (rich_text_page_id) REFERENCES public.text_page(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: pdf_template_configuration pdf_template_configuration_company_id_31b02fed_fk_company_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.pdf_template_configuration
    ADD CONSTRAINT pdf_template_configuration_company_id_31b02fed_fk_company_id FOREIGN KEY (company_id) REFERENCES public.company(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: pdf_template_configuration pdf_template_configuration_user_id_c8eba5ed_fk_users_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.pdf_template_configuration
    ADD CONSTRAINT pdf_template_configuration_user_id_c8eba5ed_fk_users_id FOREIGN KEY (user_id) REFERENCES public.users(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: pre_notification pre_notification_dynamic_form_id_913c4ad7_fk_dynamic_forms_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.pre_notification
    ADD CONSTRAINT pre_notification_dynamic_form_id_913c4ad7_fk_dynamic_forms_id FOREIGN KEY (dynamic_form_id) REFERENCES public.dynamic_forms(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: pre_notification pre_notification_notification_configu_d65be96c_fk_notificat; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.pre_notification
    ADD CONSTRAINT pre_notification_notification_configu_d65be96c_fk_notificat FOREIGN KEY (notification_configuration_id) REFERENCES public.notification_configuration(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: pre_notification pre_notification_user_id_5b8b68ac_fk_users_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.pre_notification
    ADD CONSTRAINT pre_notification_user_id_5b8b68ac_fk_users_id FOREIGN KEY (user_id) REFERENCES public.users(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: public_access public_access_company_id_5ee02e79_fk_company_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.public_access
    ADD CONSTRAINT public_access_company_id_5ee02e79_fk_company_id FOREIGN KEY (company_id) REFERENCES public.company(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: public_access_field public_access_field_public_form_id_aa006be5_fk_public_ac; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.public_access_field
    ADD CONSTRAINT public_access_field_public_form_id_aa006be5_fk_public_ac FOREIGN KEY (public_form_id) REFERENCES public.public_access_form(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: public_access public_access_user_id_f787e0ea_fk_users_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.public_access
    ADD CONSTRAINT public_access_user_id_f787e0ea_fk_users_id FOREIGN KEY (user_id) REFERENCES public.users(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: public_access_field public_field_field_id_39b2ce4b_fk_field_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.public_access_field
    ADD CONSTRAINT public_field_field_id_39b2ce4b_fk_field_id FOREIGN KEY (field_id) REFERENCES public.field(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: public_access_field public_field_public_access_id_e842b051_fk_public_access_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.public_access_field
    ADD CONSTRAINT public_field_public_access_id_e842b051_fk_public_access_id FOREIGN KEY (public_access_id) REFERENCES public.public_access(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: public_access_form public_form_form_id_a176af65_fk_form_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.public_access_form
    ADD CONSTRAINT public_form_form_id_a176af65_fk_form_id FOREIGN KEY (form_id) REFERENCES public.form(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: public_access_form public_form_public_access_id_5d292c70_fk_public_access_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.public_access_form
    ADD CONSTRAINT public_form_public_access_id_5d292c70_fk_public_access_id FOREIGN KEY (public_access_id) REFERENCES public.public_access(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: push_notification push_notification_push_notification_ta_e42bfbc0_fk_push_noti; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.push_notification
    ADD CONSTRAINT push_notification_push_notification_ta_e42bfbc0_fk_push_noti FOREIGN KEY (push_notification_tag_type_id) REFERENCES public.push_notification_tag_type(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: push_notification push_notification_user_id_3ed35132_fk_users_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.push_notification
    ADD CONSTRAINT push_notification_user_id_3ed35132_fk_users_id FOREIGN KEY (user_id) REFERENCES public.users(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: user_notification read_notification_notification_id_e4e1de6d_fk_notification_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.user_notification
    ADD CONSTRAINT read_notification_notification_id_e4e1de6d_fk_notification_id FOREIGN KEY (notification_id) REFERENCES public.notification(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: user_notification read_notification_user_id_fc1a8b5b_fk_users_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.user_notification
    ADD CONSTRAINT read_notification_user_id_fc1a8b5b_fk_users_id FOREIGN KEY (user_id) REFERENCES public.users(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: text_block text_block_block_type_id_456e6e02_fk_text_block_type_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.text_block
    ADD CONSTRAINT text_block_block_type_id_456e6e02_fk_text_block_type_id FOREIGN KEY (block_type_id) REFERENCES public.text_block_type(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: text_block text_block_depends_on_id_d159e181_fk_text_block_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.text_block
    ADD CONSTRAINT text_block_depends_on_id_d159e181_fk_text_block_id FOREIGN KEY (depends_on_id) REFERENCES public.text_block(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: text_block text_block_image_option_id_7564dcd9_fk_text_image_option_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.text_block
    ADD CONSTRAINT text_block_image_option_id_7564dcd9_fk_text_image_option_id FOREIGN KEY (image_option_id) REFERENCES public.text_image_option(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: text_block text_block_list_option_id_12b54060_fk_text_list_option_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.text_block
    ADD CONSTRAINT text_block_list_option_id_12b54060_fk_text_list_option_id FOREIGN KEY (list_option_id) REFERENCES public.text_list_option(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: text_block text_block_page_id_754b5d95_fk_text_page_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.text_block
    ADD CONSTRAINT text_block_page_id_754b5d95_fk_text_page_id FOREIGN KEY (page_id) REFERENCES public.text_page(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: text_block text_block_table_option_id_e54921bf_fk_text_table_option_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.text_block
    ADD CONSTRAINT text_block_table_option_id_e54921bf_fk_text_table_option_id FOREIGN KEY (table_option_id) REFERENCES public.text_table_option(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: text_block text_block_text_option_id_e0386baa_fk_text_text_option_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.text_block
    ADD CONSTRAINT text_block_text_option_id_e0386baa_fk_text_text_option_id FOREIGN KEY (text_option_id) REFERENCES public.text_text_option(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: text_block_type_can_contain_type text_block_type_can__block_id_6883c6c0_fk_text_bloc; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.text_block_type_can_contain_type
    ADD CONSTRAINT text_block_type_can__block_id_6883c6c0_fk_text_bloc FOREIGN KEY (block_id) REFERENCES public.text_block_type(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: text_block_type_can_contain_type text_block_type_can__contain_id_407b77b2_fk_text_bloc; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.text_block_type_can_contain_type
    ADD CONSTRAINT text_block_type_can__contain_id_407b77b2_fk_text_bloc FOREIGN KEY (contain_id) REFERENCES public.text_block_type(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: text_content text_content_block_id_fcf310b6_fk_text_block_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.text_content
    ADD CONSTRAINT text_content_block_id_fcf310b6_fk_text_block_id FOREIGN KEY (block_id) REFERENCES public.text_block(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: text_list_option text_list_option_list_type_id_6594d736_fk_text_list_type_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.text_list_option
    ADD CONSTRAINT text_list_option_list_type_id_6594d736_fk_text_list_type_id FOREIGN KEY (list_type_id) REFERENCES public.text_list_type(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: text_page text_page_company_id_29e50b4e_fk_company_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.text_page
    ADD CONSTRAINT text_page_company_id_29e50b4e_fk_company_id FOREIGN KEY (company_id) REFERENCES public.company(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: text_page text_page_user_id_c020e567_fk_users_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.text_page
    ADD CONSTRAINT text_page_user_id_c020e567_fk_users_id FOREIGN KEY (user_id) REFERENCES public.users(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: text_table_option_column_dimension text_table_option_co_text_table_option_id_162822d8_fk_text_tabl; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.text_table_option_column_dimension
    ADD CONSTRAINT text_table_option_co_text_table_option_id_162822d8_fk_text_tabl FOREIGN KEY (text_table_option_id) REFERENCES public.text_table_option(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: text_table_option_row_dimension text_table_option_ro_text_table_option_id_530f5664_fk_text_tabl; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.text_table_option_row_dimension
    ADD CONSTRAINT text_table_option_ro_text_table_option_id_530f5664_fk_text_tabl FOREIGN KEY (text_table_option_id) REFERENCES public.text_table_option(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: text_text_option text_text_option_alignment_type_id_743cafc3_fk_text_alig; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.text_text_option
    ADD CONSTRAINT text_text_option_alignment_type_id_743cafc3_fk_text_alig FOREIGN KEY (alignment_type_id) REFERENCES public.text_alignment_type(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: theme theme_company_id_f4947892_fk_company_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.theme
    ADD CONSTRAINT theme_company_id_f4947892_fk_company_id FOREIGN KEY (company_id) REFERENCES public.company(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: theme_dashboard_chart_configuration theme_dashboard_char_aggregation_type_id_5b260d82_fk_aggregati; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.theme_dashboard_chart_configuration
    ADD CONSTRAINT theme_dashboard_char_aggregation_type_id_5b260d82_fk_aggregati FOREIGN KEY (aggregation_type_id) REFERENCES public.aggregation_type(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: theme_dashboard_chart_configuration theme_dashboard_char_chart_type_id_0bd7cd7c_fk_chart_typ; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.theme_dashboard_chart_configuration
    ADD CONSTRAINT theme_dashboard_char_chart_type_id_0bd7cd7c_fk_chart_typ FOREIGN KEY (chart_type_id) REFERENCES public.chart_type(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: theme_dashboard_chart_configuration theme_dashboard_char_form_id_028f6eaf_fk_theme_for; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.theme_dashboard_chart_configuration
    ADD CONSTRAINT theme_dashboard_char_form_id_028f6eaf_fk_theme_for FOREIGN KEY (form_id) REFERENCES public.theme_form(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: theme_dashboard_chart_configuration theme_dashboard_char_label_field_id_b9b8dc8e_fk_theme_fie; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.theme_dashboard_chart_configuration
    ADD CONSTRAINT theme_dashboard_char_label_field_id_b9b8dc8e_fk_theme_fie FOREIGN KEY (label_field_id) REFERENCES public.theme_field(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: theme_dashboard_chart_configuration theme_dashboard_char_number_format_type_i_6d099b38_fk_field_num; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.theme_dashboard_chart_configuration
    ADD CONSTRAINT theme_dashboard_char_number_format_type_i_6d099b38_fk_field_num FOREIGN KEY (number_format_type_id) REFERENCES public.field_number_format_type(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: theme_dashboard_chart_configuration theme_dashboard_char_theme_id_47624a66_fk_theme_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.theme_dashboard_chart_configuration
    ADD CONSTRAINT theme_dashboard_char_theme_id_47624a66_fk_theme_id FOREIGN KEY (theme_id) REFERENCES public.theme(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: theme_dashboard_chart_configuration theme_dashboard_char_value_field_id_2fdc2fac_fk_theme_fie; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.theme_dashboard_chart_configuration
    ADD CONSTRAINT theme_dashboard_char_value_field_id_2fdc2fac_fk_theme_fie FOREIGN KEY (value_field_id) REFERENCES public.theme_field(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: theme_field theme_field_date_configuration_d_1ccb4d8f_fk_field_dat; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.theme_field
    ADD CONSTRAINT theme_field_date_configuration_d_1ccb4d8f_fk_field_dat FOREIGN KEY (date_configuration_date_format_type_id) REFERENCES public.field_date_format_type(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: theme_field theme_field_form_field_as_option_id_8fd62607_fk_theme_field_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.theme_field
    ADD CONSTRAINT theme_field_form_field_as_option_id_8fd62607_fk_theme_field_id FOREIGN KEY (form_field_as_option_id) REFERENCES public.theme_field(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: theme_field theme_field_form_id_1989d247_fk_theme_form_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.theme_field
    ADD CONSTRAINT theme_field_form_id_1989d247_fk_theme_form_id FOREIGN KEY (form_id) REFERENCES public.theme_form(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: theme_field theme_field_number_configuration_a1ccb8a5_fk_field_num; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.theme_field
    ADD CONSTRAINT theme_field_number_configuration_a1ccb8a5_fk_field_num FOREIGN KEY (number_configuration_number_format_type_id) REFERENCES public.field_number_format_type(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: theme_field_options theme_field_options_field_id_f05e2744_fk_theme_field_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.theme_field_options
    ADD CONSTRAINT theme_field_options_field_id_f05e2744_fk_theme_field_id FOREIGN KEY (field_id) REFERENCES public.theme_field(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: theme_field theme_field_period_configuration_30743340_fk_field_per; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.theme_field
    ADD CONSTRAINT theme_field_period_configuration_30743340_fk_field_per FOREIGN KEY (period_configuration_period_interval_type_id) REFERENCES public.field_period_interval_type(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: theme_field theme_field_type_id_e61914b1_fk_field_type_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.theme_field
    ADD CONSTRAINT theme_field_type_id_e61914b1_fk_field_type_id FOREIGN KEY (type_id) REFERENCES public.field_type(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: theme_form theme_form_conditional_on_field_id_e50652f8_fk_theme_field_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.theme_form
    ADD CONSTRAINT theme_form_conditional_on_field_id_e50652f8_fk_theme_field_id FOREIGN KEY (conditional_on_field_id) REFERENCES public.theme_field(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: theme_form theme_form_conditional_type_id_208792dd_fk_conditional_type_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.theme_form
    ADD CONSTRAINT theme_form_conditional_type_id_208792dd_fk_conditional_type_id FOREIGN KEY (conditional_type_id) REFERENCES public.conditional_type(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: theme_form theme_form_depends_on_id_a15f89bc_fk_theme_form_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.theme_form
    ADD CONSTRAINT theme_form_depends_on_id_a15f89bc_fk_theme_form_id FOREIGN KEY (depends_on_id) REFERENCES public.theme_form(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: theme_form theme_form_theme_id_3fc4fb3f_fk_theme_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.theme_form
    ADD CONSTRAINT theme_form_theme_id_3fc4fb3f_fk_theme_id FOREIGN KEY (theme_id) REFERENCES public.theme(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: theme_form theme_form_type_id_4bac8752_fk_form_type_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.theme_form
    ADD CONSTRAINT theme_form_type_id_4bac8752_fk_form_type_id FOREIGN KEY (type_id) REFERENCES public.form_type(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: theme_formula_variable theme_formula_variable_field_id_7bb08f75_fk_theme_field_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.theme_formula_variable
    ADD CONSTRAINT theme_formula_variable_field_id_7bb08f75_fk_theme_field_id FOREIGN KEY (field_id) REFERENCES public.theme_field(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: theme_formula_variable theme_formula_variable_variable_id_c787db1f_fk_theme_field_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.theme_formula_variable
    ADD CONSTRAINT theme_formula_variable_variable_id_c787db1f_fk_theme_field_id FOREIGN KEY (variable_id) REFERENCES public.theme_field(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: theme_kanban_card_field theme_kanban_card_fi_kanban_card_id_ac80ab91_fk_theme_kan; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.theme_kanban_card_field
    ADD CONSTRAINT theme_kanban_card_fi_kanban_card_id_ac80ab91_fk_theme_kan FOREIGN KEY (kanban_card_id) REFERENCES public.theme_kanban_card(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: theme_kanban_card_field theme_kanban_card_field_field_id_b38ea031_fk_theme_field_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.theme_kanban_card_field
    ADD CONSTRAINT theme_kanban_card_field_field_id_b38ea031_fk_theme_field_id FOREIGN KEY (field_id) REFERENCES public.theme_field(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: theme_kanban_card theme_kanban_card_theme_id_72798ebc_fk_theme_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.theme_kanban_card
    ADD CONSTRAINT theme_kanban_card_theme_id_72798ebc_fk_theme_id FOREIGN KEY (theme_id) REFERENCES public.theme(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: theme_kanban_default theme_kanban_default_form_id_3011eded_fk_theme_form_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.theme_kanban_default
    ADD CONSTRAINT theme_kanban_default_form_id_3011eded_fk_theme_form_id FOREIGN KEY (form_id) REFERENCES public.theme_form(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: theme_kanban_default theme_kanban_default_kanban_card_id_8b4bd403_fk_theme_kan; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.theme_kanban_default
    ADD CONSTRAINT theme_kanban_default_kanban_card_id_8b4bd403_fk_theme_kan FOREIGN KEY (kanban_card_id) REFERENCES public.theme_kanban_card(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: theme_kanban_default theme_kanban_default_kanban_dimension_id_89d625a7_fk_theme_fie; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.theme_kanban_default
    ADD CONSTRAINT theme_kanban_default_kanban_dimension_id_89d625a7_fk_theme_fie FOREIGN KEY (kanban_dimension_id) REFERENCES public.theme_field(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: theme_kanban_default theme_kanban_default_theme_id_ebc49039_fk_theme_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.theme_kanban_default
    ADD CONSTRAINT theme_kanban_default_theme_id_ebc49039_fk_theme_id FOREIGN KEY (theme_id) REFERENCES public.theme(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: theme_kanban_dimension_order theme_kanban_dimensi_dimension_id_f88ad393_fk_theme_fie; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.theme_kanban_dimension_order
    ADD CONSTRAINT theme_kanban_dimensi_dimension_id_f88ad393_fk_theme_fie FOREIGN KEY (dimension_id) REFERENCES public.theme_field(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: theme_kanban_dimension_order theme_kanban_dimension_order_theme_id_87c7ef72_fk_theme_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.theme_kanban_dimension_order
    ADD CONSTRAINT theme_kanban_dimension_order_theme_id_87c7ef72_fk_theme_id FOREIGN KEY (theme_id) REFERENCES public.theme(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: theme_notification_configuration_variable theme_notification_c_field_id_6ba0f96f_fk_theme_fie; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.theme_notification_configuration_variable
    ADD CONSTRAINT theme_notification_c_field_id_6ba0f96f_fk_theme_fie FOREIGN KEY (field_id) REFERENCES public.theme_field(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: theme_notification_configuration theme_notification_c_field_id_bef76fb9_fk_theme_fie; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.theme_notification_configuration
    ADD CONSTRAINT theme_notification_c_field_id_bef76fb9_fk_theme_fie FOREIGN KEY (field_id) REFERENCES public.theme_field(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: theme_notification_configuration theme_notification_c_form_id_54bf7476_fk_theme_for; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.theme_notification_configuration
    ADD CONSTRAINT theme_notification_c_form_id_54bf7476_fk_theme_for FOREIGN KEY (form_id) REFERENCES public.theme_form(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: theme_notification_configuration_variable theme_notification_c_notification_configu_c198dfd1_fk_theme_not; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.theme_notification_configuration_variable
    ADD CONSTRAINT theme_notification_c_notification_configu_c198dfd1_fk_theme_not FOREIGN KEY (notification_configuration_id) REFERENCES public.theme_notification_configuration(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: theme_photos theme_photos_theme_id_a48cfec5_fk_theme_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.theme_photos
    ADD CONSTRAINT theme_photos_theme_id_a48cfec5_fk_theme_id FOREIGN KEY (theme_id) REFERENCES public.theme(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: theme theme_user_id_cc7347f5_fk_users_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.theme
    ADD CONSTRAINT theme_user_id_cc7347f5_fk_users_id FOREIGN KEY (user_id) REFERENCES public.users(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: user_accessed_by user_accessed_by_field_id_b6445bc8_fk_field_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.user_accessed_by
    ADD CONSTRAINT user_accessed_by_field_id_b6445bc8_fk_field_id FOREIGN KEY (field_id) REFERENCES public.field(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: user_accessed_by user_accessed_by_user_id_27df8981_fk_users_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.user_accessed_by
    ADD CONSTRAINT user_accessed_by_user_id_27df8981_fk_users_id FOREIGN KEY (user_id) REFERENCES public.users(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: user_accessed_by user_accessed_by_user_option_id_6b9e5322_fk_users_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.user_accessed_by
    ADD CONSTRAINT user_accessed_by_user_option_id_6b9e5322_fk_users_id FOREIGN KEY (user_option_id) REFERENCES public.users(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: users users_company_id_23a5e9c4_fk_company_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_company_id_23a5e9c4_fk_company_id FOREIGN KEY (company_id) REFERENCES public.company(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: users users_data_type_id_2279beb4_fk_data_type_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_data_type_id_2279beb4_fk_data_type_id FOREIGN KEY (data_type_id) REFERENCES public.data_type(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: users_groups users_groups_group_id_2f3517aa_fk_auth_group_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.users_groups
    ADD CONSTRAINT users_groups_group_id_2f3517aa_fk_auth_group_id FOREIGN KEY (group_id) REFERENCES public.auth_group(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: users_groups users_groups_userextended_id_037e2530_fk_users_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.users_groups
    ADD CONSTRAINT users_groups_userextended_id_037e2530_fk_users_id FOREIGN KEY (userextended_id) REFERENCES public.users(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: users users_profile_id_d5052114_fk_profiles_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_profile_id_d5052114_fk_profiles_id FOREIGN KEY (profile_id) REFERENCES public.profiles(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: users_user_permissions users_user_permissio_permission_id_6d08dcd2_fk_auth_perm; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.users_user_permissions
    ADD CONSTRAINT users_user_permissio_permission_id_6d08dcd2_fk_auth_perm FOREIGN KEY (permission_id) REFERENCES public.auth_permission(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: users_user_permissions users_user_permissions_userextended_id_3a96f18f_fk_users_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.users_user_permissions
    ADD CONSTRAINT users_user_permissions_userextended_id_3a96f18f_fk_users_id FOREIGN KEY (userextended_id) REFERENCES public.users(id) DEFERRABLE INITIALLY DEFERRED;


--
-- PostgreSQL database dump complete
--

