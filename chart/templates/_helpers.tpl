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
Name of the bundled Postgres resources (Service, StatefulSet, Secret).
*/}}
{{- define "django.postgresName" -}}
{{ include "django.fullname" . }}-postgres
{{- end -}}

{{/*
DATABASE_URL env entry sourced from the chart-managed Postgres Secret.
Included in web Deployment and Jobs when postgres.enabled=true so it
overrides any DATABASE_URL loaded from `existingSecret` via envFrom.
*/}}
{{- define "django.postgresDatabaseUrlEnv" -}}
- name: DATABASE_URL
  valueFrom:
    secretKeyRef:
      name: {{ include "django.postgresName" . }}
      key: DATABASE_URL
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
