<template>
  <div v-if="isVisible" class="modal-overlay">
    <div class="modal-container modal-large" @click.stop>
      <div class="modal-header">
        <h2>Configuração de Limites e Alertas</h2>
        <button class="close-btn" @click="closeModal">&times;</button>
      </div>
      
      <div class="modal-body">
        <div class="config-sections">
          <!-- Seção de Performance -->
          <div class="config-section">
            <h3>📈 Limites de Performance</h3>
            <div class="form-row">
              <div class="form-group">
                <label for="rendimentoMinimo">Rendimento Mínimo (%):</label>
                <input
                  id="rendimentoMinimo"
                  v-model.number="config.rendimento_minimo"
                  type="number"
                  step="0.1"
                  min="0"
                  max="100"
                  class="form-input"
                />
              </div>
              <div class="form-group">
                <label for="rendimentoIdeal">Rendimento Ideal (%):</label>
                <input
                  id="rendimentoIdeal"
                  v-model.number="config.rendimento_ideal"
                  type="number"
                  step="0.1"
                  min="0"
                  max="100"
                  class="form-input"
                />
              </div>
            </div>
          </div>

          <!-- Seção de Lucro -->
          <div class="config-section">
            <h3>💰 Limites de Lucro</h3>
            <div class="form-row">
              <div class="form-group">
                <label for="lucroMinimo">Lucro Mínimo por Ave (R$):</label>
                <input
                  id="lucroMinimo"
                  v-model.number="config.lucro_minimo_por_ave"
                  type="number"
                  step="0.01"
                  min="0"
                  class="form-input"
                />
              </div>
              <div class="form-group">
                <label for="lucroIdeal">Lucro Ideal por Ave (R$):</label>
                <input
                  id="lucroIdeal"
                  v-model.number="config.lucro_ideal_por_ave"
                  type="number"
                  step="0.01"
                  min="0"
                  class="form-input"
                />
              </div>
            </div>
          </div>

          <!-- Seção de Eficiência -->
          <div class="config-section">
            <h3>⚡ Limites de Eficiência Operacional</h3>
            <div class="form-row">
              <div class="form-group">
                <label for="avesHoraMinimo">Aves por Hora Mínimo:</label>
                <input
                  id="avesHoraMinimo"
                  v-model.number="config.aves_por_hora_minimo"
                  type="number"
                  step="1"
                  min="0"
                  class="form-input"
                />
              </div>
              <div class="form-group">
                <label for="avesHoraIdeal">Aves por Hora Ideal:</label>
                <input
                  id="avesHoraIdeal"
                  v-model.number="config.aves_por_hora_ideal"
                  type="number"
                  step="1"
                  min="0"
                  class="form-input"
                />
              </div>
            </div>
          </div>

          <!-- Seção de Qualidade -->
          <div class="config-section">
            <h3>🎯 Limites de Qualidade</h3>
            <div class="form-row">
              <div class="form-group">
                <label for="pesoMedioMinimo">Peso Médio Mínimo por Ave (kg):</label>
                <input
                  id="pesoMedioMinimo"
                  v-model.number="config.peso_medio_minimo"
                  type="number"
                  step="0.01"
                  min="0"
                  class="form-input"
                />
              </div>
              <div class="form-group">
                <label for="pesoMedioIdeal">Peso Médio Ideal por Ave (kg):</label>
                <input
                  id="pesoMedioIdeal"
                  v-model.number="config.peso_medio_ideal"
                  type="number"
                  step="0.01"
                  min="0"
                  class="form-input"
                />
              </div>
            </div>
          </div>

          <!-- Seção de Custos -->
          <div class="config-section">
            <h3>💸 Limites de Custos</h3>
            <div class="form-row">
              <div class="form-group">
                <label for="custoMaximo">Custo Operacional Máximo por Ave (R$):</label>
                <input
                  id="custoMaximo"
                  v-model.number="config.custo_operacional_maximo_por_ave"
                  type="number"
                  step="0.01"
                  min="0"
                  class="form-input"
                />
              </div>
              <div class="form-group">
                <label for="custoIdeal">Custo Operacional Ideal por Ave (R$):</label>
                <input
                  id="custoIdeal"
                  v-model.number="config.custo_operacional_ideal_por_ave"
                  type="number"
                  step="0.01"
                  min="0"
                  class="form-input"
                />
              </div>
            </div>
          </div>

          <!-- Seção de Perdas -->
          <div class="config-section">
            <h3>📉 Limites de Perdas</h3>
            <div class="form-row">
              <div class="form-group">
                <label for="perdasMaximo">Percentual Máximo de Perdas (%):</label>
                <input
                  id="perdasMaximo"
                  v-model.number="config.percentual_perdas_maximo"
                  type="number"
                  step="0.1"
                  min="0"
                  max="100"
                  class="form-input"
                />
              </div>
            </div>
          </div>

          <!-- Seção de Alertas -->
          <div class="config-section">
            <h3>🔔 Configuração de Alertas</h3>
            <div class="alert-toggles">
              <div class="form-group checkbox-group">
                <label class="checkbox-label">
                  <input
                    v-model="config.alertas_ativos"
                    type="checkbox"
                    class="checkbox-input"
                  />
                  <span class="checkbox-text">Alertas Ativos</span>
                </label>
              </div>
              
              <div v-if="config.alertas_ativos" class="alert-options">
                <div class="form-group checkbox-group">
                  <label class="checkbox-label">
                    <input
                      v-model="config.alerta_rendimento_baixo"
                      type="checkbox"
                      class="checkbox-input"
                    />
                    <span class="checkbox-text">Alerta de Rendimento Baixo</span>
                  </label>
                </div>
                
                <div class="form-group checkbox-group">
                  <label class="checkbox-label">
                    <input
                      v-model="config.alerta_lucro_baixo"
                      type="checkbox"
                      class="checkbox-input"
                    />
                    <span class="checkbox-text">Alerta de Lucro Baixo</span>
                  </label>
                </div>
                
                <div class="form-group checkbox-group">
                  <label class="checkbox-label">
                    <input
                      v-model="config.alerta_eficiencia_baixa"
                      type="checkbox"
                      class="checkbox-input"
                    />
                    <span class="checkbox-text">Alerta de Eficiência Baixa</span>
                  </label>
                </div>
                
                <div class="form-group checkbox-group">
                  <label class="checkbox-label">
                    <input
                      v-model="config.alerta_qualidade_baixa"
                      type="checkbox"
                      class="checkbox-input"
                    />
                    <span class="checkbox-text">Alerta de Qualidade Baixa</span>
                  </label>
                </div>
                
                <div class="form-group checkbox-group">
                  <label class="checkbox-label">
                    <input
                      v-model="config.alerta_custo_alto"
                      type="checkbox"
                      class="checkbox-input"
                    />
                    <span class="checkbox-text">Alerta de Custo Alto</span>
                  </label>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
      
      <div class="modal-footer">
        <button class="btn btn-secondary" @click="closeModal">Cancelar</button>
        <button class="btn btn-primary" @click="salvarConfiguracao" :disabled="isLoading">
          {{ isLoading ? 'Salvando...' : 'Salvar Configuração' }}
        </button>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios'
import { useToast } from '../composables/useToast'

export default {
  name: 'ModalConfiguracaoLimites',
  props: {
    isVisible: {
      type: Boolean,
      default: false
    }
  },
  
  data() {
    return {
      isLoading: false,
      config: {
        rendimento_minimo: 75.0,
        rendimento_ideal: 85.0,
        lucro_minimo_por_ave: 5.0,
        lucro_ideal_por_ave: 8.0,
        aves_por_hora_minimo: 80.0,
        aves_por_hora_ideal: 120.0,
        peso_medio_minimo: 1.8,
        peso_medio_ideal: 2.2,
        custo_operacional_maximo_por_ave: 3.0,
        custo_operacional_ideal_por_ave: 2.5,
        percentual_perdas_maximo: 15.0,
        alertas_ativos: true,
        alerta_rendimento_baixo: true,
        alerta_lucro_baixo: true,
        alerta_eficiencia_baixa: true,
        alerta_qualidade_baixa: true,
        alerta_custo_alto: true
      }
    }
  },
  
  setup() {
    const { showSuccess, showError } = useToast()
    return { showSuccess, showError }
  },
  
  async mounted() {
    await this.carregarConfiguracao()
  },
  
  methods: {
    async carregarConfiguracao() {
      try {
        const response = await axios.get('/api/v1/configuracao-limites/')
        if (response.data) {
          this.config = { ...this.config, ...response.data }
        }
      } catch (error) {
        console.log('Nenhuma configuração encontrada, usando valores padrão')
      }
    },
    
    async salvarConfiguracao() {
      this.isLoading = true
      try {
        await axios.post('/api/v1/configuracao-limites/', this.config)
        this.showSuccess('Configuração de limites salva com sucesso!')
        this.$emit('configuracao-salva')
        this.closeModal()
      } catch (error) {
        console.error('Erro ao salvar configuração:', error)
        this.showError('Erro ao salvar configuração de limites')
      } finally {
        this.isLoading = false
      }
    },
    
    closeModal() {
      this.$emit('close')
    }
  }
}
</script>

<style scoped>
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.5);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1000;
}

.modal-container {
  background: white;
  border-radius: 12px;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.3);
  width: 90%;
  max-width: 800px;
  max-height: 90vh;
  overflow-y: auto;
}

.modal-large {
  max-width: 900px;
}

.modal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 20px;
  border-bottom: 1px solid #e0e0e0;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  border-radius: 12px 12px 0 0;
}

.modal-header h2 {
  margin: 0;
  font-size: 1.5rem;
  font-weight: 600;
}

.close-btn {
  background: none;
  border: none;
  font-size: 2rem;
  color: white;
  cursor: pointer;
  padding: 0;
  width: 30px;
  height: 30px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 50%;
  transition: background-color 0.2s;
}

.close-btn:hover {
  background-color: rgba(255, 255, 255, 0.2);
}

.modal-body {
  padding: 20px;
}

.config-sections {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.config-section {
  border: 1px solid #e0e0e0;
  border-radius: 8px;
  padding: 16px;
  background: #f9f9f9;
}

.config-section h3 {
  margin: 0 0 16px 0;
  color: #333;
  font-size: 1.1rem;
  font-weight: 600;
}

.form-row {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 16px;
}

.form-group {
  display: flex;
  flex-direction: column;
}

.form-group label {
  margin-bottom: 4px;
  font-weight: 500;
  color: #555;
  font-size: 0.9rem;
}

.form-input {
  padding: 8px 12px;
  border: 1px solid #ddd;
  border-radius: 6px;
  font-size: 0.9rem;
  transition: border-color 0.2s;
}

.form-input:focus {
  outline: none;
  border-color: #667eea;
  box-shadow: 0 0 0 2px rgba(102, 126, 234, 0.2);
}

.checkbox-group {
  flex-direction: row;
  align-items: center;
  margin-bottom: 8px;
}

.checkbox-label {
  display: flex;
  align-items: center;
  cursor: pointer;
  margin: 0;
}

.checkbox-input {
  margin-right: 8px;
  width: 16px;
  height: 16px;
}

.checkbox-text {
  font-size: 0.9rem;
  color: #555;
}

.alert-options {
  margin-left: 20px;
  padding-left: 16px;
  border-left: 2px solid #667eea;
}

.modal-footer {
  display: flex;
  justify-content: flex-end;
  gap: 12px;
  padding: 20px;
  border-top: 1px solid #e0e0e0;
  background: #f8f9fa;
  border-radius: 0 0 12px 12px;
}

.btn {
  padding: 10px 20px;
  border: none;
  border-radius: 6px;
  font-size: 0.9rem;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s;
}

.btn-secondary {
  background: #6c757d;
  color: white;
}

.btn-secondary:hover {
  background: #5a6268;
}

.btn-primary {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
}

.btn-primary:hover {
  transform: translateY(-1px);
  box-shadow: 0 4px 12px rgba(102, 126, 234, 0.3);
}

.btn:disabled {
  opacity: 0.6;
  cursor: not-allowed;
  transform: none;
}

@media (max-width: 768px) {
  .modal-container {
    width: 95%;
    margin: 10px;
  }
  
  .form-row {
    grid-template-columns: 1fr;
  }
  
  .modal-header {
    padding: 16px;
  }
  
  .modal-body {
    padding: 16px;
  }
}
</style>