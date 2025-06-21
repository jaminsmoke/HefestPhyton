# 🐳 Containerización Docker - Sistema Hefest

Configuración completa de Docker para desarrollo, testing y producción del proyecto Hefest.

---

## 📋 Índice de Contenidos

| Sección | Líneas | Descripción |
|---------|--------|-------------|
| [🏗️ Configuración Docker](#%EF%B8%8F-configuración-docker) | 18-35 | Archivos y servicios disponibles |
| [🚀 Uso y Despliegue](#-uso-y-despliegue) | 37-55 | Comandos para desarrollo y producción |
| [⚙️ Variables y Configuración](#%EF%B8%8F-variables-y-configuración) | 57-fin | Configuración de entorno y monitoreo |

---

## 🏗️ Configuración Docker

### � Archivos de Configuración

| Archivo | Propósito | Descripción |
|---------|-----------|-------------|
| `docker-compose.yml` | Stack completo | Configuración de servicios para producción |
| `Dockerfile` | Imagen de aplicación | Imagen multi-stage optimizada |

### 🔧 Servicios del Stack

#### ✅ Servicios Principales
| Servicio | Puerto | Descripción |
|----------|--------|-------------|
| **hefest-app** | 8080 | Aplicación principal Hefest |
| **hefest-db** | 5432 | Base de datos PostgreSQL |
| **hefest-redis** | 6379 | Cache y sesiones Redis |
| **hefest-nginx** | 80/443 | Reverse proxy y SSL |
| **hefest-monitoring** | 9090 | Prometheus para métricas |

#### 🎯 Características del Dockerfile
- **Multi-stage build**: Optimización de tamaño de imagen
- **Usuario no-root**: Seguridad mejorada
- **Health checks**: Monitoreo automático de salud
- **Dependencias cacheadas**: Build más rápido

---

## 🚀 Uso y Despliegue

### 🔧 Desarrollo Local

```bash
# Ejecutar stack completo
docker-compose up -d

# Solo la aplicación
docker-compose up hefest-app

# Ver logs en tiempo real
docker-compose logs -f hefest-app

# Detener servicios
docker-compose down
```

### 🏭 Producción

```bash
# Build y deploy completo
docker-compose -f docker-compose.yml up -d --build

# Escalado horizontal
docker-compose up -d --scale hefest-app=3

# Actualizar servicios
docker-compose pull && docker-compose up -d
```

### � Gestión y Debugging

```bash
# Entrar al contenedor
docker-compose exec hefest-app bash

# Ver estado de servicios
docker-compose ps

# Reiniciar servicio específico
docker-compose restart hefest-app

# Ver recursos utilizados
docker stats
```

---

## ⚙️ Variables y Configuración

### 🔧 Variables de Entorno

#### Aplicación
```env
HEFEST_ENV=production
PYTHONPATH=/app/src
DATABASE_URL=postgresql://user:pass@hefest-db:5432/hefest
```

#### Base de Datos
```env
POSTGRES_DB=hefest
POSTGRES_USER=hefest_user
POSTGRES_PASSWORD=hefest_secure_password
```

#### Cache Redis
```env
REDIS_PASSWORD=hefest_redis_password
REDIS_URL=redis://:password@hefest-redis:6379/0
```

### 🌐 Puertos Expuestos

| Puerto | Servicio | Acceso |
|--------|----------|--------|
| **80** | Nginx HTTP | Acceso web público |
| **443** | Nginx HTTPS | Acceso web seguro |
| **8080** | Hefest App | Aplicación directa |
| **5432** | PostgreSQL | Base de datos |
| **6379** | Redis | Cache |
| **9090** | Prometheus | Métricas |

### 📊 Monitoreo Incluido

#### ✅ Métricas de Sistema
- **CPU/Memoria**: Uso de recursos por contenedor
- **Disco**: Espacio y I/O por servicio
- **Red**: Tráfico y latencia

#### ✅ Métricas de Aplicación
- **Requests**: Volumen y tiempo de respuesta
- **Errores**: Rate de errores por endpoint
- **Base de datos**: Conexiones y queries

#### ✅ Alertas Automáticas
- **Alto uso de CPU**: >80% por 5 minutos
- **Memoria crítica**: >90% utilizada
- **Aplicación down**: Health check fallando

### 🔒 Seguridad

- **Usuarios no-root**: Todos los contenedores ejecutan como usuario limitado
- **Networks aisladas**: Comunicación interna segura
- **Secrets management**: Contraseñas en Docker secrets
- **SSL/TLS**: Certificados automáticos con Let's Encrypt

---

**📖 Para usar Docker**: Ejecuta `docker-compose up -d` para desarrollo o `docker-compose -f docker-compose.yml up -d --build` para producción.
