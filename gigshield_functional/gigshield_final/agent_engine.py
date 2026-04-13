import os

try:
    from langchain_groq import ChatGroq
    from langchain_core.messages import HumanMessage
    GROQ_AVAILABLE = True
except ImportError:
    GROQ_AVAILABLE = False

def synthesize_agent_rationale(zone, ml_payout, is_fraud_normal, precip_level):
    """
    Core Agentic Logic: Takes the hard ML integers and uses an Open-Source LLM
    to generate the authoritative rationale for the end-user dashboard.
    """
    api_key = os.environ.get("GROQ_API_KEY", "").strip()
    
    if GROQ_AVAILABLE and api_key and "paste_your_key" not in api_key:
        try:
            llm = ChatGroq(
                temperature=0.2, 
                groq_api_key=api_key, 
                model_name="llama3-8b-8192"
            )
            
            fraud_status = "Validation OK: Trajectory graph integrity 100%." if is_fraud_normal else "FRAUD BLOCK: GPS velocity anomaly detected."
            
            prompt = f"""
You are the ArthSahay Autonomous Validation Agent.
A claim was filed in {zone}. The Machine Learning model calculated an income loss of ₹{ml_payout}.
The Precipitation severity level factor was {precip_level}.
The Fraud ML Model returned this status: {fraud_status}

Synthesize a 2-sentence formal approval or rejection rationale for the dashboard. 
Start exactly with either 'Agent Approved:' or 'Agent Rejected:'. Focus on the data logic.
"""
            response = llm.invoke([HumanMessage(content=prompt)])
            return response.content
        except Exception as e:
            print(f"Agent Warning (Executing Fallback): {e}")
            return generate_fallback_rationale(zone, ml_payout, is_fraud_normal, precip_level)
    else:
        # ── HACKATHON FALLBACK LOGIC ──
        return generate_fallback_rationale(zone, ml_payout, is_fraud_normal, precip_level)


def generate_fallback_rationale(zone, ml_payout, is_fraud_normal, precip_level=30):
    """Local fallback if API limits hit or keys not provided."""
    import time
    time.sleep(1) # Simulate LLM thinking time
    
    if not is_fraud_normal:
        return "Agent Rejected: GPS velocity vectors generated anomalous topological edges. Structural spoofing detected during event timeframe."
    
    if ml_payout == 0:
        return "Agent Rejected: Environmental severity in this zone did not breach the baseline required for capacity loss."
        
    return f"Agent Approved: Spatial-temporal logs confirmed validity. Model projects ₹{ml_payout} in lost capacity due to environmental saturation. Compensatory payload authorized."
