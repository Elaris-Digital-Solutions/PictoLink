-- Actualizar el trigger para crear perfiles correctamente
-- Este script corrige el problema del Display name vacío

-- 1. Eliminar el trigger y función existentes
drop trigger if exists on_auth_user_created on auth.users;
drop function if exists public.handle_new_user();

-- 2. Crear nueva función mejorada
create or replace function public.handle_new_user()
returns trigger
security definer
set search_path = public
language plpgsql
as $$
declare
  user_name text;
begin
  -- Obtener el nombre del user_metadata o usar el email como fallback
  user_name := coalesce(
    new.raw_user_meta_data->>'name',
    split_part(new.email, '@', 1)
  );
  
  -- Insertar en la tabla profiles
  insert into public.profiles (id, name)
  values (new.id, user_name);
  
  return new;
end;
$$;

-- 3. Recrear el trigger
create trigger on_auth_user_created
  after insert on auth.users
  for each row execute function public.handle_new_user();

-- 4. Actualizar usuarios existentes sin perfil o con nombre vacío
insert into public.profiles (id, name)
select 
  id, 
  coalesce(
    raw_user_meta_data->>'name',
    split_part(email, '@', 1)
  )
from auth.users
where id not in (select id from public.profiles)
on conflict (id) do update
set name = coalesce(
  excluded.name,
  split_part((select email from auth.users where id = profiles.id), '@', 1)
)
where profiles.name is null or profiles.name = '';

-- ============================================
-- FIN DEL SCRIPT
-- ============================================
