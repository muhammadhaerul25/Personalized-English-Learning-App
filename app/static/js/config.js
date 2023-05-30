// Time
const placementTestTime = 10 * 60 * 1000; // 10 minutes
const breakTestTime = 10 * 1000 // 10 seconds
const textSpanCountdown = breakTestTime/1000; 
const defaultMode = 'pronunciation';

const pronunciationDropdownOptions = `
  <option value="">Select a message</option>
  <option value="Introduce yourself and explain what you do">Introduce yourself and explain what you do</option>
  <option value="Assess my English level and suggest improvements">Assess my English level and suggest improvements</option>
  <option value="Recall what I learned last time">Recall what I learned last time</option>
  <option value="Learn about a specific topic (e.g., hobbies, travel)...">Learn about a specific topic (e.g., hobbies, travel)...</option>
  <option value="Request a lesson on a topic (e.g., food, technology)...">Request a lesson on a topic (e.g., food, technology)...</option>
  <option value="Engage in a conversation about a general topic...">Engage in a conversation about a general topic...</option>
  <option value="Have a conversation with vocabulary suggestions...">Have a conversation with vocabulary suggestions...</option>
  <option value="Have a conversation with error corrections...">Have a conversation with error corrections...</option>
  <option value="Write a conversation about a specific topic (e.g., family, sports)...">Write a conversation about a specific topic (e.g., family, sports)...</option>
  <option value="Write a conversation between two people (e.g., ordering food, planning an outing)...">Write a conversation between two people (e.g., ordering food, planning an outing)...</option>
  <option value="Simulate a job interview for a specific role (e.g., customer service, sales)...">Simulate a job interview for a specific role (e.g., customer service, sales)...</option>
  <option value="Practice pronunciation, speaking, and conversation skills. You will give me one question at a time, and I will answer it. Then, you can grade my answer and move on to another question">Practice pronunciation, speaking, and conversation skills</option>
  <option value="Request feedback on my performance">Request feedback on my performance</option>
  <option value="Explain it in Indonesian">Explain it in Indonesian</option>
`;


const contextDropdownOptions = `
  <option value="">Select a message</option>
  <option value="Introduce yourself and explain what you do">Introduce yourself and explain what you do</option>
  <option value="Assess my English level and suggest improvements">Assess my English level and suggest improvements</option>
  <option value="Recall what I learned last time">Recall what I learned last time</option>
  <option value="I want to learn about a specific topic (e.g., hobbies, travel)...">I want to learn about a specific topic (e.g., hobbies, travel)...</option>
  <option value="Give me a lesson about a specific topic (e.g., food, technology)...">Give me a lesson about a specific topic (e.g., food, technology)...</option>
  <option value="Explain about a particular subject or concept...">Explain about a particular subject or concept...</option>
  <option value="What is the meaning of a certain word or phrase...">What is the meaning of a certain word or phrase...</option>
  <option value="Write sentences using specific vocabulary or grammar structures...">Write sentences using specific vocabulary or grammar structures...</option>
  <option value="Correct my grammar mistakes in the following text: ...">Correct my grammar mistakes in the following text: ...</option>
  <option value="Practice using context, vocabulary, and grammar.  You will give me one question at a time, and I will answer it. Then, you can grade my answer and move on to another question">Practice using context, vocabulary, and grammar</option>
  <option value="Request feedback on my performance">Request feedback on my performance</option>
  <option value="Explain it in Indonesian">Explain it in Indonesian</option>
`;


const readingDropdownOptions = `
  <option value="">Select a message</option>
  <option value="Explain who you are and what you can do">Explain who you are and what you can do</option>
  <option value="Assess my English level and suggest improvements">Assess my English level and suggest improvements</option>
  <option value="Recall what I learned last time">Recall what I learned last time</option>
  <option value="I want to learn about a specific topic (e.g., hobbies, travel)...">I want to learn about a specific topic (e.g., hobbies, travel)...</option>
  <option value="Give me a lesson about a specific topic (e.g., food, technology)...">Give me a lesson about a specific topic (e.g., food, technology)...</option>
  <option value="Write a text about a given topic...">Write a text about a given topic...</option>
  <option value="Explain this text: ...">Explain this text: ...</option>
  <option value="Simplify this text: ...">Simplify this text: ...</option>
  <option value="Beautify this text: ...">Beautify this text: ...</option>
  <option value="Summarize this text: ...">Summarize this text: ...</option>
  <option value="Conclude this text: ...">Conclude this text: ...</option>
  <option value="Practice reading and writing skills. You will give me one question at a time, and I will answer it. Then, you can grade my answer and move on to another question">Practice reading and writing skills</option>
  <option value="Request feedback on my performance">Request feedback on my performance</option>
  <option value="Explain it in Indonesian">Explain it in Indonesian</option>
`;


//Export
export {
    breakTestTime,
    contextDropdownOptions,
    defaultMode,
    placementTestTime,
    pronunciationDropdownOptions,
    readingDropdownOptions,
    textSpanCountdown
  };
  