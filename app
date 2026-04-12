import streamlit as st
from abc import ABC, abstractmethod
from typing import Dict, Type, List

# =============================================================================
# SEZIONE 1: CORE INTERFACES (Clean Architecture)
# =============================================================================

class CodeGenerator(ABC):
    """Interfaccia astratta per i generatori di codice dei produttori."""
    
    @abstractmethod
    def get_features(self) -> Dict[str, List[str]]:
        """Restituisce le opzioni disponibili per questo produttore."""
        pass

    @abstractmethod
    def generate(self, features: dict) -> str:
        """Genera il blocco di codice specifico."""
        pass

# =============================================================================
# SEZIONE 2: IMPLEMENTAZIONE PRODUTTORI (Moduli Indipendenti)
# =============================================================================

class ProducerA(CodeGenerator):
    def get_features(self):
        return {
            "Protocollo": ["MQTT", "HTTP", "WebSocket"],
            "Auth": ["API Key", "OAuth2"],
            "Logging": ["Basic", "Verbose"]
        }

    def generate(self, features: dict) -> str:
        return f"""# Generated for Producer A
import producer_a_sdk

client = producer_a_sdk.Client(
    protocol="{features['Protocollo']}",
    auth_type="{features['Auth']}"
)
# Mode: {features['Logging']}
client.connect()
"""

class ProducerB(CodeGenerator):
    def get_features(self):
        return {
            "DB_Driver": ["PostgreSQL", "MongoDB"],
            "Sync": ["Asyncio", "Threaded"],
            "Encryption": ["AES-256", "RSA"]
        }

    def generate(self, features: dict) -> str:
        return f"""// Generated for Producer B (C++ Style)
#include "producer_b_lib.h"

auto config = ProducerB::Config{{
    .driver = "{features['DB_Driver']}",
    .mode = "{features['Sync']}",
    .security = "{features['Encryption']}"
}};
auto instance = ProducerB::initialize(config);
"""

# =============================================================================
# SEZIONE 3: BACKEND & REGISTRY (Logica di Business)
# =============================================================================

class GeneratorRegistry:
    """Sistema di mapping centrale per evitare if-elif."""
    _generators: Dict[str, CodeGenerator] = {
        "Produttore A": ProducerA(),
        "Produttore B": ProducerB()
    }

    @classmethod
    def get_producers(cls) -> List[str]:
        return list(cls._generators.keys())

    @classmethod
    def get_generator(cls, producer: str) -> CodeGenerator:
        return cls._generators.get(producer)

def generate_code(producer: str, features: dict) -> str:
    """Interfaccia unica (Core Function)."""
    generator = GeneratorRegistry.get_generator(producer)
    if generator:
        return generator.generate(features)
    return "-- Errore: Produttore non trovato --"

# =============================================================================
# SEZIONE 4: INTERFACCIA (Streamlit Frontend)
# =============================================================================

def render_config_column(col_index: int):
    """Renderizza una singola colonna di configurazione."""
    st.subheader(f"Opzione {col_index + 1}")
    
    # 1. Selezione Produttore
    producers = GeneratorRegistry.get_producers()
    selected_prod = st.selectbox(
        f"Seleziona Produttore", 
        producers, 
        key=f"prod_{col_index}"
    )
    
    generator = GeneratorRegistry.get_generator(selected_prod)
    feature_options = generator.get_features()
    user_selections = {}

    # 2. Selezione Dinamica Caratteristiche
    for feature_name, options in feature_options.items():
        user_selections[feature_name] = st.selectbox(
            f"{feature_name}", 
            options, 
            key=f"feat_{feature_name}_{col_index}"
        )

    # 3. Output Codice
    st.markdown("---")
    if st.button(f"Genera Codice {col_index + 1}", key=f"btn_{col_index}", type="primary"):
        code_output = generate_code(selected_prod, user_selections)
        st.code(code_output, language="python" if "A" in selected_prod else "cpp")

def main():
    st.set_page_config(page_title="Code Gen Architect", layout="wide")
    
    st.title("🛠️ Technical Code Generator")
    st.sidebar.header("Global Settings")
    st.sidebar.info("Questo tool segue i principi di Clean Architecture. Aggiungi nuove classi generatore per estendere le funzionalità.")

    # Creazione delle 3 colonne indipendenti
    cols = st.columns(3)
    
    for i, col in enumerate(cols):
        with col:
            with st.container(border=True):
                render_config_column(i)

if __name__ == "__main__":
    main()
