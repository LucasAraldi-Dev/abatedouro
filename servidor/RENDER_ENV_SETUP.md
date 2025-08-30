# Configuração de Variáveis de Ambiente no Render

O backend está funcionando localmente, mas no Render as variáveis de ambiente precisam ser configuradas manualmente no painel de controle.

## Variáveis de Ambiente Necessárias no Render

Acesse o painel do Render (https://dashboard.render.com) e configure as seguintes variáveis de ambiente para o serviço `abatedouro-jkax`:

### 1. MongoDB
```
MONGODB_URI=mongodb://lucasaraldi:R6pXvaislUmmKm8A@ac-nqlllrv-shard-00-00.tvwmq9c.mongodb.net:27017,ac-nqlllrv-shard-00-01.tvwmq9c.mongodb.net:27017,ac-nqlllrv-shard-00-02.tvwmq9c.mongodb.net:27017/abatedouro?ssl=true&authSource=admin&retryWrites=true&w=majority
MONGODB_DBNAME=abatedouro
```

### 2. API
```
API_V1_STR=/api/v1
APP_NAME=Abatedouro API
```

### 3. CORS (MAIS IMPORTANTE)
```
BACKEND_CORS_ORIGINS=http://localhost:5173,http://127.0.0.1:5173,https://abatedouro-frontend.onrender.com,https://abatedouro-jkax.onrender.com
```

## Como Configurar no Render

1. Acesse https://dashboard.render.com
2. Clique no serviço `abatedouro-jkax`
3. Vá para a aba "Environment"
4. Adicione cada variável de ambiente listada acima
5. Clique em "Save Changes"
6. O serviço será automaticamente reimplantado

## Verificação

Após configurar, teste acessando:
- https://abatedouro-jkax.onrender.com/api/v1/saude/
- Verifique se os headers CORS estão presentes na resposta

## Teste Local vs Render

✅ **Local**: CORS funcionando corretamente (testado)
❌ **Render**: Variáveis de ambiente não configuradas

**Solução**: Configurar as variáveis de ambiente no painel do Render conforme instruções acima.