# PictoLink

Una aplicación de mensajería con soporte para pictogramas usando ARASAAC.

## Configuración

### 1. Instalar dependencias
```bash
npm install
```

### 2. Configurar Supabase
1. Crea un proyecto en [Supabase](https://supabase.com)
2. Ve a Settings > API en tu dashboard de Supabase
3. Copia el Project URL y anon/public key
4. Crea un archivo `.env.local` en la raíz del proyecto con:

```
VITE_SUPABASE_URL=tu_supabase_project_url
VITE_SUPABASE_ANON_KEY=tu_supabase_anon_key
```

### 3. Configurar la base de datos
Ejecuta el script `supabase-setup.sql` en tu base de datos de Supabase para crear las tablas necesarias.

### 4. Ejecutar la aplicación
```bash
npm run dev
```

## Funcionalidades

- Chat en tiempo real
- Soporte para pictogramas de ARASAAC
- Reconocimiento de voz
- Síntesis de voz
- Gestión de contactos

## Tecnologías

- React + TypeScript + Vite
- Supabase (Backend y base de datos)
- Tailwind CSS + shadcn/ui
- API de ARASAAC para pictogramas