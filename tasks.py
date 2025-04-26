from crewai import Task
from agents import research_agent,answer_drafter_agent
from tools import tool

# Task for the Research Agent
research_task = Task(
    description=(
        "Conduct thorough research to find reliable and up-to-date information about the given user query: "
        "'{{ input }}'. Use TavilySearchTool to search the web and summarize findings concisely. "
        "Focus on collecting facts, insights, and real-world examples that would be helpful to a professional audience."
    ),
    tools=[tool],
    expected_output=(
        "A detailed bullet-point summary of key findings from trusted sources. Include citations or links where applicable."
    ),
    
    agent=research_agent,
    async_execution=True
)

# Task for the Answer Drafter Agent
draft_task = Task(
    description=(
        """Transform the research findings into a comprehensive, executive-level response that directly addresses the original question: '{{ input }}'. Craft your answer with:

1. **Strategic Structure**:
   - Opening paragraph with clear thesis statement
   - 2-3 body paragraphs with supporting evidence
   - Conclusion with actionable recommendations

2. **Professional Qualities**:
   - Maintain an authoritative yet accessible tone
   - Use precise terminology where appropriate
   - Include relevant data points with context
   - Anticipate and address potential follow-up questions

3. **Actionable Formatting**:
   - Begin with a 1-sentence key takeaway (bolded)
   - Use bullet points for multi-step recommendations
   - Highlight critical insights using italics
   - Include potential implementation considerations

4. **Quality Standards**:
   - Eliminate jargon without oversimplifying
   - Balance depth with readability
   - Connect findings to real-world applications
   - Flag any limitations or uncertainties

The response should be immediately useful to decision-makers while maintaining academic rigor. Prioritize novel insights over mere information aggregation."""
    ),
    expected_output=(
        """Produce a comprehensive, professional-grade synthesis that:

Opens with a clear, engaging thesis statement capturing the core insight

Organizes findings into logical sections with smooth transitions

Integrates multiple perspectives from the research with balanced analysis

Supports key points with relevant evidence and examples

Maintains an authoritative yet accessible academic tone

Concludes with actionable insights or thought-provoking implications

Adheres to professional formatting standards (paragraph structure, proper citations if applicable)

The response should demonstrate:

Depth of critical thinking beyond surface-level summary

Nuanced understanding of complex relationships between findings

Appropriate technical terminology where warranted

Elimination of redundancy while preserving key information

Fluent, publication-quality writing suitable for business or academic contexts"""
    ),
    agent=answer_drafter_agent,
    async_execution=False,
    output_file="final_answer.txt"
)