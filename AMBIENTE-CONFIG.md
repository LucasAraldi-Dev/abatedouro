# Configuração de Ambientes

Este projeto agora suporta configurações separadas para desenvolvimento e produção.

## 📁 Estrutura dos Arquivos de Ambiente

### Frontend (interface/)
- `.env.development` - Configurações para desenvolvimento local
- `.env.production` - Configurações para produção (Render)

### Backend (servidor/)
- `.env` - Arquivo ativo (atualmente configurado para desenvolvimento)
- `.env.development` - Template para desenvolvimento
- `.env.production` - Template para produção

## 🚀 Como Executar

### Frontend

#### Opção 1: Script Interativo (Recomendado)
```bash
cd interface
npm run dev
```
O sistema perguntará qual ambiente usar:
- **1** = Desenvolvimento (localhost:8000)
- **2** = Produção (Render)

#### Opção 2: Comandos Diretos
```bash
# Desenvolvimento
npm run dev:local

# Produção
npm run dev:prod
```

### Backend

#### Para Desenvolvimento (Atual)
O arquivo `.env` já está configurado para desenvolvimento.
```bash
cd servidor
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

#### Para Produção
1. Faça backup do `.env` atual:
   ```bash
   cp .env .env.backup
   ```

2. Copie as configurações de produção:
   ```bash
   cp .env.production .env
   ```

3. Execute o servidor:
   ```bash
   uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
   ```

## 🔧 Configurações por Ambiente

### Desenvolvimento
- **Frontend**: `http://localhost:5173`
- **Backend**: `http://localhost:8000`
- **Banco**: `abatedouro_dev` (MongoDB Atlas)
- **CORS**: Apenas localhost

### Produção
- **Frontend**: Vite com configurações de produção
- **Backend**: `https://abatedouro-jkax.onrender.com`
- **Banco**: `abatedouro` (MongoDB Atlas)
- **CORS**: Inclui domínios do Render

## 📝 Notas Importantes

1. **Banco de Dados**: Desenvolvimento usa `abatedouro_dev`, produção usa `abatedouro`
2. **CORS**: Desenvolvimento permite apenas localhost, produção inclui Render
3. **Logs**: Desenvolvimento tem debug ativo, produção tem logs otimizados
4. **Vite**: Usa `import.meta.env.VITE_*` para acessar variáveis de ambiente

## 🔄 Alternando Rapidamente

### Para Desenvolvimento
```bash
# Backend
cd servidor
cp .env.development .env

# Frontend
cd interface
npm run dev:local
```

### Para Produção
```bash
# Backend
cd servidor
cp .env.production .env

# Frontend
cd interface
npm run dev:prod
```