-- Actualizar la función add_contact_by_email con SECURITY DEFINER
-- Esto le da permisos para acceder a auth.users

drop function if exists public.add_contact_by_email(uuid, text);

create or replace function public.add_contact_by_email(p_user_id uuid, p_email text)
returns jsonb
language plpgsql
security definer -- IMPORTANTE: Esto permite acceder a auth.users
set search_path = public
as $$
declare
  found_id uuid;
begin
  -- 1) Buscar usuario por email
  select id into found_id
  from auth.users
  where email = p_email
  limit 1;

  if found_id is null then
    return jsonb_build_object('status', 'error', 'message', 'user_not_found');
  end if;

  -- 2) Evitar que se agregue a sí mismo
  if found_id = p_user_id then
    return jsonb_build_object('status', 'error', 'message', 'cannot_add_self');
  end if;

  -- 3) Si ya existe la relación, devolver error
  if exists (
    select 1
    from public.contacts
    where user_id = p_user_id
      and contact_id = found_id
  ) then
    return jsonb_build_object('status', 'error', 'message', 'already_contact');
  end if;

  -- 4) Insertar relación A → B
  insert into public.contacts (user_id, contact_id)
  values (p_user_id, found_id)
  on conflict (user_id, contact_id) do nothing;

  -- 5) Insertar relación B → A (bidireccional)
  insert into public.contacts (user_id, contact_id)
  values (found_id, p_user_id)
  on conflict (user_id, contact_id) do nothing;

  -- 6) Devolver OK
  return jsonb_build_object('status', 'ok', 'contact_id', found_id);
end;
$$;
