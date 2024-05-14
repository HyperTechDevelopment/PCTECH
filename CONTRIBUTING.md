# Contribuindo para HyperTech

Agradecemos seu interesse em contribuir para a HyperTech! Queremos tornar o processo de contribuição o mais simples e eficaz possível. Este documento descreve como você pode participar.

## Como Contribuir
### Reportando Bugs

Encontrou um bug? Por favor, reporte-o usando a aba de [Issues](https://github.com/HyperTechDevelopment/PCTECH/issues). Certifique-se de incluir detalhes suficientes para que possamos reproduzir e corrigir o problema.

### Sugerindo Melhorias

Tem uma ideia para melhorar nosso software? Adoramos novas ideias! Abra uma Issue com a tag "melhoria" e descreva sua sugestão em detalhes.

### Fazendo Pull Requests

Para garantir a qualidade e a segurança do nosso código, temos algumas diretrizes para Pull Requests (PRs):

1. **Fork o Repositório**: Faça um fork do repositório e crie sua branch a partir da `master`.
2. **Siga as Convenções de Código**: Certifique-se de seguir nossas diretrizes de estilo de código.
3. **Faça Commits Assinados**: Todos os commits devem ser assinados digitalmente para garantir a integridade e a autoria. [Saiba como assinar seus commits](https://docs.github.com/en/authentication/managing-commit-signature-verification/signing-commits).
4. **Escreva Testes**: Se você adicionar novos recursos ou corrigir bugs, escreva testes para garantir que tudo funcione conforme esperado.
5. **Atualize a Documentação**: Certifique-se de que a documentação está atualizada com qualquer mudança ou nova funcionalidade.
6. **Submeta o Pull Request**: Abra um PR para a branch `master`. Sua submissão passará pelo processo de revisão e aprovação conforme descrito abaixo.

### Revisão de Pull Requests

Para garantir a qualidade do código, todas as PRs passarão pelas seguintes etapas:

- **Revisões Necessárias**: Cada PR deve ser revisada e aprovada por pelo menos um revisor.
- **Desaprovação de Revisões Desatualizadas**: Se novos commits forem adicionados a um PR, as aprovações anteriores serão descartadas e precisarão ser reavaliadas.
- **Revisão de Code Owners**: PRs que modificam arquivos com proprietários de código designados precisarão de aprovação desses proprietários.
- **Checks de Status**: Todos os checks de status configurados devem passar antes que o PR possa ser mesclado.

### Configuração do Ambiente de Desenvolvimento

Para configurar seu ambiente de desenvolvimento local:

1. Clone o repositório:
   ```bash
   git clone https://github.com/HyperTechDevelopment/PCTECH.git
   cd PCTECH
