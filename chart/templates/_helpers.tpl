{{/* vim: set filetype=mustache: */}}
{{/*
Expand the name of the chart.
*/}}
{{- define "django.name" -}}
{{- default .Chart.Name .Values.nameOverride | trunc 63 | trimSuffix "-" -}}
{{- end -}}

{{/*
Create a default fully qualified app name.
We truncate at 63 chars because some Kubernetes name fields are limited to this (by the DNS naming spec).
If release name contains chart name it will be used as a full name.
*/}}
{{- define "django.fullname" -}}
{{- if .Values.fullnameOverride -}}
{{- .Values.fullnameOverride | trunc 63 | trimSuffix "-" -}}
{{- else -}}
{{- $name := default .Chart.Name .Values.nameOverride -}}
{{- if contains $name .Release.Name -}}
{{- .Release.Name | trunc 63 | trimSuffix "-" -}}
{{- else -}}
{{- printf "%s-%s" .Release.Name $name | trunc 63 | trimSuffix "-" -}}
{{- end -}}
{{- end -}}
{{- end -}}

{{/*
Create chart name and version as used by the chart label.
*/}}
{{- define "django.chart" -}}
{{- printf "%s-%s" .Chart.Name .Chart.Version | replace "+" "_" | trunc 63 | trimSuffix "-" -}}
{{- end -}}

{{/*
Common labels
*/}}
{{- define "django.labels" -}}
helm.sh/chart: {{ include "django.chart" . }}
{{ include "django.selectorLabels" . }}
{{- if .Chart.AppVersion }}
app.kubernetes.io/version: {{ .Chart.AppVersion | quote }}
{{- end }}
app.kubernetes.io/managed-by: {{ .Release.Service }}
{{- end -}}

{{/*
Selector labels
*/}}
{{- define "django.selectorLabels" -}}
app.kubernetes.io/name: {{ include "django.name" . }}
app.kubernetes.io/instance: {{ .Release.Name }}
{{- end -}}

{{/*
Create the name of the service account to use
*/}}
{{- define "django.serviceAccountName" -}}
{{- if .Values.serviceAccount.create -}}
    {{ default (include "django.fullname" .) .Values.serviceAccount.name }}
{{- else -}}
    {{ default "default" .Values.serviceAccount.name }}
{{- end -}}
{{- end -}}

{{/*
Create a default fully qualified app name.
We truncate at 63 chars because some Kubernetes name fields are limited to this (by the DNS naming spec).
*/}}
{{- define "django.postgresql.fullname" -}}
{{- if .Values.postgresql.fullnameOverride -}}
{{- .Values.postgresql.fullnameOverride | trunc 63 | trimSuffix "-" -}}
{{- else -}}
{{- $name := default .Chart.Name .Values.postgresql.nameOverride -}}
{{- if contains $name .Release.Name -}}
{{- .Release.Name | trunc 63 | trimSuffix "-" -}}-postgresql
{{- else -}}
{{- printf "%s-%s" .Release.Name "postgresql" | trunc 63 | trimSuffix "-" -}}
{{- end -}}
{{- end -}}
{{- end -}}

{{- define "django.valkey.fullname" -}}
{{- if .Values.valkey.fullnameOverride -}}
{{- .Values.valkey.fullnameOverride | trunc 63 | trimSuffix "-" -}}
{{- else -}}
{{- $name := default .Chart.Name -}}
{{- if contains $name .Release.Name -}}
{{- .Release.Name | trunc 63 | trimSuffix "-" -}}-valkey-primary
{{- else -}}
{{- printf "%s-%s" .Release.Name "valkey-primary" | trunc 63 | trimSuffix "-" -}}
{{- end -}}
{{- end -}}
{{- end -}}

{{/*
Set postgresql host
*/}}
{{- define "django.postgresql.host" -}}
{{- if .Values.postgresql.enabled -}}
{{- template "django.postgresql.fullname" . -}}
{{- end -}}
{{- end -}}

{{/*
Set postgresql username
*/}}
{{- define "django.postgresql.username" -}}
{{- if .Values.postgresql.enabled -}}
{{ .Values.postgresql.auth.username | default "postgres" }}
{{- end -}}
{{- end -}}

{{/*
Set postgresql name
*/}}
{{- define "django.postgresql.name" -}}
{{- if .Values.postgresql.enabled -}}
{{ .Values.postgresql.auth.database | default "postgres" }}
{{- end -}}
{{- end -}}

{{/*
Set postgresql port
*/}}
{{- define "django.postgresql.port" -}}
{{- if .Values.postgresql.enabled -}}
{{ .Values.postgresql.global.postgresql.service.ports.postgresql | default 5432 }}
{{- end -}}
{{- end -}}

{{/*
Set redis host
*/}}
{{- define "django.valkey.host" -}}
{{- if .Values.valkey.enabled -}}
{{- template "django.valkey.fullname" . -}}-valkey-primary
{{- else -}}
{{- .Values.valkey.host | quote -}}
{{- end -}}
{{- end -}}

{{/*
Set redis url
*/}}
{{- define "django.valkey.url" -}}
{{- if .Values.valkey.enabled -}}
redis://:{{ .Values.valkey.auth.password }}@{{- template "django.valkey.fullname" . -}}:{{- template "django.valkey.port" . -}}/0
{{- end -}}
{{- end -}}

{{/*
Set redis port
*/}}
{{- define "django.valkey.port" -}}
{{- if .Values.valkey.enabled -}}
    6379
{{- else -}}
{{- default "6379" .Values.valkey.port -}}
{{- end -}}
{{- end -}}
