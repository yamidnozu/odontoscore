import { defineConfig } from 'astro/config';
import react from '@astrojs/react';

// https://astro.build/config
export default defineConfig({
  site: 'https://odontoscore.com',
  integrations: [react()],
  build: {
    format: 'file' // Crucial: genera /producto/id.html y /categoria/slug.html en lugar de carpetas con index.html
  }
});
