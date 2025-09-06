#!/usr/bin/env node

import { createInterface } from 'readline';
import { spawn } from 'child_process';
import { fileURLToPath } from 'url';
import { dirname, join } from 'path';

const __filename = fileURLToPath(import.meta.url);
const __dirname = dirname(__filename);

const rl = createInterface({
  input: process.stdin,
  output: process.stdout
});

console.log('\n🚀 Seleção de Ambiente para Desenvolvimento\n');
console.log('Escolha o ambiente que deseja executar:');
console.log('1. Desenvolvimento (Local - http://localhost:8000)');
console.log('2. Produção (Render - https://abatedouro-jkax.onrender.com)');
console.log('');

rl.question('Digite sua escolha (1 ou 2): ', (answer) => {
  let mode;
  let description;
  
  switch (answer.trim()) {
    case '1':
      mode = 'development';
      description = 'Desenvolvimento (Local)';
      break;
    case '2':
      mode = 'production';
      description = 'Produção (Render)';
      break;
    default:
      console.log('\n❌ Opção inválida! Usando desenvolvimento por padrão.');
      mode = 'development';
      description = 'Desenvolvimento (Local)';
      break;
  }
  
  console.log(`\n✅ Iniciando em modo: ${description}`);
  console.log(`📁 Carregando configurações de: .env.${mode}`);
  console.log('\n🔄 Iniciando servidor de desenvolvimento...\n');
  
  rl.close();
  
  // Executar vite com o modo selecionado
  const viteProcess = spawn('npx', ['vite', '--mode', mode], {
    stdio: 'inherit',
    shell: true,
    cwd: join(__dirname, '..')
  });
  
  viteProcess.on('error', (error) => {
    console.error('❌ Erro ao iniciar o Vite:', error);
    process.exit(1);
  });
  
  viteProcess.on('close', (code) => {
    process.exit(code);
  });
});

// Tratar Ctrl+C
process.on('SIGINT', () => {
  console.log('\n\n👋 Processo cancelado pelo usuário.');
  rl.close();
  process.exit(0);
});