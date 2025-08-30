// Utilitários para exportação de dados

export interface ExportColumn {
  key: string
  label: string
  format?: (value: any) => string
}

export interface ExportOptions {
  filename?: string
  title?: string
  subtitle?: string
  columns: ExportColumn[]
  data: any[]
}

/**
 * Exporta dados para CSV
 */
export const exportToCSV = (options: ExportOptions): void => {
  const { filename = 'dados', columns, data } = options
  
  if (!data || data.length === 0) {
    alert('Não há dados para exportar')
    return
  }

  // Cabeçalhos
  const headers = columns.map(col => col.label)
  
  // Dados formatados
  const rows = data.map(item => 
    columns.map(col => {
      const value = item[col.key]
      if (col.format && value !== null && value !== undefined) {
        return col.format(value)
      }
      return value || ''
    })
  )

  // Criar CSV
  const csvContent = [
    headers.join(','),
    ...rows.map(row => row.map(cell => `"${String(cell).replace(/"/g, '""')}"`).join(','))
  ].join('\n')

  // Download
  const blob = new Blob([csvContent], { type: 'text/csv;charset=utf-8;' })
  const link = document.createElement('a')
  const url = URL.createObjectURL(blob)
  link.setAttribute('href', url)
  link.setAttribute('download', `${filename}-${new Date().toISOString().split('T')[0]}.csv`)
  link.style.visibility = 'hidden'
  document.body.appendChild(link)
  link.click()
  document.body.removeChild(link)
}

/**
 * Exporta dados para PDF (usando HTML e print)
 */
export const exportToPDF = (options: ExportOptions): void => {
  const { filename = 'relatorio', title = 'Relatório', subtitle, columns, data } = options
  
  if (!data || data.length === 0) {
    alert('Não há dados para exportar')
    return
  }

  // Criar HTML para impressão
  const printWindow = window.open('', '_blank')
  if (!printWindow) {
    alert('Não foi possível abrir a janela de impressão. Verifique se o bloqueador de pop-ups está desabilitado.')
    return
  }

  const currentDate = new Date().toLocaleDateString('pt-BR')
  const currentTime = new Date().toLocaleTimeString('pt-BR')

  const htmlContent = `
    <!DOCTYPE html>
    <html>
    <head>
      <meta charset="utf-8">
      <title>${title}</title>
      <style>
        @media print {
          @page {
            margin: 1cm;
            size: A4;
          }
        }
        
        body {
          font-family: Arial, sans-serif;
          margin: 0;
          padding: 20px;
          color: #333;
        }
        
        .header {
          text-align: center;
          margin-bottom: 30px;
          border-bottom: 2px solid #dc2626;
          padding-bottom: 20px;
        }
        
        .header h1 {
          color: #dc2626;
          margin: 0 0 10px 0;
          font-size: 24px;
        }
        
        .header h2 {
          color: #666;
          margin: 0 0 10px 0;
          font-size: 18px;
          font-weight: normal;
        }
        
        .header .meta {
          color: #888;
          font-size: 12px;
        }
        
        table {
          width: 100%;
          border-collapse: collapse;
          margin-top: 20px;
          font-size: 12px;
        }
        
        th, td {
          border: 1px solid #ddd;
          padding: 8px;
          text-align: left;
        }
        
        th {
          background-color: #f8f9fa;
          font-weight: bold;
          color: #333;
        }
        
        tr:nth-child(even) {
          background-color: #f9f9f9;
        }
        
        .footer {
          margin-top: 30px;
          text-align: center;
          font-size: 10px;
          color: #888;
          border-top: 1px solid #ddd;
          padding-top: 10px;
        }
        
        .summary {
          margin-bottom: 20px;
          padding: 15px;
          background-color: #f8f9fa;
          border-radius: 5px;
        }
        
        .summary h3 {
          margin: 0 0 10px 0;
          color: #dc2626;
        }
      </style>
    </head>
    <body>
      <div class="header">
        <h1>Sistema de Abatedouro</h1>
        <h2>${title}</h2>
        ${subtitle ? `<p>${subtitle}</p>` : ''}
        <div class="meta">
          Gerado em: ${currentDate} às ${currentTime}
        </div>
      </div>
      
      <div class="summary">
        <h3>Resumo</h3>
        <p>Total de registros: <strong>${data.length}</strong></p>
      </div>
      
      <table>
        <thead>
          <tr>
            ${columns.map(col => `<th>${col.label}</th>`).join('')}
          </tr>
        </thead>
        <tbody>
          ${data.map(item => `
            <tr>
              ${columns.map(col => {
                const value = item[col.key]
                const formattedValue = col.format && value !== null && value !== undefined 
                  ? col.format(value) 
                  : (value || '')
                return `<td>${String(formattedValue)}</td>`
              }).join('')}
            </tr>
          `).join('')}
        </tbody>
      </table>
      
      <div class="footer">
        <p>Sistema de Abatedouro - Relatório gerado automaticamente</p>
      </div>
    </body>
    </html>
  `

  printWindow.document.write(htmlContent)
  printWindow.document.close()
  
  // Aguardar carregamento e imprimir
  printWindow.onload = () => {
    setTimeout(() => {
      printWindow.print()
      printWindow.close()
    }, 250)
  }
}

/**
 * Formata data para exibição
 */
export const formatDate = (date: string | Date): string => {
  if (!date) return ''
  const d = new Date(date)
  return d.toLocaleDateString('pt-BR')
}

/**
 * Formata data e hora para exibição
 */
export const formatDateTime = (date: string | Date): string => {
  if (!date) return ''
  const d = new Date(date)
  return `${d.toLocaleDateString('pt-BR')} ${d.toLocaleTimeString('pt-BR')}`
}

/**
 * Formata número como moeda brasileira
 */
export const formatCurrency = (value: number): string => {
  if (value === null || value === undefined) return 'R$ 0,00'
  return new Intl.NumberFormat('pt-BR', {
    style: 'currency',
    currency: 'BRL'
  }).format(value)
}

/**
 * Formata número com separadores de milhares
 */
export const formatNumber = (value: number, decimals: number = 0): string => {
  if (value === null || value === undefined) return '0'
  return new Intl.NumberFormat('pt-BR', {
    minimumFractionDigits: decimals,
    maximumFractionDigits: decimals
  }).format(value)
}

/**
 * Formata peso em kg
 */
export const formatWeight = (value: number): string => {
  if (value === null || value === undefined) return '0 kg'
  return `${formatNumber(value, 2)} kg`
}