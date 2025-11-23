-- ============================================
-- SCRIPT SQL PARA SUPABASE - SISTEMA DE CONTACTOS Y MENSAJERÍA
-- VERSIÓN ACTUALIZADA (Elimina políticas existentes primero)
-- ============================================

-- 1. ELIMINAR POLÍTICAS EXISTENTES (si existen)
-- ============================================
drop policy if exists "Users can view their own contacts" on public.contacts;
drop policy if exists "Users can insert their own contacts" on public.contacts;
drop policy if exists "Users can delete their own contacts" on public.contacts;
drop policy if exists "Users can view their messages" on public.messages;
drop policy if exists "Users can send messages" on public.messages;
drop policy if exists "Users can update received messages" on public.messages;

-- 2. CREAR TABLA DE CONTACTOS
-- ============================================
create table if not exists public.contacts (
  id uuid default gen_random_uuid() primary key,
  user_id uuid references auth.users(id) on delete cascade not null,
  contact_id uuid references auth.users(id) on delete cascade not null,
  created_at timestamp with time zone default timezone('utc'::text, now()) not null,
  
  -- Evitar duplicados
  unique(user_id, contact_id)
);

-- Índices para optimizar consultas
create index if not exists contacts_user_id_idx on public.contacts(user_id);
create index if not exists contacts_contact_id_idx on public.contacts(contact_id);

-- 3. CREAR TABLA DE MENSAJES
-- ============================================
create table if not exists public.messages (
  id uuid default gen_random_uuid() primary key,
  sender_id uuid references auth.users(id) on delete cascade not null,
  receiver_id uuid references auth.users(id) on delete cascade not null,
  content text not null,
  created_at timestamp with time zone default timezone('utc'::text, now()) not null,
  read boolean default false not null
);

-- Índices para optimizar consultas
create index if not exists messages_sender_id_idx on public.messages(sender_id);
create index if not exists messages_receiver_id_idx on public.messages(receiver_id);
create index if not exists messages_created_at_idx on public.messages(created_at desc);

-- 4. HABILITAR ROW LEVEL SECURITY (RLS)
-- ============================================
alter table public.contacts enable row level security;
alter table public.messages enable row level security;

-- 5. POLÍTICAS DE SEGURIDAD PARA CONTACTS
-- ============================================

-- Los usuarios pueden ver sus propios contactos
create policy "Users can view their own contacts"
  on public.contacts for select
  using (auth.uid() = user_id);

-- Los usuarios pueden insertar sus propios contactos
create policy "Users can insert their own contacts"
  on public.contacts for insert
  with check (auth.uid() = user_id);

-- Los usuarios pueden eliminar sus propios contactos
create policy "Users can delete their own contacts"
  on public.contacts for delete
  using (auth.uid() = user_id);

-- 6. POLÍTICAS DE SEGURIDAD PARA MESSAGES
-- ============================================

-- Los usuarios pueden ver mensajes donde son emisor o receptor
create policy "Users can view their messages"
  on public.messages for select
  using (
    auth.uid() = sender_id or 
    auth.uid() = receiver_id
  );

-- Los usuarios pueden insertar mensajes donde son el emisor
create policy "Users can send messages"
  on public.messages for insert
  with check (auth.uid() = sender_id);

-- Los usuarios pueden actualizar mensajes donde son el receptor (para marcar como leído)
create policy "Users can update received messages"
  on public.messages for update
  using (auth.uid() = receiver_id);

-- 7. HABILITAR REALTIME PARA MENSAJES
-- ============================================
-- Esto permite recibir mensajes en tiempo real
-- Nota: Si ya está agregada, este comando fallará pero no es problema
do $$
begin
  alter publication supabase_realtime add table public.messages;
exception
  when duplicate_object then
    null; -- La tabla ya está en la publicación, no hacer nada
end $$;

-- ============================================
-- FIN DEL SCRIPT
-- ============================================

-- VERIFICACIÓN: Ejecuta estas queries para verificar que todo se creó correctamente
-- SELECT * FROM public.contacts;
-- SELECT * FROM public.messages;
