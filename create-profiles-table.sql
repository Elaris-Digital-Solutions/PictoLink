-- ============================================
-- CREAR TABLA DE PERFILES DE USUARIO
-- ============================================

-- 1. Crear tabla de perfiles
create table if not exists public.profiles (
  id uuid references auth.users(id) on delete cascade primary key,
  name text not null,
  created_at timestamp with time zone default timezone('utc'::text, now()) not null,
  updated_at timestamp with time zone default timezone('utc'::text, now()) not null
);

-- 2. Habilitar RLS
alter table public.profiles enable row level security;

-- 3. Políticas de seguridad
-- Todos pueden ver todos los perfiles (necesario para mostrar nombres de contactos)
create policy "Profiles are viewable by everyone"
  on public.profiles for select
  using (true);

-- Los usuarios solo pueden actualizar su propio perfil
create policy "Users can update own profile"
  on public.profiles for update
  using (auth.uid() = id);

-- 4. Crear función para crear perfil automáticamente al registrarse
create or replace function public.handle_new_user()
returns trigger
security definer
set search_path = public
language plpgsql
as $$
begin
  insert into public.profiles (id, name)
  values (new.id, new.raw_user_meta_data->>'name');
  return new;
end;
$$;

-- 5. Crear trigger para ejecutar la función al crear un usuario
drop trigger if exists on_auth_user_created on auth.users;
create trigger on_auth_user_created
  after insert on auth.users
  for each row execute function public.handle_new_user();

-- 6. Migrar usuarios existentes a la tabla de perfiles
insert into public.profiles (id, name)
select 
  id, 
  coalesce(raw_user_meta_data->>'name', email)
from auth.users
where id not in (select id from public.profiles)
on conflict (id) do nothing;

-- ============================================
-- FIN DEL SCRIPT
-- ============================================
