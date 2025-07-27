// import ReactMarkdown from "react-markdown";
// import { useState, useRef } from "react";
// import {
//   Box,
//   Button,
//   TextField,
//   IconButton,
//   List,
//   ListItem,
//   Typography,
//   Avatar,
//   Paper,
//   InputAdornment,
//   Select,
//   MenuItem,
// } from "@mui/material";
// import AttachFileIcon from "@mui/icons-material/AttachFile";
// import SendIcon from "@mui/icons-material/Send";
// import Sidebar from "./components/Sidebar";
// import axios from "axios";

// const API_URLS = {
//   ai: "http://localhost:8001/general_chat/",
//   sql: "http://localhost:8001/sql_bot/",
//   course: "http://localhost:8001/course_builder/",
//   image: "http://localhost:8001/image_analyzer/",
// };

// const modelOptions = [
//   "llama3.2:latest",
//   "tinyllama:latest",
//   "llama3.2-vision:11b",
//   "llama3.2:1b",
// ];

// export default function ChatUI() {
//   const [selectedAgent, setSelectedAgent] = useState("ai");
//   const [selectedModel, setSelectedModel] = useState("llama3.2:latest");
//   const [messages, setMessages] = useState([]);
//   const [input, setInput] = useState("");
//   const [loading, setLoading] = useState(false);
//   const [file, setFile] = useState(null);
//   const fileInputRef = useRef();

//   const handleSend = async () => {
//     if (!input && !file) return;

//     const newMessage = { role: "user", content: input || file?.name };
//     setMessages((prev) => [...prev, newMessage]);
//     setInput("");
//     setLoading(true);

//     let response;
//     const session_id = "demo_session";

//     try {
//       if (selectedAgent === "course" || selectedAgent === "image") {
//         const formData = new FormData();
//         formData.append("file", file);
//         formData.append("session_id", session_id);
//         formData.append("model", selectedModel); // send model to backend
//         response = await axios.post(API_URLS[selectedAgent], formData);
//         setFile(null);
//       } else {
//         response = await axios.post(API_URLS[selectedAgent], {
//           prompt: input,
//           session_id,
//           model: selectedModel, // send model to backend
//         });
//       }

//       const rawReply = response.data;
//       const botReply =
//         typeof rawReply === "object" && rawReply.output
//           ? rawReply.output
//           : JSON.stringify(rawReply, null, 2);

//       setMessages((prev) => [...prev, { role: "bot", content: botReply }]);
//     } catch (err) {
//       console.error("❌ API error:", err);
//       setMessages((prev) => [
//         ...prev,
//         { role: "bot", content: "Something went wrong." },
//       ]);
//     } finally {
//       setLoading(false);
//     }
//   };

//   return (
//     <Box display="flex" height="100vh">
//       <Sidebar selectedAgent={selectedAgent} setSelectedAgent={setSelectedAgent} />

//       <Box flex={1} display="flex" flexDirection="column" p={3}>
//         <Box textAlign="center" mb={2}>
//           <Avatar sx={{ bgcolor: "#d1c4e9", width: 48, height: 48, mx: "auto" }}>
//             🤝
//           </Avatar>
//           <Typography variant="h6" mt={1}>
//             Welcome to {selectedAgent.charAt(0).toUpperCase() + selectedAgent.slice(1)} Assistant
//           </Typography>
//           <Typography variant="body2" color="textSecondary">
//             How can I assist you today?
//           </Typography>
//         </Box>

//         <Box flex={1} overflow="auto" mb={2}>
//           <List>
//             {messages.map((msg, i) => (
//               <ListItem key={i}>
//                 <Paper
//                   elevation={2}
//                   sx={{ p: 1, bgcolor: msg.role === "user" ? "#e3f2fd" : "#ede7f6" }}
//                 >
//                   <ReactMarkdown>{msg.content}</ReactMarkdown>
//                 </Paper>
//               </ListItem>
//             ))}
//             {loading && (
//               <ListItem>
//                 <Paper elevation={2} sx={{ p: 1, bgcolor: "#ede7f6", fontStyle: "italic" }}>
//                   <Typography variant="body2">🤖 Bot is thinking...</Typography>
//                 </Paper>
//               </ListItem>
//             )}
//           </List>
//         </Box>

//         <Box display="flex" alignItems="center" gap={1}>
//           <input
//             type="file"
//             hidden
//             ref={fileInputRef}
//             onChange={(e) => setFile(e.target.files[0])}
//           />
//           <IconButton onClick={() => fileInputRef.current.click()}>
//             <AttachFileIcon />
//           </IconButton>

//           <TextField
//             fullWidth
//             variant="outlined"
//             placeholder={`Ask ${selectedAgent} anything...`}
//             value={input}
//             onChange={(e) => setInput(e.target.value)}
//             onKeyDown={(e) => e.key === "Enter" && handleSend()}
//             InputProps={{
//               startAdornment: (
//                 <InputAdornment position="start">
//                   <Select
//                     value={selectedModel}
//                     onChange={(e) => setSelectedModel(e.target.value)}
//                     size="small"
//                     sx={{ minWidth: 180 }}
//                   >
//                     {modelOptions.map((model) => (
//                       <MenuItem key={model} value={model}>
//                         {model}
//                       </MenuItem>
//                     ))}
//                   </Select>
//                 </InputAdornment>
//               ),
//             }}
//           />

//           <IconButton color="primary" onClick={handleSend}>
//             <SendIcon />
//           </IconButton>
//         </Box>

//         {file && (
//           <Box mt={1} display="flex" alignItems="center" gap={2}>
//             <Typography variant="body2" color="textSecondary">
//               📎 Attached: {file.name}
//             </Typography>
//             {file.type.startsWith("image/") && (
//               <img
//                 src={URL.createObjectURL(file)}
//                 alt="preview"
//                 style={{ width: 60, height: 60, objectFit: "cover", borderRadius: 4 }}
//               />
//             )}
//           </Box>
//         )}
//       </Box>
//     </Box>
//   );
// }
import ReactMarkdown from "react-markdown";
import { useState, useRef } from "react";
import {
  Box,
  Button,
  TextField,
  IconButton,
  List,
  ListItem,
  Typography,
  Avatar,
  Paper,
} from "@mui/material";
import AttachFileIcon from "@mui/icons-material/AttachFile";
import SendIcon from "@mui/icons-material/Send";
import  Sidebar  from "./components/Sidebar"
import axios from "axios";

const API_URLS = {
  ai: "http://localhost:8000/general_chat/",
  sql: "http://localhost:8000/sql_bot/",
  course: "http://localhost:8000/course_builder/",
  image: "http://localhost:8001/image_analyzer/",
};

export default function ChatUI() {
  const [selectedAgent, setSelectedAgent] = useState("ai");
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState("");
  const [loading, setLoading] = useState(false);
  const [file, setFile] = useState(null);
  const fileInputRef = useRef();

  const handleSend = async () => {
    if (!input && !file) return;
  
    const newMessage = { role: "user", content: input || file?.name };
    setMessages((prev) => [...prev, newMessage]);
    setInput("");
    setLoading(true); // Start loading
  
    let response;
    const session_id = "demo_session";
  
    try {
      if (selectedAgent === "course" || selectedAgent === "image") {
        const formData = new FormData();
        formData.append("file", file);
        formData.append("session_id", session_id);
        response = await axios.post(API_URLS[selectedAgent], formData);
        setFile(null);
      } else {
        response = await axios.post(API_URLS[selectedAgent], {
          prompt: input,
          session_id,
        });
      }
  
      const rawReply = response.data;
      const botReply =
        typeof rawReply === "object" && rawReply.output
          ? rawReply.output
          : JSON.stringify(rawReply, null, 2);
  
      setMessages((prev) => [...prev, { role: "bot", content: botReply }]);
    } catch (err) {
      console.error("❌ API error:", err);
      setMessages((prev) => [
        ...prev,
        { role: "bot", content: "Something went wrong." },
      ]);
    } finally {
      setLoading(false); // Stop loading
    }
  };

  
  return (
    <Box display="flex" height="100vh">
      <Sidebar selectedAgent={selectedAgent} setSelectedAgent={setSelectedAgent} />

      <Box flex={1} display="flex" flexDirection="column" p={3}>
        <Box textAlign="center" mb={2}>
          <Avatar sx={{ bgcolor: "#d1c4e9", width: 48, height: 48, mx: "auto" }}>
            🤝
          </Avatar>
          <Typography variant="h6" mt={1}>Welcome to {selectedAgent.charAt(0).toUpperCase() + selectedAgent.slice(1)} Assistant</Typography>
          <Typography variant="body2" color="textSecondary">How can I assist you today?</Typography>
        </Box>

        <Box flex={1} overflow="auto" mb={2}>
        <List>
  {messages.map((msg, i) => (
   <ListItem key={i} sx={{ justifyContent: msg.role === "user" ? "flex-start" : "flex-end" }}>
   <Paper
     elevation={2}
     sx={{
       p: 1.5,
       maxWidth: "100%",
       bgcolor: msg.role === "user" ? "#e3f2fd" : "#ede7f6",
       borderRadius: 2,
     }}
   >
     <ReactMarkdown>{msg.content}</ReactMarkdown>
     {/* <pre style={{ whiteSpace: "pre-wrap", wordBreak: "break-word" }}>
      {msg.content}
      </pre>
      -------for json----------
      <pre style={{ backgroundColor: "#f6f8fa", padding: "12px", borderRadius: "6px" }}>
        {JSON.stringify(JSON.parse(msg.content), null, 2)}
      </pre> */}


   </Paper>
 </ListItem>
 
  ))}
  
  {loading && (
    <ListItem>
      <Paper elevation={2} sx={{ p: 1, bgcolor: "#ede7f6", fontStyle: 'italic' }}>
        <Typography variant="body2">🤖 Bot is thinking...</Typography>
      </Paper>
    </ListItem>
  )}
</List>

        </Box>

        <Box display="flex" alignItems="center" gap={1}>
          <input
            type="file"
            hidden
            ref={fileInputRef}
            onChange={(e) => setFile(e.target.files[0])}
          />
          <IconButton onClick={() => fileInputRef.current.click()}>
            <AttachFileIcon />
          </IconButton>
          <TextField
            fullWidth
            variant="outlined"
            placeholder={`Ask ${selectedAgent} anything...`}
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyDown={(e) => e.key === "Enter" && handleSend()}
          />
          <IconButton color="primary" onClick={handleSend}>
            <SendIcon />
          </IconButton>
        </Box>

        {file && (
  <Box mt={1} display="flex" alignItems="center" gap={2} >
    <Typography variant="body2" color="textSecondary">
      📎 Attached: {file.name}
    </Typography>
    {file.type.startsWith("image/") && (
      <img
        src={URL.createObjectURL(file)}
        alt="preview"
        style={{ width: 60, height: 60, objectFit: "cover", borderRadius: 4 }}
      />
    )}
  </Box>
)}
      </Box>
    </Box>
  );
}