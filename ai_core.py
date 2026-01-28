import openai
import anthropic
import os
from typing import Optional

class AICore:
    def __init__(self, provider="openai"):
        self.provider = provider
        
        if provider == "openai":
            # Configurar OpenAI
            openai.api_key = os.getenv("OPENAI_API_KEY", "sua-chave-openai")
            self.model = "gpt-4"
        elif provider == "claude":
            # Configurar Anthropic Claude
            self.client = anthropic.Anthropic(
                api_key=os.getenv("ANTHROPIC_API_KEY", "sua-chave-claude")
            )
            self.model = "claude-3-opus-20240229"
        else:
            raise ValueError("Provider deve ser 'openai' ou 'claude'")
    
    def chat(self, message: str, context: Optional[list] = None) -> str:
        """Processa mensagem com AI"""
        
        system_prompt = """Você é o CherifeBot, um assistente AI 24/7 profissional. 
        Você ajuda com automação, pesquisa, programação, análise de dados, 
        gerenciamento de tarefas e muito mais.
        
        Seja direto, útil e proativo. Ofereça soluções práticas.
        Use formatação Markdown para melhor legibilidade."""
        
        if self.provider == "openai":
            messages = [{"role": "system", "content": system_prompt}]
            if context:
                messages.extend(context)
            messages.append({"role": "user", "content": message})
            
            response = openai.ChatCompletion.create(
                model=self.model,
                messages=messages,
                temperature=0.7,
                max_tokens=1500
            )
            return response.choices[0].message.content
            
        elif self.provider == "claude":
            messages = []
            if context:
                for msg in context:
                    messages.append({
                        "role": msg["role"],
                        "content": msg["content"]
                    })
            
            message_obj = self.client.messages.create(
                model=self.model,
                max_tokens=2000,
                temperature=0.7,
                system=system_prompt,
                messages=[
                    {"role": "user", "content": message}
                ]
            )
            return message_obj.content[0].text
    
    def summarize(self, text: str, max_length: int = 300) -> str:
        """Resume texto"""
        prompt = f"Resuma o seguinte texto em {max_length} caracteres:\n\n{text}"
        return self.chat(prompt)
    
    def translate(self, text: str, target_lang: str = "português") -> str:
        """Traduz texto"""
        prompt = f"Traduza para {target_lang}:\n\n{text}"
        return self.chat(prompt)
    
    def code_analysis(self, code: str, language: str) -> str:
        """Analisa código"""
        prompt = f"Analise este código {language} e forneça:\n1. Funcionalidade\n2. Possíveis melhorias\n3. Bugs potenciais\n\nCódigo:\n```{language}\n{code}\n```"
        return self.chat(prompt)
