# base_agent.rb

# This is a simplified base class for all agents in the system.
# It provides the basic functionality for loading a prompt and "executing" a task.
# In a real implementation, the `execute_task` method would interact with a large language model (LLM).

class BaseAgent
  attr_reader :name

  def initialize(name:, prompt_file:)
    @name = name
    @prompt = File.read(prompt_file)
  end

  def execute_task(task_description, input = nil)
    puts "Agent '#{@name}' is executing task: #{task_description}"

    # In a real implementation, we would construct a detailed prompt
    # and send it to an LLM.
    full_prompt = "#{@prompt}\n\n--- TASK ---\n\n#{task_description}\n"
    full_prompt += "\n--- INPUT ---\n\n#{input}\n" if input

    # Simulate LLM interaction
    simulated_output = "This is a simulated output for the task: '#{task_description}'."

    # Log the task and output
    log_task(task_description, input, simulated_output)

    simulated_output
  end

  private

  def log_task(task_description, input, output)
    # In a real implementation, this would write to the `agent_tasks` table in the database.
    log_entry = <<~LOG
      Timestamp: #{Time.now.utc}
      Agent: #{@name}
      Task: #{task_description}
      Input: #{input}
      Output: #{output}
      ---
    LOG

    # For now, we'll just append to a log file.
    File.open("../memory/agent_tasks.log", "a") do |f|
      f.puts(log_entry)
    end
  end
end
