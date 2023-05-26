// Time
const placementTestTime = 10 * 60 * 1000; // 10 minutes
const breakTestTime = 10 * 1000 // 10 seconds
const textSpanCountdown = breakTestTime/1000; 
const defaultMode = 'pronunciation';

const pronunciationDropdownOptions = `
  <option value="">Select a prompt</option>
  <option value="Explain who are you and what can you do?">Explain who are you and what can you do?</option>
  <option value="Explain my English level and how can I improve it">Explain my English level and how can I improve it</option>
  <option value="Recall what I learned last time">Recall what I learned last time</option>
  <option value="I want to learn about ...">I want to learn about ...</option>
  <option value="Give me lesson about...">Give me lesson about ...</option>
  <option value="Let's have a conversation about ...">Let's have a conversation about ...</option>
  <option value="Let's have a conversation about ... and suggest different vocabularies">Let's have a conversation about ... and suggest different vocabularies</option>
  <option value="Let's have a conversation about ... and correct my mistakes">Let's have a conversation about ... and correct my mistakes</option>
  <option value="Write a conversation about ...">Write a conversation about ...</option>
  <option value="Write a conversation between ...">Write a conversation between ...</option>
  <option value="Let's simulate an interview for">Let's simulate a interview for</option>
  <option value="Let's practice for pronunciation, speaking, and conversation. You will give me a question by question and I will answer it, then grade my answer and move to another questions">Let's practice</option>
  <option value="Give me feedbacks">Give me feedbacks</option>
`;

const contextDropdownOptions = `
  <option value="">Select a prompt</option>
  <option value="Explain who are you and what can you do?">Explain who are you and what can you do?</option>
  <option value="Explain my English level and how can I improve it">Explain my English level and how can I improve it</option>
  <option value="Recall what I learned last time">Recall what I learned last time</option>
  <option value="I want to learn about ...">I want to learn about ...</option>
  <option value="Give me lesson about...">Give me lesson about ...</option>
  <option value="Explain about ...">Explain about ...</option>
  <option value="What is the meaning of ...">What is the meaning of ...</option>
  <option value="Write sentences using ...">Write sentences using ...</option>
  <option value="Correct my grammar mistakes in the following text: ...">Correct my grammar mistakes in the following text: ...</option>
  <option value="Write sentences using ...">Write sentences using ...</option>
  <option value="Let's practice for context, vocabular, and grammar. You will give me a question by question and I will answer it, then grade my answer and move to another questions">Let's practice</option>
  <option value="Give me feedbacks">Give me feedbacks</option>
`;

const readingDropdownOptions = `
  <option value="">Select a prompt</option>
  <option value="Explain who are you and what can you do?">Explain who are you and what can you do?</option>
  <option value="Explain my English level and how can I improve it">Explain my English level and how can I improve it</option>
  <option value="Recall what I learned last time">Recall what I learned last time</option>
  <option value="I want to learn about ...">I want to learn about ...</option>
  <option value="Give me lesson about ...">Give me lesson about ...</option>
  <option value="Write a text about ...">Write a text about ...</option>
  <option value="Explain this text: ...">Explain this text: ...</option>
  <option value="Simplify this text: ...">Simplify this text: ...</option>
  <option value="Beautify this text: ...">Beautify this text: ...</option>
  <option value="Summarize this text: ...">Summarize this text: ...</option>
  <option value="Conclude this text: ...">Conclude this text: ...</option>
  <option value="Let's practice for reading and writing. You will give me a question by question and I will answer it, then grade my answer and move to another questions">Let's practice</option>
  <option value="Give me feedbacks">Give me feedbacks</option>
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
  