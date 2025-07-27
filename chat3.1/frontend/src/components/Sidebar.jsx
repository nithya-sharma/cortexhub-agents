import React, { useState } from 'react';
import {
  List,
  ListItemButton,
  ListItemIcon,
  ListItemText,
  Box,
  IconButton,
  Typography
} from '@mui/material';
import SchoolIcon from '@mui/icons-material/School';
import StorageIcon from '@mui/icons-material/Storage';
import ChatIcon from '@mui/icons-material/Chat';
import ImageIcon from '@mui/icons-material/Image';
import PsychologyIcon from '@mui/icons-material/Psychology';
import GroupIcon from '@mui/icons-material/Group';
import MenuIcon from '@mui/icons-material/Menu';

const agents = [
  { key: 'ai', name: 'AI Assistant', icon: <ChatIcon />, description: 'General conversation and assistance', color: "#e5cffd", bc: "#a65ef3" },
  { key: 'course', name: 'Course Builder', icon: <SchoolIcon />, description: 'Create and design educational courses', color: "#c9fae0",  bc: "#7ef7b6" },
  { key: 'sql', name: 'SQL Bot', icon: <StorageIcon />, description: 'Database queries and SQL assistance', color: "#bccbfc", bc: "#7593f7" },
  { key: 'image', name: 'Image Analyzer', icon: <ImageIcon />, description: 'Analyze and describe images', color: "#fce2c2", bc: "#f3b263" },
  // { key: 'ai', name: 'AI Assistant', icon: <PsychologyIcon />, description: 'Advanced AI reasoning and problem solving', color: "#f5c0f7" },
  // { key: 'team', name: 'Team Collaborator', icon: <GroupIcon />, description: 'Team coordination and project management', color: "#c0fcf9" },
];

const Sidebar = ({ selectedAgent, setSelectedAgent, setMessages }) => {
  const [isOpen, setIsOpen] = useState(true);

  return (
    <Box
      sx={{
        width: isOpen ? 260 : 65,
        height: '100vh',
        borderRight: '1px solid #e0e0e0',
        bgcolor: '#f9f9fc',
        transition: 'width 0.3s ease',
        position: 'relative',
        p: isOpen ? 2 : 1,
        boxSizing: 'border-box'
      }}
    >
      {/* Toggle Button */}
      <IconButton
        onClick={() => setIsOpen(!isOpen)}
        sx={{
          position: 'absolute',
          top: 12,
          right: isOpen ? 8 : 12,
          zIndex: 10,
          bgcolor: '#fff',
          border: '1px solid #ddd',
        }}
      >
        <MenuIcon />
      </IconButton>

      {isOpen && (
        <>
          <Box sx={{ fontWeight: 600, fontSize: '1.1rem', mb: 1.2 }}>🧠 AI Assistants</Box>
          <Typography sx={{ fontSize: '0.8rem', color: '#888', mb: 2 }}>
            Choose your specialized assistant
          </Typography>
        </>
      )}

      {/* 🛠 Add top margin to push below the Menu button */}
      <List sx={{ mt: isOpen ? 0 : 6 }}>
        {agents.map((agent) => (
          <ListItemButton
            key={agent.key}
            selected={selectedAgent === agent.key}
            onClick={() => setSelectedAgent(agent.key)}
            sx={{
              mb: 1,
              borderRadius: '10px',
              alignItems: 'flex-start',
              padding: 1.5,
              bgcolor: selectedAgent === agent.key ? `${agent.color} !important` : "transparent",
              border: selectedAgent === agent.key ? `2px solid ${agent.bc}` : "1px solid #e5e7eb",
              boxShadow: selectedAgent === agent.key ? "0 2px 6px rgba(0,0,0,0.1)" : "none",
              transition: "all 0.3s ease",
            }}
          >
            <ListItemIcon sx={{ mt: '4px', minWidth: isOpen ? 40 : 32 }}>
              {agent.icon}
            </ListItemIcon>
            {isOpen && (
              <ListItemText
                primary={agent.name}
                secondary={agent.description}
                primaryTypographyProps={{ fontWeight: 500 }}
                secondaryTypographyProps={{ fontSize: '0.75rem' }}
              />
            )}
          </ListItemButton>
        ))}
      </List>
    </Box>
  );
};

export default Sidebar;
