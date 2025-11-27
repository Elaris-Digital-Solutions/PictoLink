-- Create table for storing user pictograms (favorites and recents)
create table public.user_pictograms (
  id uuid default gen_random_uuid() primary key,
  user_id uuid references auth.users(id) on delete cascade not null,
  pictogram_id integer not null,
  type text check (type in ('favorite', 'recent')) not null,
  data jsonb not null, -- Stores the full pictogram object
  created_at timestamp with time zone default timezone('utc'::text, now()) not null,
  last_used_at timestamp with time zone default timezone('utc'::text, now()) not null,
  
  -- Prevent duplicates for the same user, pictogram, and type
  unique(user_id, pictogram_id, type)
);

-- Set up Row Level Security (RLS)
alter table public.user_pictograms enable row level security;

-- Policy: Users can view their own pictograms
create policy "Users can view their own pictograms"
  on public.user_pictograms for select
  using (auth.uid() = user_id);

-- Policy: Users can insert their own pictograms
create policy "Users can insert their own pictograms"
  on public.user_pictograms for insert
  with check (auth.uid() = user_id);

-- Policy: Users can update their own pictograms
create policy "Users can update their own pictograms"
  on public.user_pictograms for update
  using (auth.uid() = user_id);

-- Policy: Users can delete their own pictograms
create policy "Users can delete their own pictograms"
  on public.user_pictograms for delete
  using (auth.uid() = user_id);
