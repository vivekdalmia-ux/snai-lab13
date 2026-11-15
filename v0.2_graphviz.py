import os
import graphviz

def generate_system_architecture():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    output_base = os.path.join(base_dir, "architecture_diagram")

    # Initialize a directed graph with custom visual styling
    dot = graphviz.Digraph(
        name="system_architecture",
        comment="Production Microservices Architecture",
        format="png"
    )

    # Graph-level attributes: Left to Right layout, clean typography
    dot.attr(rankdir="LR", bgcolor="white", fontname="Helvetica")
    dot.attr("node", fontname="Helvetica", fontsize="11", style="filled")
    dot.attr("edge", fontname="Helvetica", fontsize="9", color="#64748b")

    # Define nodes with roles, colors, and shapes
    dot.node("client", "Web Client\n(Browser/App)", shape="box", fillcolor="#e0f2fe", color="#0284c7")
    dot.node("gateway", "API Gateway\n(Reverse Proxy)", shape="hexagon", fillcolor="#fef3c7", color="#d97706")
    dot.node("auth", "Auth Service\n(OAuth2 / JWT)", shape="box", fillcolor="#f3e8ff", color="#9333ea")
    dot.node("api", "Core API Service\n(Business Logic)", shape="box", fillcolor="#dcfce7", color="#16a34a")
    dot.node("db", "Primary Database\n(PostgreSQL)", shape="cylinder", fillcolor="#fee2e2", color="#dc2626")

    # Define connections / data flow
    dot.edge("client", "gateway", label="HTTPS / REST")
    dot.edge("gateway", "auth", label="Verify Token")
    dot.edge("gateway", "api", label="Forward Request")
    dot.edge("api", "db", label="SQL Query")

    # Render diagram to PNG
    output_file = dot.render(output_base, cleanup=True)
    print(f"Graphviz v0.2 rendered: {output_file}")

if __name__ == "__main__":
    generate_system_architecture()
