import { useEffect, useRef, useState } from 'react';
import './App.css';

// Real API functions
const API_BASE_URL = 'http://127.0.0.1:8080';
const TIME_ZONE = 'Asia/Singapore';

const api = {
  login: async (identifier, password) => {
    console.log('Frontend login API called with:', { identifier, password: password ? '***' : 'empty' });
    
    const response = await fetch(`${API_BASE_URL}/api/v1/auth/login`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ identifier, password }),
    });

    console.log('Login response status:', response.status);
    console.log('Login response ok:', response.ok);

    if (!response.ok) {
      const error = await response.json();
      console.error('Login error response:', error);
      throw new Error(error.error || 'Login failed');
    }

    const result = await response.json();
    console.log('Login success response:', result);
    return result;
  },

  register: async (userData) => {
    console.log('Frontend register API called with:', { 
      username: userData.username,
      email: userData.email,
      age: userData.age,
      nationality: userData.nationality,
      gender: userData.gender,
      hobbies: userData.hobbies,
      password: userData.password ? '***' : 'empty'
    });
    
    const response = await fetch(`${API_BASE_URL}/api/v1/auth/register`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(userData),
    });

    console.log('Register response status:', response.status);
    console.log('Register response ok:', response.ok);

    if (!response.ok) {
      const error = await response.json();
      console.error('Register error response:', error);
      throw new Error(error.error || 'Registration failed');
    }

    const result = await response.json();
    console.log('Register success response:', result);
    return result;
  },

  logMood: async (moodData, token) => {
    const response = await fetch(`${API_BASE_URL}/api/v1/mood/mood`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        Authorization: `Bearer ${token}`,
      },
      body: JSON.stringify(moodData),
    });

    if (!response.ok) {
      const error = await response.json();
      if (response.status === 401) {
        throw new Error('Unauthorized: Invalid or expired token');
      }
      throw new Error(error.error || 'Failed to log mood');
    }

    return await response.json();
  },

  getRecommendation: async (moodData, token) => {
    console.log('API getRecommendation called with:', { moodData, token: token ? 'present' : 'missing' });
    
    const response = await fetch(`${API_BASE_URL}/api/v1/mood/recommend`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        Authorization: `Bearer ${token}`,
      },
      body: JSON.stringify(moodData),
    });

    console.log('API response status:', response.status);
    console.log('API response ok:', response.ok);

    if (!response.ok) {
      const error = await response.json();
      console.error('API error response:', error);
      if (response.status === 401) {
        throw new Error('Unauthorized: Invalid or expired token');
      }
      throw new Error(error.error || 'Failed to get recommendations');
    }

    const result = await response.json();
    console.log('API success response:', result);
    return result;
  },

  getMoodHistory: async (token) => {
    const response = await fetch(`${API_BASE_URL}/api/v1/mood/mood`, {
      method: 'GET',
      headers: {
        Authorization: `Bearer ${token}`,
      },
    });

    if (!response.ok) {
      const error = await response.json();
      throw new Error(error.error || 'Failed to get mood history');
    }

    return await response.json();
  },

  getCommunityPosts: async (token) => {
    const response = await fetch(`${API_BASE_URL}/api/v1/community/posts`, {
      method: 'GET',
      headers: {
        Authorization: `Bearer ${token}`,
      },
    });

    if (!response.ok) {
      const error = await response.json();
      throw new Error(error.error || 'Failed to get community posts');
    }

    return await response.json();
  },

  createConversation: async (otherUserId, token) => {
    const response = await fetch(`${API_BASE_URL}/api/v1/community/conversations`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        Authorization: `Bearer ${token}`,
      },
      body: JSON.stringify({ other_user_id: otherUserId }),
    });

    if (!response.ok) {
      const error = await response.json();
      throw new Error(error.error || 'Failed to create conversation');
    }

    return await response.json();
  },

  getConversationMessages: async (conversationId, token, since) => {
    const query = since ? `?since=${encodeURIComponent(since)}` : '';
    const response = await fetch(
      `${API_BASE_URL}/api/v1/community/conversations/${conversationId}/messages${query}`,
      {
        method: 'GET',
        headers: {
          Authorization: `Bearer ${token}`,
        },
      },
    );

    if (!response.ok) {
      const error = await response.json();
      throw new Error(error.error || 'Failed to load messages');
    }

    return await response.json();
  },

  getConversations: async (token) => {
    const response = await fetch(`${API_BASE_URL}/api/v1/community/conversations`, {
      method: 'GET',
      headers: {
        Authorization: `Bearer ${token}`,
      },
    });

    if (!response.ok) {
      const error = await response.json();
      throw new Error(error.error || 'Failed to load conversations');
    }

    return await response.json();
  },

  sendConversationMessage: async (conversationId, text, clientId, token) => {
    const response = await fetch(
      `${API_BASE_URL}/api/v1/community/conversations/${conversationId}/messages`,
      {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          Authorization: `Bearer ${token}`,
        },
        body: JSON.stringify({ text, client_id: clientId }),
      },
    );

    if (!response.ok) {
      const error = await response.json();
      throw new Error(error.error || 'Failed to send message');
    }

    return await response.json();
  },

  chatSupport: async (payload, token) => {
    const response = await fetch(`${API_BASE_URL}/api/v1/mood/chat`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        Authorization: `Bearer ${token}`,
      },
      body: JSON.stringify(payload),
    });

    if (!response.ok) {
      const error = await response.json();
      throw new Error(error.error || 'Failed to run AI support');
    }

    return await response.json();
  },

  getPostComments: async (postId, token) => {
    const response = await fetch(`${API_BASE_URL}/api/v1/community/posts/${postId}/comments`, {
      method: 'GET',
      headers: {
        Authorization: `Bearer ${token}`,
      },
    });

    if (!response.ok) {
      const error = await response.json();
      throw new Error(error.error || 'Failed to get comments');
    }

    return await response.json();
  },

  addPostComment: async (postId, commentData, token) => {
    const response = await fetch(`${API_BASE_URL}/api/v1/community/posts/${postId}/comments`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        Authorization: `Bearer ${token}`,
      },
      body: JSON.stringify(commentData),
    });

    if (!response.ok) {
      const error = await response.json();
      throw new Error(error.error || 'Failed to add comment');
    }

    return await response.json();
  },

  likePost: async (postId, token) => {
    const response = await fetch(
      `${API_BASE_URL}/api/v1/community/posts/${postId}/like`,
      {
        method: 'POST',
        headers: {
          Authorization: `Bearer ${token}`,
        },
      },
    );

    if (!response.ok) {
      const error = await response.json();
      throw new Error(error.error || 'Failed to like post');
    }

    return await response.json();
  },

  starPost: async (postId, token) => {
    const response = await fetch(
      `${API_BASE_URL}/api/v1/community/posts/${postId}/star`,
      {
        method: 'POST',
        headers: {
          Authorization: `Bearer ${token}`,
        },
      },
    );

    if (!response.ok) {
      const error = await response.json();
      throw new Error(error.error || 'Failed to star post');
    }

    return await response.json();
  },

  shareRecommendation: async (shareData, token) => {
    const response = await fetch(`${API_BASE_URL}/api/v1/mood/share`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        Authorization: `Bearer ${token}`,
      },
      body: JSON.stringify(shareData),
    });

    if (!response.ok) {
      const error = await response.json();
      throw new Error(error.error || 'Failed to share recommendation');
    }

    return await response.json();
  },

  shareAIRecommendation: async (shareData, token) => {
    console.log('API shareAIRecommendation called with:', shareData);
    
    const response = await fetch(`${API_BASE_URL}/api/v1/mood/share-ai-recommendation`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        Authorization: `Bearer ${token}`,
      },
      body: JSON.stringify(shareData),
    });

    console.log('Share AI API response status:', response.status);
    console.log('Share AI API response ok:', response.ok);

    if (!response.ok) {
      const error = await response.json();
      console.error('Share AI API error response:', error);
      throw new Error(error.error || 'Failed to share AI recommendation');
    }

    const result = await response.json();
    console.log('Share AI API success response:', result);
    return result;
  },

  updateProfile: async (token, profileData) => {
    const response = await fetch(`${API_BASE_URL}/api/v1/auth/profile`, {
      method: 'PUT',
      headers: {
        'Content-Type': 'application/json',
        Authorization: `Bearer ${token}`,
      },
      body: JSON.stringify(profileData),
    });

    if (!response.ok) {
      const error = await response.json();
      if (response.status === 401) {
        throw new Error('Unauthorized: Invalid or expired token');
      }
      throw new Error(error.error || 'Failed to update profile');
    }

    return await response.json();
  },

  getUserProfile: async (token) => {
    const response = await fetch(`${API_BASE_URL}/api/v1/auth/profile`, {
      method: 'GET',
      headers: {
        Authorization: `Bearer ${token}`,
      },
    });

    if (!response.ok) {
      const error = await response.json();
      if (response.status === 401) {
        throw new Error('Unauthorized: Invalid or expired token');
      }
      throw new Error(error.error || 'Failed to get user profile');
    }

    return await response.json();
  },

  submitRecommendationFeedback: async (feedbackData, token) => {
    console.log('API submitRecommendationFeedback called with:', feedbackData);
    
    const response = await fetch(
      `${API_BASE_URL}/api/v1/mood/recommendation/feedback`,
      {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          Authorization: `Bearer ${token}`,
        },
        body: JSON.stringify(feedbackData),
      },
    );

    console.log('Feedback API response status:', response.status);
    console.log('Feedback API response ok:', response.ok);

    if (!response.ok) {
      const error = await response.json();
      console.error('Feedback API error response:', error);
      throw new Error(error.error || 'Failed to submit feedback');
    }

    const result = await response.json();
    console.log('Feedback API success response:', result);
    return result;
  },

  submitAIRecommendationFeedback: async (feedbackData, token) => {
    console.log('API submitAIRecommendationFeedback called with:', feedbackData);
    
    const response = await fetch(
      `${API_BASE_URL}/api/v1/mood/ai-recommendation/feedback`,
      {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          Authorization: `Bearer ${token}`,
        },
        body: JSON.stringify(feedbackData),
      },
    );

    console.log('AI Feedback API response status:', response.status);
    console.log('AI Feedback API response ok:', response.ok);

    if (!response.ok) {
      const error = await response.json();
      console.error('AI Feedback API error response:', error);
      throw new Error(error.error || 'Failed to submit AI feedback');
    }

    const result = await response.json();
    console.log('AI Feedback API success response:', result);
    return result;
  },
};

export function App() {
  const [currentView, setCurrentView] = useState('auth');
  const [user, setUser] = useState(() => {
    // Try to restore user from localStorage on app start
    try {
      if (typeof localStorage !== 'undefined') {
        const savedUser = localStorage.getItem('moodJournalUser');
        if (savedUser) {
          const parsedUser = JSON.parse(savedUser);
          console.log('Restored user from localStorage:', parsedUser);
          return parsedUser;
        }
      }
    } catch (error) {
      console.error('Error restoring user from localStorage:', error);
    }
    return null;
  });
  const [isLoading, setIsLoading] = useState(false);
  const [moodEntries, setMoodEntries] = useState([]);
  const [currentRecommendation, setCurrentRecommendation] = useState(null);
  const [communityPosts, setCommunityPosts] = useState([]);
  const [postComments, setPostComments] = useState({});
  const [commentDrafts, setCommentDrafts] = useState({});
  const [activeReplyTargets, setActiveReplyTargets] = useState({});
  const [activeConversationId, setActiveConversationId] = useState(null);
  const [chatMessages, setChatMessages] = useState([]);
  const [chatDraft, setChatDraft] = useState('');
  const [activeConversationPartner, setActiveConversationPartner] = useState(null);
  const [hasUnreadMessages, setHasUnreadMessages] = useState(false);
  const [lastSeenConversations, setLastSeenConversations] = useState({});
  const [aiChatMessages, setAiChatMessages] = useState([]);
  const [aiChatDraft, setAiChatDraft] = useState('');
  const [aiChatLoading, setAiChatLoading] = useState(false);
  const [recommendationList, setRecommendationList] = useState([]);
  const [conversations, setConversations] = useState([]);
  const [isConversationsLoading, setIsConversationsLoading] = useState(false);
  const authModeRef = useRef('login');

  // Auth state
  const [authMode, setAuthMode] = useState('login');
  const [authData, setAuthData] = useState({
    username: '',
    email: '',
    password: '',
    age: null,
    nationality: '',
    gender: '',
    hobbies: [],
    hobbiesInput: '',
  });

  // Mood logging state
  const [moodData, setMoodData] = useState({
    mood: 'happy',
    intensity: 5,
    note: '',
    description: '',
    is_public: false,
  });

  // Calendar state
  const [currentDate, setCurrentDate] = useState(new Date());
  const [selectedDate, setSelectedDate] = useState(null);
  const [calendarMoodEntries, setCalendarMoodEntries] = useState({});
  const [moodLogDate, setMoodLogDate] = useState(new Date()); // Date for logging mood

  // Profile editing state
  const [profileData, setProfileData] = useState({
    username: '',
    age: 25,
    gender: '',
    nationality: '',
    hobbies: []
  });

  // Utility functions
  const getMoodEmoji = (mood) => {
    const emojis = { happy: '😊', sad: '😢', anxious: '😰', excited: '🤩' };
    return emojis[mood] || '😊';
  };

  const getMoodColor = (mood) => {
    const colors = {
      happy: '#FFD700',
      sad: '#87CEEB',
      anxious: '#DDA0DD',
      excited: '#FF6B6B',
    };
    return colors[mood] || '#FFD700';
  };

  const parseServerTimestamp = (value) => {
    if (!value) return null;
    if (value instanceof Date) return value;
    const raw = String(value);
    const hasTimezone = /[zZ]|[+-]\d{2}:?\d{2}$/.test(raw);
    return new Date(hasTimezone ? raw : `${raw}Z`);
  };

  const formatTime = (value) => {
    if (!value) return '';
    const date = parseServerTimestamp(value);
    if (!date) return '';
    return new Intl.DateTimeFormat('en-GB', {
      hour: '2-digit',
      minute: '2-digit',
      second: '2-digit',
      timeZone: TIME_ZONE
    }).format(date);
  };

  const formatDate = (value, options) => {
    if (!value) return '';
    const date = parseServerTimestamp(value);
    if (!date) return '';
    return new Intl.DateTimeFormat('en-US', {
      timeZone: TIME_ZONE,
      ...options
    }).format(date);
  };

  const parseHobbiesInput = (value) => {
    if (!value) return [];
    return value
      .split(',')
      .map((item) => item.trim())
      .filter(Boolean);
  };

  const getMoodEntryKey = (entry) => {
    const primaryId = entry?._id || entry?.id || entry?.mood_id;
    if (primaryId) return String(primaryId);
    const date = entry?.date || entry?.created_at || '';
    return `${date}-${entry?.mood || ''}-${entry?.intensity || ''}-${entry?.description || ''}-${entry?.note || ''}`;
  };

  const dedupeMoodEntries = (entries) => {
    const seen = new Set();
    const unique = [];
    entries.forEach((entry) => {
      const key = getMoodEntryKey(entry);
      if (seen.has(key)) return;
      seen.add(key);
      unique.push(entry);
    });
    return unique;
  };

  const getConversationPartnerName = (convo) => {
    if (!convo) return 'User';
    const participants = convo.participants || [];
    const otherId = participants.find((id) => String(id) !== String(user?.id));
    if (otherId && convo.participant_usernames) {
      return convo.participant_usernames[String(otherId)] || 'User';
    }
    return 'User';
  };

  const isConversationUnread = (convo) => {
    if (!convo?.last_message_at) return false;
    if (convo.last_message_sender_id && String(convo.last_message_sender_id) === String(user?.id)) {
      return false;
    }
    const lastSeen = lastSeenConversations[convo._id];
    if (!lastSeen) return true;
    return new Date(convo.last_message_at) > new Date(lastSeen);
  };

  const getLastSeenKey = (userId) => `moodJournalLastSeen:${userId}`;

  const capitalizeFirst = (str) => {
    return str.charAt(0).toUpperCase() + str.slice(1);
  };

  const formatDateKey = (date) => {
    const dateKey = date.toISOString().split('T')[0];
    console.log('formatDateKey input:', date);
    console.log('formatDateKey output:', dateKey);
    return dateKey;
  };

  const isToday = (date) => {
    const today = new Date();
    return date.toDateString() === today.toDateString();
  };

  const isFutureDate = (date) => {
    const today = new Date();
    today.setHours(23, 59, 59, 999);
    return date > today;
  };

  const hasMoodEntry = (date) => {
    const dateKey = formatDateKey(date);
    return (
      calendarMoodEntries[dateKey] && calendarMoodEntries[dateKey].length > 0
    );
  };

  const getMoodForDate = (date) => {
    const dateKey = formatDateKey(date);
    const entries = calendarMoodEntries[dateKey];
    console.log(`Getting mood for date ${dateKey}:`, entries);
    if (entries && entries.length > 0) {
      const lastMood = entries[entries.length - 1].mood;
      console.log(`Last mood for ${dateKey}:`, lastMood);
      return lastMood;
    }
    return null;
  };

  // Event handlers
  const handleAuth = async () => {
    const mode =
      authModeRef.current === 'register' || authMode === 'register'
        ? 'register'
        : 'login';
    console.log('handleAuth called with authMode:', authMode);
    console.log('authData:', {
      username: authData.username,
      email: authData.email,
      age: authData.age,
      nationality: authData.nationality,
      gender: authData.gender,
      hobbies: authData.hobbies,
      password: authData.password ? '***' : 'empty'
    });

    if (mode === 'register') {
      const username = authData.username.trim();
      const email = authData.email.trim();
      const password = authData.password;
      if (!username || !email || !password) {
        alert('Username, email, and password are required to register.');
        return;
      }
    }
    
    setIsLoading(true);
    try {
      let result =
        mode === 'login'
          ? await api.login(authData.username, authData.password)
          : (() => {
              const { hobbiesInput, ...rest } = authData;
              return api.register({
                ...rest,
                hobbies: parseHobbiesInput(hobbiesInput),
              });
            })();

      if (mode === 'register' && !result?.token) {
        const loginResult = await api.login(authData.username, authData.password);
        result = {
          ...result,
          token: loginResult.token,
          user: {
            ...result.user,
            ...loginResult.user,
          },
        };
      }

      console.log('Authentication successful:', result);
      const userData = { ...result.user, token: result.token };
      setUser(userData);
      
      // Save user to localStorage for persistence
      try {
        if (typeof localStorage !== 'undefined') {
          localStorage.setItem('moodJournalUser', JSON.stringify(userData));
          console.log('User saved to localStorage');
        } else {
          console.log('localStorage not available, skipping save');
        }
      } catch (error) {
        console.error('Error saving user to localStorage:', error);
      }
      
      setCurrentView('main');
      console.log('User state set, view changed to main');
    } catch (error) {
      console.error('Auth error:', error);
      alert('Authentication failed: ' + error.message);
    } finally {
      setIsLoading(false);
    }
  };

  const handleLogout = () => {
    console.log('Logging out user');
    setUser(null);
    setCurrentView('auth');
    setMoodEntries([]);
    setCurrentRecommendation(null);
    setCommunityPosts([]);
    setActiveConversationId(null);
    setChatMessages([]);
    setChatDraft('');
    setHasUnreadMessages(false);
    setLastSeenConversations({});
    
    // Clear localStorage
    try {
      if (typeof localStorage !== 'undefined') {
        localStorage.removeItem('moodJournalUser');
        console.log('User data cleared from localStorage');
        if (user?.id) {
          localStorage.removeItem(getLastSeenKey(user.id));
        }
      }
    } catch (error) {
      console.error('Error clearing user data from localStorage:', error);
    }
  };

  const handleGetRecommendation = async () => {
    console.log('handleGetRecommendation called');
    console.log('Current user:', user);
    console.log('Current moodData:', moodData);
    console.log('Current view:', currentView);
    
    if (!user?.token) {
      console.error('No user token found for recommendations');
      return;
    }

    if (!moodData || !moodData.mood) {
      console.error('No mood data available for recommendations');
      alert('Please log a mood first to get recommendations');
      return;
    }

    setIsLoading(true);
    try {
      console.log('Getting recommendations for mood:', moodData);
      console.log('API call with token:', user.token.substring(0, 20) + '...');
      const result = await api.getRecommendation(moodData, user.token);
      console.log('Recommendations received:', result);

      if (result.recommendation) {
        setCurrentRecommendation(result.recommendation);
        setRecommendationList(result.alternatives || []);
      } else {
        console.log('No recommendation in result');
        alert('No recommendations available');
      }
    } catch (error) {
      console.error('Failed to get recommendations:', error);
      console.error('Error details:', error.message);
      alert('Failed to get recommendations: ' + error.message);
    } finally {
      setIsLoading(false);
    }
  };

  const handleRecommendationFeedback = async (feedback) => {
    console.log('handleRecommendationFeedback called with:', feedback);
    console.log('Current recommendation:', currentRecommendation);
    
    if (!user?.token || !currentRecommendation) {
      console.error('No user token or recommendation for feedback');
      return;
    }

    // For AI-generated recommendations that don't have IDs, we'll use a simpler approach
    if (!currentRecommendation.id && !currentRecommendation._id) {
      console.log('AI recommendation without ID, using simple feedback');
      
      // Store feedback locally or send to a different endpoint
      const feedbackData = {
        recommendation_title: currentRecommendation.title,
        recommendation_type: currentRecommendation.type,
        recommendation_description: currentRecommendation.description,
        liked: feedback === 'like',
        mood: moodData.mood,
        user_id: user.id
      };
      
      console.log('Sending AI feedback data:', feedbackData);
      
      try {
        await api.submitAIRecommendationFeedback(feedbackData, user.token);
        console.log('AI feedback submitted successfully:', feedback);
        alert('Thank you for your feedback! This helps improve future recommendations.');
      } catch (error) {
        console.error('Failed to submit AI feedback:', error);
        console.error('Error details:', error.message);
        alert('Failed to submit feedback: ' + error.message);
      }
      return;
    }

    // For saved recommendations with IDs
    try {
      const feedbackData = {
        recommendation_id: currentRecommendation.id || currentRecommendation._id,
        liked: feedback === 'like', // Convert 'like'/'dislike' to boolean
        mood: moodData.mood // Send just the mood string, not the whole object
      };
      
      console.log('Sending feedback data:', feedbackData);
      
      await api.submitRecommendationFeedback(feedbackData, user.token);
      console.log('Feedback submitted successfully:', feedback);
      alert('Thank you for your feedback!');
    } catch (error) {
      console.error('Failed to submit feedback:', error);
      console.error('Error details:', error.message);
      alert('Failed to submit feedback: ' + error.message);
    }
  };

  const handleShareRecommendation = async () => {
    console.log('handleShareRecommendation called');
    console.log('Current recommendation:', currentRecommendation);
    
    if (!user?.token || !currentRecommendation) {
      console.error('No user token or recommendation for sharing');
      return;
    }

    // For AI-generated recommendations that don't have IDs, use the AI share endpoint
    if (!currentRecommendation.id && !currentRecommendation._id) {
      console.log('AI recommendation without ID, using AI share endpoint');
      
      const shareData = {
        recommendation_title: currentRecommendation.title,
        recommendation_type: currentRecommendation.type,
        recommendation_description: currentRecommendation.description,
        mood_data: moodData,
        description: `I'm feeling ${moodData.mood} and got this recommendation: ${currentRecommendation.title}`
      };
      
      console.log('Sending AI share data:', shareData);
      
      try {
        await api.shareAIRecommendation(shareData, user.token);
        console.log('AI recommendation shared successfully');
        alert('AI recommendation shared to community!');
      } catch (error) {
        console.error('Failed to share AI recommendation:', error);
        console.error('Error details:', error.message);
        alert('Failed to share AI recommendation: ' + error.message);
      }
      return;
    }

    // For saved recommendations with IDs
    try {
      const shareData = {
        recommendation_id: currentRecommendation.id || currentRecommendation._id,
        mood: moodData.mood,
        mood_intensity: moodData.intensity,
        description: `I'm feeling ${moodData.mood} and got this recommendation: ${currentRecommendation.title}`
      };
      
      console.log('Sending share data:', shareData);
      
      await api.shareRecommendation(shareData, user.token);
      console.log('Recommendation shared successfully');
      alert('Recommendation shared to community!');
    } catch (error) {
      console.error('Failed to share recommendation:', error);
      console.error('Error details:', error.message);
      alert('Failed to share recommendation: ' + error.message);
    }
  };

  const handleLogMood = async () => {
    console.log('handleLogMood called');
    console.log('Current user state:', user);
    console.log('Current moodData:', moodData);
    console.log('Current view before logging:', currentView);
    
    if (!user?.token) {
      console.error('No user token found');
      console.log('User state is:', user);
      // Don't redirect to auth if we're already on a different view
      if (currentView !== 'auth') {
        console.log('User lost but staying on current view');
        return;
      }
      return;
    }

    if (isFutureDate(moodLogDate)) {
      alert('You can only log moods for today or earlier.');
      return;
    }

    setIsLoading(true);
    try {
      console.log('Calling API with token:', user.token.substring(0, 20) + '...');
      console.log('Logging mood for date:', moodLogDate);
      
      // Send the selected date to the backend
      const moodDataWithDate = {
        ...moodData,
        date: moodLogDate.toISOString()
      };
      
      const result = await api.logMood(moodDataWithDate, user.token);
      console.log('API call successful, result:', result);

      // Use the date from the API response to ensure consistency
      const apiDate = new Date(result.date);
      const newMoodEntry = {
        id: result.mood_id,
        ...moodData,
        date: result.date, // Use the API response date
      };

      console.log('Created new mood entry:', newMoodEntry);
      console.log('API date:', apiDate);
      console.log('Local date:', new Date());

      setMoodEntries(prev => dedupeMoodEntries([...prev, newMoodEntry]));

      const dateKey = formatDateKey(apiDate);
      console.log('Date key for calendar:', dateKey);
      setCalendarMoodEntries(prev => {
        const existingEntries = prev[dateKey] || [];
        return {
          ...prev,
          [dateKey]: dedupeMoodEntries([...existingEntries, newMoodEntry]),
        };
      });

      console.log('About to set currentView to main');
      setCurrentRecommendation(null);
      setCurrentView('main');
      console.log('View changed to main');
    } catch (error) {
      console.error('Mood logging error:', error);
      console.error('Error message:', error.message);
      
      // Check if it's an authentication error
      if (error.message.includes('Unauthorized') || error.message.includes('Invalid token')) {
        console.log('Authentication error detected, redirecting to login');
        setUser(null);
        setCurrentView('auth');
      } else {
        // For other errors, show an alert or handle differently
        console.log('Non-auth error, showing alert');
        alert('Failed to log mood: ' + error.message);
      }
    } finally {
      setIsLoading(false);
    }
  };

  const loadCommunityPosts = async () => {
    if (!user?.token) return;

    setIsLoading(true);
    try {
      const result = await api.getCommunityPosts(user.token);
      setCommunityPosts(result.posts);
    } catch (error) {
      console.error('Community posts error:', error);
    } finally {
      setIsLoading(false);
    }
  };

  const isPostOwner = (post) => {
    return user?.id && post.user_id === user.id;
  };

  const loadPostComments = async (postId) => {
    if (!user?.token) return;

    try {
      const result = await api.getPostComments(postId, user.token);
      setPostComments(prev => ({
        ...prev,
        [postId]: result.comments || []
      }));
    } catch (error) {
      console.error('Load comments error:', error);
    }
  };

  const handleCommentDraftChange = (postId, value) => {
    setCommentDrafts(prev => ({
      ...prev,
      [postId]: value
    }));
  };

  const handleAddComment = async (post) => {
    if (!user?.token) return;
    const postId = post._id;
    const commentText = (commentDrafts[postId] || '').trim();

    if (!commentText) return;

    const isOwner = isPostOwner(post);
    const threadUserId = isOwner ? activeReplyTargets[postId] : undefined;

    if (isOwner && !threadUserId) {
      alert('Select a thread to reply to.');
      return;
    }

    try {
      await api.addPostComment(
        postId,
        {
          comment: commentText,
          thread_user_id: threadUserId
        },
        user.token
      );

      setCommentDrafts(prev => ({ ...prev, [postId]: '' }));
      await loadPostComments(postId);
    } catch (error) {
      console.error('Add comment error:', error);
      alert('Failed to add reply: ' + error.message);
    }
  };

  const startConversationWithUser = async (otherUserId) => {
    if (!user?.token) return;

    try {
      const result = await api.createConversation(otherUserId, user.token);
      setActiveConversationId(result.conversation_id);
      setChatMessages([]);
      setActiveConversationPartner(otherUserId);
      setHasUnreadMessages(false);
      setCurrentView('chat');
    } catch (error) {
      console.error('Start conversation error:', error);
      alert('Failed to start chat: ' + error.message);
    }
  };

  const handleSendChatMessage = async () => {
    if (!user?.token || !activeConversationId) return;

    const text = chatDraft.trim();
    if (!text) return;

    const clientId = `client-${Date.now()}-${Math.random().toString(16).slice(2)}`;

    const optimisticMessage = {
      _id: `temp-${Date.now()}`,
      sender_id: user.id,
      text,
      created_at: new Date().toISOString(),
      client_id: clientId
    };
    setChatMessages(prev => [...prev, optimisticMessage]);
    setChatDraft('');
    setLastSeenConversations(prev => ({
      ...prev,
      [activeConversationId]: new Date().toISOString()
    }));

    try {
      await api.sendConversationMessage(activeConversationId, text, clientId, user.token);
    } catch (error) {
      console.error('Send chat message error:', error);
      alert('Failed to send message: ' + error.message);
    }
  };

  const handleSendAiChat = async () => {
    if (!user?.token) return;

    const text = aiChatDraft.trim();
    if (!text) return;

    const userMessage = { role: 'user', content: text };
    setAiChatMessages(prev => [...prev, userMessage]);
    setAiChatDraft('');
    setAiChatLoading(true);

    try {
      const result = await api.chatSupport(
        {
          entry_text: text,
          mood: moodData.mood
        },
        user.token
      );

      const aiMessage = {
        role: 'assistant',
        content: result.support || result.summary || 'Thanks for sharing.'
      };
      setAiChatMessages(prev => [...prev, aiMessage]);
    } catch (error) {
      console.error('AI chat error:', error);
      alert('AI chat failed: ' + error.message);
    } finally {
      setAiChatLoading(false);
    }
  };

  const handlePrefillAiSupport = () => {
    const fallbackText = moodData.description || moodData.note || '';
    if (!aiChatDraft && fallbackText) {
      setAiChatDraft(fallbackText);
    }
    setCurrentView('ai-chat');
  };

  const handleLikePost = async (postId) => {
    if (!user?.token) return;

    try {
      await api.likePost(postId, user.token);
      setCommunityPosts(prev =>
        prev.map(post => {
          if (post._id === postId) {
            return {
              ...post,
              isLiked: !post.isLiked,
              likes: post.isLiked ? post.likes - 1 : post.likes + 1,
            };
          }
          return post;
        }),
      );
    } catch (error) {
      console.error('Like post error:', error);
    }
  };

  const handleStarPost = async (postId) => {
    if (!user?.token) return;

    try {
      await api.starPost(postId, user.token);
      setCommunityPosts(prev =>
        prev.map(post => {
          if (post._id === postId) {
            return {
              ...post,
              isStarred: !post.isStarred,
              stars: post.isStarred ? post.stars - 1 : post.stars + 1,
            };
          }
          return post;
        }),
      );
    } catch (error) {
      console.error('Star post error:', error);
    }
  };

  const loadMoodEntriesForCalendar = async () => {
    if (!user?.token) return;

    try {
      console.log('Loading mood entries for calendar...');
      const result = await api.getMoodHistory(user.token);
      console.log('Mood history result:', result);
      
      const entries = dedupeMoodEntries(result.moods || []);
      console.log('Mood entries loaded:', entries.length);
      
      const entriesByDate = {};
      entries.forEach(entry => {
        const dateKey = formatDateKey(new Date(entry.date));
        if (!entriesByDate[dateKey]) {
          entriesByDate[dateKey] = [];
        }
        entriesByDate[dateKey].push(entry);
      });

      console.log('Entries by date:', entriesByDate);
      setCalendarMoodEntries(entriesByDate);
      setMoodEntries(entries);
    } catch (error) {
      console.error('Failed to load mood entries for calendar:', error);
    }
  };

  const handleEnterEditProfile = async () => {
    if (!user?.token) return;
    
    setIsLoading(true);
    try {
      // Fetch fresh user data from database
      const result = await api.getUserProfile(user.token);
      console.log('Fresh user data fetched:', result);
      
      // Update local user state with fresh data
      setUser(prev => ({
        ...prev,
        ...result.user
      }));
      
      // Initialize profile data with fresh user data
      setProfileData({
        username: result.user.username || '',
        age: result.user.age || 25,
        gender: result.user.gender || '',
        nationality: result.user.nationality || '',
        hobbies: result.user.hobbies || []
      });
      
      // Update localStorage
      try {
        if (typeof localStorage !== 'undefined') {
          const updatedUser = { ...user, ...result.user };
          localStorage.setItem('moodJournalUser', JSON.stringify(updatedUser));
          console.log('Updated user data in localStorage');
        }
      } catch (error) {
        console.error('Error updating localStorage:', error);
      }
      
      setCurrentView('edit-profile');
    } catch (error) {
      console.error('Failed to fetch user profile:', error);
      // Fallback to current user data
      setProfileData({
        username: user.username || '',
        age: user.age || 25,
        gender: user.gender || '',
        nationality: user.nationality || '',
        hobbies: user.hobbies || []
      });
      setCurrentView('edit-profile');
    } finally {
      setIsLoading(false);
    }
  };

  // Load mood entries when user logs in
  useEffect(() => {
    if (user?.token) {
      loadMoodEntriesForCalendar();
    }
  }, [user]);

  // Load community posts when viewing community
  useEffect(() => {
    if (currentView === 'community') {
      loadCommunityPosts();
    }
  }, [currentView]);

  // Auto-redirect to main if user is already logged in
  useEffect(() => {
    if (user?.token && currentView === 'auth') {
      console.log('User already logged in, redirecting to main');
      setCurrentView('main');
    }
  }, [user, currentView]);

  useEffect(() => {
    if (!user?.id) return;
    try {
      if (typeof localStorage !== 'undefined') {
        const raw = localStorage.getItem(getLastSeenKey(user.id));
        if (raw) {
          setLastSeenConversations(JSON.parse(raw));
        }
      }
    } catch (error) {
      console.error('Error loading last seen map:', error);
    }
  }, [user?.id]);

  useEffect(() => {
    if (!user?.id) return;
    try {
      if (typeof localStorage !== 'undefined') {
        localStorage.setItem(
          getLastSeenKey(user.id),
          JSON.stringify(lastSeenConversations)
        );
      }
    } catch (error) {
      console.error('Error saving last seen map:', error);
    }
  }, [lastSeenConversations, user?.id]);

  useEffect(() => {
    if (!user?.token || !user?.id) return;

    let intervalId;
    const pollConversations = async () => {
      try {
        const result = await api.getConversations(user.token);
        const conversations = result.conversations || [];

        const hasUnread = conversations.some((convo) => {
          if (!convo.last_message_at) return false;
          if (convo.last_message_sender_id && String(convo.last_message_sender_id) === String(user.id)) {
            return false;
          }
          const lastSeen = lastSeenConversations[convo._id];
          if (!lastSeen) return true;
          return new Date(convo.last_message_at) > new Date(lastSeen);
        });

        if (hasUnread && currentView !== 'chat') {
          setHasUnreadMessages(true);
        }
      } catch (error) {
        console.error('Polling conversations failed:', error);
      }
    };

    pollConversations();
    intervalId = setInterval(pollConversations, 5000);

    return () => {
      if (intervalId) clearInterval(intervalId);
    };
  }, [user?.token, user?.id, lastSeenConversations, currentView]);

  useEffect(() => {
    if (currentView !== 'chat' || !user?.token) return;

    let isMounted = true;
    const loadConversations = async () => {
      setIsConversationsLoading(true);
      try {
        const result = await api.getConversations(user.token);
        if (!isMounted) return;
        const list = result.conversations || [];
        setConversations(list);

        if (list.length > 0) {
          const activeExists = list.some((convo) => convo._id === activeConversationId);
          if (!activeConversationId || !activeExists) {
            setActiveConversationId(list[0]._id);
          }
        }
      } catch (error) {
        console.error('Load conversations failed:', error);
      } finally {
        if (isMounted) setIsConversationsLoading(false);
      }
    };

    loadConversations();
    return () => {
      isMounted = false;
    };
  }, [currentView, user?.token, activeConversationId]);

  useEffect(() => {
    authModeRef.current = authMode;
  }, [authMode]);

  useEffect(() => {
    if (!activeConversationId || !user?.token) return;

    let intervalId;
    const pollMessages = async () => {
      try {
        const lastServerMessage = [...chatMessages]
          .reverse()
          .find((message) => !String(message._id || '').startsWith('temp-'));
        const since = lastServerMessage ? lastServerMessage.created_at : undefined;
        const result = await api.getConversationMessages(
          activeConversationId,
          user.token,
          since
        );

        if (result.messages && result.messages.length > 0) {
          setChatMessages(prev => {
            const existingIds = new Set(prev.map((msg) => msg._id));
            const existingClientIds = new Set(
              prev.map((msg) => msg.client_id).filter(Boolean)
            );
            const next = result.messages.filter((msg) => {
              if (existingIds.has(msg._id)) return false;
              if (msg.client_id && existingClientIds.has(msg.client_id)) return false;
              return true;
            });
            const hasIncoming = next.some(
              (msg) => String(msg.sender_id) !== String(user?.id)
            );
            if (hasIncoming && currentView !== 'chat') {
              setHasUnreadMessages(true);
            }
            if (currentView === 'chat' && next.length > 0) {
              const lastMessage = next[next.length - 1];
              setLastSeenConversations(prev => ({
                ...prev,
                [activeConversationId]: lastMessage.created_at
              }));
            }
            return [...prev, ...next];
          });
        }
      } catch (error) {
        console.error('Polling messages failed:', error);
      }
    };

    pollMessages();
    intervalId = setInterval(pollMessages, 3000);

    return () => {
      if (intervalId) clearInterval(intervalId);
    };
  }, [activeConversationId, user?.token, chatMessages, currentView]);

  useEffect(() => {
    if (currentView === 'chat') {
      setHasUnreadMessages(false);
    }
  }, [currentView]);

  useEffect(() => {
    if (currentView !== 'chat' || !activeConversationId) return;
    if (chatMessages.length === 0) return;
    const lastMessage = chatMessages[chatMessages.length - 1];
    setLastSeenConversations(prev => ({
      ...prev,
      [activeConversationId]: lastMessage.created_at
    }));
  }, [currentView, activeConversationId, chatMessages]);

  // Render functions
  const renderAuth = () => (
    <div className="auth-container">
      <div className="auth-card">
        <span className="auth-title">Mood Journal</span>
        <span className="auth-subtitle">
          Track your feelings, get personalized recommendations
        </span>

        <div className="auth-tabs">
          <span
            className={`auth-tab ${authMode === 'login' ? 'active' : ''}`}
            onClick={() => {
              authModeRef.current = 'login';
              setAuthMode('login');
            }}
          >
            Login
          </span>
          <span
            className={`auth-tab ${authMode === 'register' ? 'active' : ''}`}
            onClick={() => {
              authModeRef.current = 'register';
              setAuthMode('register');
            }}
          >
            Register
          </span>
        </div>

        <div className="auth-input-container">
          <span className="auth-input-label">Username</span>
          <input
            className="auth-input-field"
            placeholder="Enter username"
            value={authData.username}
            type="text"
            
            onChange={(e) => {
              setAuthData(prev => ({ ...prev, username: e.target.value }));
            }}
            onFocus={(e) => {
              console.log('Username input focused');
            }}
            onClick={(e) => {
              console.log('Username input tapped');
            }}
          />
        </div>

        {authMode === 'register' && (
          <>
            <div className="auth-input-container">
              <span className="auth-input-label">Email</span>
              <input
                className="auth-input-field"
                placeholder="Enter email"
                type="email"
                value={authData.email}
                
                onChange={(e) => {
                  setAuthData(prev => ({ ...prev, email: e.target.value }));
                }}
                onFocus={(e) => {
                  console.log('Email input focused');
                }}
                onClick={(e) => {
                  console.log('Email input tapped');
                }}
              />
            </div>

            <div className="auth-input-container">
              <span className="auth-input-label">Age</span>
              <input
                className="auth-input-field"
                placeholder="Enter age"
                type="number"
                value={authData.age === null ? '' : authData.age.toString()}
                
                onChange={(e) => {
                  const rawValue = e.target.value.trim();
                  const parsedAge = rawValue === '' ? null : parseInt(rawValue, 10);
                  setAuthData(prev => ({ ...prev, age: Number.isNaN(parsedAge) ? null : parsedAge }));
                }}
                onFocus={(e) => {
                  console.log('Age input focused');
                }}
                onClick={(e) => {
                  console.log('Age input tapped');
                }}
              />
            </div>

            <div className="auth-input-container">
              <span className="auth-input-label">Gender</span>
              <input
                className="auth-input-field"
                placeholder="Enter gender"
                value={authData.gender}
                type="text"
                
                onChange={(e) => {
                  setAuthData(prev => ({ ...prev, gender: e.target.value }));
                }}
                onFocus={(e) => {
                  console.log('Gender input focused');
                }}
                onClick={(e) => {
                  console.log('Gender input tapped');
                }}
              />
            </div>

            <div className="auth-input-container">
              <span className="auth-input-label">Nationality</span>
              <input
                className="auth-input-field"
                placeholder="Enter nationality"
                value={authData.nationality}
                type="text"
                
                onChange={(e) => {
                  setAuthData(prev => ({ ...prev, nationality: e.target.value }));
                }}
                onFocus={(e) => {
                  console.log('Nationality input focused');
                }}
                onClick={(e) => {
                  console.log('Nationality input tapped');
                }}
              />
            </div>

            <div className="auth-input-container">
              <span className="auth-input-label">Hobbies (comma separated)</span>
              <input
                className="auth-input-field"
                placeholder="e.g., reading, music, sports"
                value={authData.hobbiesInput}
                type="text"
                
                onChange={(e) => {
                  setAuthData(prev => ({ ...prev, hobbiesInput: e.target.value }));
                }}
                onFocus={(e) => {
                  console.log('Hobbies input focused');
                }}
                onClick={(e) => {
                  console.log('Hobbies input tapped');
                }}
              />
            </div>
          </>
        )}

        <div className="auth-input-container">
          <span className="auth-input-label">Password</span>
          <input
            className="auth-input-field"
            placeholder="Enter password"
            type="password"
            value={authData.password}
            
            onChange={(e) => {
              setAuthData(prev => ({ ...prev, password: e.target.value }));
            }}
            onFocus={(e) => {
              console.log('Password input focused');
            }}
            onClick={(e) => {
              console.log('Password input tapped');
            }}
          />
        </div>

        <div className="auth-button" onClick={handleAuth}>
          <span className="auth-button-text">
            {isLoading
              ? 'Loading...'
              : authMode === 'login'
                ? 'Login'
                : 'Register'}
          </span>
        </div>
      </div>
    </div>
  );

  const renderMain = () => (
    <div className="main-container">
      <div className="header">
        <div style={{
          display: 'flex',
          justifyContent: 'space-between',
          alignItems: 'center',
          width: '100%'
        }}>
          <div style={{ flex: 1 }}>
            <span className="welcome-text">Welcome back, {user?.username}! 👋</span>
            <span className="date-text">{formatDate(new Date())}</span>
          </div>
          <div
            className="profile-button"
            onClick={handleEnterEditProfile}
            style={{
              background: 'rgba(255, 255, 255, 0.2)',
              borderRadius: '50%',
              width: '40px',
              height: '40px',
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center',
              cursor: 'pointer',
              transition: 'all 0.3s ease'
            }}
          >
            <span style={{ fontSize: '20px' }}>👤</span>
          </div>
        </div>
      </div>

      <div className="calendar-section">
        <div className="calendar-header">
          <div
            className="calendar-nav-button"
            onClick={() => {
              setCurrentDate(new Date(
                currentDate.getFullYear(),
                currentDate.getMonth() - 1,
                1,
              ));
            }}
          >
            <span className="calendar-nav-text">‹</span>
          </div>
          <span className="calendar-title">
            {formatDate(currentDate, {
              month: 'long',
              year: 'numeric'
            })}
          </span>
          <div
            className="calendar-nav-button"
            onClick={() => {
              setCurrentDate(new Date(
                currentDate.getFullYear(),
                currentDate.getMonth() + 1,
                1,
              ));
            }}
          >
            <span className="calendar-nav-text">›</span>
          </div>
        </div>

        <div className="calendar-grid">
          <div className="calendar-day-header">Sun</div>
          <div className="calendar-day-header">Mon</div>
          <div className="calendar-day-header">Tue</div>
          <div className="calendar-day-header">Wed</div>
          <div className="calendar-day-header">Thu</div>
          <div className="calendar-day-header">Fri</div>
          <div className="calendar-day-header">Sat</div>

          {/* Render calendar days */}
          {(() => {
            const year = currentDate.getFullYear();
            const month = currentDate.getMonth();
            const firstDay = new Date(year, month, 1);
            const lastDay = new Date(year, month + 1, 0);
            const startDate = new Date(firstDay);
            startDate.setDate(startDate.getDate() - firstDay.getDay());
            
            const days = [];
            const today = new Date();
            
            for (let i = 0; i < 42; i++) {
              const date = new Date(startDate);
              date.setDate(startDate.getDate() + i);
              
              const isCurrentMonth = date.getMonth() === month;
              const isToday = date.toDateString() === today.toDateString();
              const isFuture = isFutureDate(date);
              const dateKey = formatDateKey(date);
              const moodForDate = getMoodForDate(date);
              
              days.push(
                <div
                  key={i}
                  className={`calendar-day ${!isCurrentMonth ? 'other-month' : ''} ${isToday ? 'today' : ''} ${moodForDate ? 'has-mood' : ''} ${isFuture ? 'future' : ''}`}
                  onClick={() => {
                    if (isCurrentMonth) {
                      if (isFuture) {
                        alert('You can only log moods for today or earlier.');
                        return;
                      }
                      if (moodForDate) {
                        // If there's already a mood for this date, show day details
                        setSelectedDate(date);
                        setCurrentView('day-detail');
                        console.log('Showing day details for date:', date.toDateString());
                      } else {
                        // If no mood for this date, navigate to mood logging
                        setMoodLogDate(date);
                        setCurrentView('mood-log');
                        console.log('Navigating to mood logging for date:', date.toDateString());
                      }
                    }
                  }}
                  style={{
                    backgroundColor: moodForDate ? getMoodColor(moodForDate) : undefined,
                    opacity: !isCurrentMonth ? 0.4 : 1
                  }}
                >
                  <span className="calendar-day-number">{date.getDate()}</span>
                  {moodForDate && (
                    <span className="calendar-day-mood" style={{ fontSize: '12px', marginTop: '2px' }}>
                      {getMoodEmoji(moodForDate)}
                    </span>
                  )}
                </div>
              );
            }
            
            return days;
          })()}
        </div>
      </div>

      <div className="bottom-actions">
        <div
          className="action-button log-mood"
          onClick={() => {
            setMoodLogDate(new Date()); // Set current date for mood logging
            setCurrentView('mood-log');
          }}
        >
          <span className="action-button-text">📝 Log Mood</span>
        </div>
        <div
          className="action-button community"
          onClick={() => setCurrentView('community')}
        >
          <span className="action-button-text">🌍 Community</span>
        </div>
      </div>
    </div>
  );

  const renderAppShell = (bodyContent) => (
    <div className="app-shell">
      <div className="topbar">
        <div className="brand">
          <span className="brand-title">Mood Journal</span>
          <span className="brand-subtitle">Personal dashboard</span>
        </div>
        <div className="topbar-actions">
          <span className="topbar-user">Hi, {user?.username}</span>
          <div className="topbar-button" onClick={handleLogout}>
            <span className="topbar-button-text">Log out</span>
          </div>
        </div>
      </div>
      <div className="shell-body">
        <div className="sidebar">
          <div
            className={`nav-item ${currentView === 'main' ? 'active' : ''}`}
            onClick={() => setCurrentView('main')}
          >
            <span className="nav-item-text">Dashboard</span>
          </div>
          <div
            className={`nav-item ${currentView === 'mood-log' ? 'active' : ''}`}
            onClick={() => setCurrentView('mood-log')}
          >
            <span className="nav-item-text">Log mood</span>
          </div>
          <div
            className={`nav-item ${currentView === 'recommendations' ? 'active' : ''}`}
            onClick={() => setCurrentView('recommendations')}
          >
            <span className="nav-item-text">Recommendations</span>
          </div>
          <div
            className={`nav-item ${currentView === 'community' ? 'active' : ''}`}
            onClick={() => setCurrentView('community')}
          >
            <span className="nav-item-text">Community</span>
          </div>
          <div
            className={`nav-item ${currentView === 'chat' ? 'active' : ''}`}
            onClick={() => setCurrentView('chat')}
          >
            <div className="nav-item-label">
              <span className="nav-item-text">Messages</span>
              {hasUnreadMessages && currentView !== 'chat' && (
                <span className="nav-item-dot" title="New messages" />
              )}
            </div>
          </div>
          <div
            className={`nav-item ${currentView === 'ai-chat' ? 'active' : ''}`}
            onClick={() => setCurrentView('ai-chat')}
          >
            <span className="nav-item-text">AI Chat</span>
          </div>
          <div
            className={`nav-item ${currentView === 'edit-profile' ? 'active' : ''}`}
            onClick={handleEnterEditProfile}
          >
            <span className="nav-item-text">Profile</span>
          </div>
        </div>
        <div className="content-area">{bodyContent}</div>
      </div>
    </div>
  );

  const renderMoodLog = () => (
    <div className="mood-log-container">
      <div className="mood-log-header">
        <div
          className="back-button"
          onClick={() => setCurrentView('main')}
        >
          <span className="back-button-text">← Back</span>
        </div>
        <span className="mood-log-title">How are you feeling?</span>
      </div>

      <div className="mood-selector">
        {['happy', 'sad', 'anxious', 'excited'].map(mood => (
          <div
            key={mood}
            className={`mood-option ${moodData.mood === mood ? 'selected' : ''}`}
            onClick={() => setMoodData(prev => ({ ...prev, mood }))}
            style={{
              backgroundColor: moodData.mood === mood ? getMoodColor(mood) : 'rgba(255, 255, 255, 0.95)',
              border: moodData.mood === mood ? '3px solid var(--accent)' : '3px solid transparent',
              borderRadius: '16px',
              padding: '20px',
              textAlign: 'center',
              transition: 'all 0.3s ease',
              boxShadow: moodData.mood === mood ? '0 8px 25px rgba(0, 0, 0, 0.15)' : '0 4px 15px rgba(0, 0, 0, 0.1)',
              transform: moodData.mood === mood ? 'translateY(-2px)' : 'translateY(0)'
            }}
          >
            <span className="mood-option-emoji" style={{ fontSize: '32px', marginBottom: '8px' }}>{getMoodEmoji(mood)}</span>
            <span className="mood-option-name" style={{ 
              fontSize: '16px', 
              fontWeight: '600', 
              color: moodData.mood === mood ? 'white' : '#333' 
            }}>{capitalizeFirst(mood)}</span>
          </div>
        ))}
      </div>

      <div className="mood-intensity">
        <span className="mood-intensity-label" style={{
          fontSize: '18px',
          fontWeight: '600',
          color: 'white',
          marginBottom: '15px',
          textAlign: 'center'
        }}>
          Intensity (1-10)
        </span>
        
        {/* Segmented intensity bar */}
        <div style={{
          display: 'flex',
          justifyContent: 'space-between',
          gap: '4px',
          marginBottom: '15px',
          width: '100%'
        }}>
          {[1, 2, 3, 4, 5, 6, 7, 8, 9, 10].map(level => (
            <div
              key={level}
              onClick={() => {
                console.log('Intensity segment selected:', level);
                setMoodData(prev => ({ ...prev, intensity: level }));
              }}
              style={{
                flex: 1,
                height: '20px',
                backgroundColor: moodData.intensity >= level ? '#6036d6' : 'rgb(255, 255, 255)',
                borderRadius: '6px',
                transition: 'all 0.3s ease',
                border: moodData.intensity >= level ? 'none' : '1px solid rgb(255, 255, 255)',
                minWidth: '20px'
              }}
            />
          ))}
        </div>
      </div>

      <div className="mood-input-container">
        <span className="mood-input-label">What happened today?</span>
        <input
          className="mood-input-field"
          placeholder="Describe what made you feel this way..."
          value={moodData.description}
          type="text"
          
          auto-focus={false}
          onChange={(e) => {
            console.log('Description input value:', e.target.value);
            setMoodData(prev => ({ ...prev, description: e.target.value }));
          }}
          onFocus={(e) => {
            console.log('Description input focused');
          }}
          bindblur={(e) => {
            console.log('Description input blurred');
          }}
          onClick={(e) => {
            console.log('Description input tapped');
          }}
        />
      </div>

      <div className="mood-visibility" style={{
        display: 'flex',
        alignItems: 'center',
        gap: '10px',
        marginTop: '10px',
        background: 'rgba(255, 255, 255, 0.9)',
        borderRadius: '12px',
        padding: '12px 16px'
      }}>
        <input
          id="mood-public-toggle"
          type="checkbox"
          checked={moodData.is_public}
          onChange={(e) => {
            setMoodData(prev => ({ ...prev, is_public: e.target.checked }));
          }}
        />
        <label htmlFor="mood-public-toggle" style={{
          fontSize: '14px',
          color: '#1f2937',
          fontWeight: 600
        }}>
          Share this entry to the community feed
        </label>
      </div>

      <div
        className="ai-chat-cta"
        onClick={handlePrefillAiSupport}
        style={{
          marginTop: '12px',
          background: 'rgba(255, 255, 255, 0.95)',
          borderRadius: '12px',
          padding: '12px 16px',
          cursor: 'pointer',
          fontWeight: 600,
          color: '#0f172a'
        }}
      >
        Talk to AI support about this entry
      </div>

      <div className="mood-input-container">
        <span className="mood-input-label">Additional notes (optional)</span>
        <input
          className="mood-input-field"
          placeholder="Any additional thoughts..."
          value={moodData.note}
          type="text"
          
          auto-focus={false}
          onChange={(e) => {
            console.log('Notes input value:', e.target.value);
            setMoodData(prev => ({ ...prev, note: e.target.value }));
          }}
          onFocus={(e) => {
            console.log('Notes input focused');
          }}
          bindblur={(e) => {
            console.log('Notes input blurred');
          }}
          onClick={(e) => {
            console.log('Notes input tapped');
          }}
        />
      </div>

      <div 
        className="mood-log-button" 
        onClick={handleLogMood}
        style={{
          background: 'linear-gradient(135deg, var(--accent-strong) 0%, var(--accent-soft) 100%)',
          borderRadius: '16px',
          padding: '20px',
          textAlign: 'center',
          boxShadow: '0 8px 25px rgba(102, 126, 234, 0.3)',
          transition: 'all 0.3s ease',
          marginTop: '30px',
          border: 'none'
        }}
      >
        <span className="mood-log-button-text" style={{
          color: 'white',
          fontSize: '18px',
          fontWeight: '600'
        }}>
          {isLoading ? 'Logging...' : 'Log Mood'}
        </span>
      </div>
    </div>
  );

  const renderCommunity = () => (
    <div className="community-container">
      <div className="community-header">
        <div
          className="back-button"
          onClick={() => setCurrentView('main')}
        >
          <span className="back-button-text">← Back</span>
        </div>
        <span className="community-title">Community Feed</span>
      </div>

      <div
        className="community-posts-scroll"
        
        style={{ flex: 1, width: '100%' }}
        
        
      >
        {communityPosts.map(post => (
          <div key={post._id} className="community-post">
            <div className="post-header">
              <span className="post-username">{post.user_username}</span>
              <span className="post-mood">
                {getMoodEmoji(post.mood)} {capitalizeFirst(post.mood)}
              </span>
            </div>

            <span className="post-message">
              <span className="post-user-label">{post.user_username}:</span>
              <span className="post-message-text">
                {post.description || post.activity_description || post.activity_title}
              </span>
            </span>

            {!isPostOwner(post) && (
              <div
                className="post-thread-button"
                onClick={() => startConversationWithUser(post.user_id)}
                style={{
                  background: 'linear-gradient(135deg, rgba(14, 165, 164, 0.95), rgba(56, 189, 248, 0.95))',
                  padding: '10px 16px',
                  borderRadius: '999px',
                  boxShadow: '0 6px 16px rgba(14, 165, 164, 0.25)',
                  display: 'inline-flex',
                  alignItems: 'center',
                  gap: '6px',
                  cursor: 'pointer'
                }}
              >
                <span className="post-thread-button-text">Message creator</span>
              </div>
            )}

            <div className="post-stats">
              <div
                className={`post-stat ${post.isLiked ? 'liked' : ''}`}
                onClick={() => handleLikePost(post._id)}
              >
                <span className="post-stat-text">👍 {post.likes}</span>
              </div>
              <div
                className={`post-stat ${post.isStarred ? 'starred' : ''}`}
                onClick={() => handleStarPost(post._id)}
              >
                <span className="post-stat-text">⭐ {post.stars}</span>
              </div>
            </div>

            <div className="post-thread">
              <div className="post-thread-actions">
                <div
                  className="post-thread-button"
                  onClick={() => loadPostComments(post._id)}
                  style={{
                    background: 'linear-gradient(135deg, rgba(14, 165, 164, 0.95), rgba(56, 189, 248, 0.95))',
                    padding: '10px 16px',
                    borderRadius: '999px',
                    boxShadow: '0 6px 16px rgba(14, 165, 164, 0.25)',
                    display: 'inline-flex',
                    alignItems: 'center',
                    gap: '6px',
                    cursor: 'pointer'
                  }}
                >
                  <span className="post-thread-button-text">View replies</span>
                </div>
                {isPostOwner(post) && activeReplyTargets[post._id] && (
                  <span className="post-thread-target">
                    Replying to thread
                  </span>
                )}
              </div>

              {(postComments[post._id] || []).length > 0 && (
                <div className="post-thread-list">
                  {postComments[post._id].map((comment) => (
                    <div key={comment._id} className="post-thread-item">
                      <span className="post-thread-text">
                        <span className="post-thread-author">
                          {comment.user_username || 'Anonymous'}
                          {comment.is_owner_reply ? ' (Owner)' : ''}:
                        </span>{' '}
                        {comment.comment}
                      </span>
                      {isPostOwner(post) && (
                        <div
                          className="post-thread-reply"
                          onClick={() => {
                            setActiveReplyTargets(prev => ({
                              ...prev,
                              [post._id]: comment.thread_user_id
                            }));
                          }}
                          style={{
                            background: 'rgba(15, 23, 42, 0.08)',
                            padding: '6px 10px',
                            borderRadius: '999px',
                            display: 'inline-flex',
                            alignItems: 'center',
                            cursor: 'pointer'
                          }}
                        >
                          <span className="post-thread-reply-text">Reply</span>
                        </div>
                      )}
                    </div>
                  ))}
                </div>
              )}

              <div className="post-thread-input">
                <input
                  className="post-thread-field"
                  placeholder={
                    isPostOwner(post)
                      ? 'Select a thread, then reply'
                      : 'Write a reply'
                  }
                  value={commentDrafts[post._id] || ''}
                  onChange={(e) => handleCommentDraftChange(post._id, e.target.value)}
                />
                <div
                  className="post-thread-send"
                  onClick={() => handleAddComment(post)}
                  style={{
                    background: '#0f172a',
                    padding: '10px 16px',
                    borderRadius: '12px',
                    boxShadow: '0 6px 16px rgba(15, 23, 42, 0.2)',
                    display: 'inline-flex',
                    alignItems: 'center',
                    cursor: 'pointer'
                  }}
                >
                  <span className="post-thread-send-text" style={{ color: '#ffffff' }}>Send</span>
                </div>
              </div>
            </div>
          </div>
        ))}
      </div>
    </div>
  );

  const renderChat = () => (
    <div className="chat-container">
      <div className="chat-header">
        <div
          className="back-button"
          onClick={() => setCurrentView('community')}
        >
          <span className="back-button-text">← Back</span>
        </div>
        <span className="chat-title">Private Messages</span>
      </div>
      <div className="chat-layout">
        <div className="chat-list">
          <div className="chat-list-title">Conversations</div>
          {isConversationsLoading && (
            <div className="chat-list-empty">Loading...</div>
          )}
          {!isConversationsLoading && conversations.length === 0 && (
            <div className="chat-list-empty">Start a chat from the community feed.</div>
          )}
          {!isConversationsLoading && conversations.length > 0 && (
            <div className="chat-list-items">
              {conversations.map((convo) => (
                <div
                  key={convo._id}
                  className={`chat-list-item ${convo._id === activeConversationId ? 'active' : ''}`}
                  onClick={() => setActiveConversationId(convo._id)}
                >
                  <div className="chat-list-name">{getConversationPartnerName(convo)}</div>
                  <div className="chat-list-meta">
                    {convo.last_message_at ? formatTime(convo.last_message_at) : 'No messages yet'}
                    {isConversationUnread(convo) && (
                      <span className="chat-list-badge" />
                    )}
                  </div>
                </div>
              ))}
            </div>
          )}
        </div>

        {!activeConversationId ? (
          <div className="chat-empty">
            <span className="chat-empty-text">
              Select a conversation to view messages.
            </span>
          </div>
        ) : (
          <div className="chat-body">
            <div className="chat-messages">
              {chatMessages.map((message) => (
                <div
                  key={message._id}
                  className={`chat-message ${message.sender_id === user?.id ? 'outgoing' : 'incoming'}`}
                >
                  {message.sender_id !== user?.id && (
                    <span className="chat-message-author">
                      {message.sender_username || 'User'}
                    </span>
                  )}
                  <span className="chat-message-text">{message.text}</span>
                  <span className="chat-message-time">
                    {formatTime(message.created_at)}
                  </span>
                </div>
              ))}
            </div>

            <div className="chat-input">
              <input
                className="chat-input-field"
                placeholder="Type a message"
                value={chatDraft}
                onChange={(e) => setChatDraft(e.target.value)}
                onKeyDown={(e) => {
                  if (e.key === 'Enter') {
                    e.preventDefault();
                    handleSendChatMessage();
                  }
                }}
              />
              <div className="chat-send" onClick={handleSendChatMessage}>
                <span className="chat-send-text">Send</span>
              </div>
            </div>
          </div>
        )}
      </div>
    </div>
  );

  const renderAiChat = () => (
    <div className="chat-container">
      <div className="chat-header">
        <div
          className="back-button"
          onClick={() => setCurrentView('main')}
        >
          <span className="back-button-text">← Back</span>
        </div>
        <span className="chat-title">AI Support Chat</span>
      </div>

      <div className="chat-disclaimer">
        <span className="chat-disclaimer-text">
          This is not a medical service. If you feel unsafe, contact local emergency services.
        </span>
      </div>

      <div className="chat-body">
        <div className="chat-messages">
          {aiChatMessages.map((message, index) => (
            <div
              key={`${message.role}-${index}`}
              className={`chat-message ${message.role === 'user' ? 'outgoing' : 'incoming'} ${message.role === 'meta' ? 'meta' : ''}`}
            >
              <span className="chat-message-text">{message.content}</span>
            </div>
          ))}
          {aiChatLoading && (
            <div className="chat-message incoming">
              <span className="chat-typing">
                <span className="chat-typing-dot" />
                <span className="chat-typing-dot" />
                <span className="chat-typing-dot" />
              </span>
            </div>
          )}
        </div>

        <div className="chat-input">
          <input
            className="chat-input-field"
            placeholder="Share how you're feeling"
            value={aiChatDraft}
            onChange={(e) => setAiChatDraft(e.target.value)}
            onKeyDown={(e) => {
              if (e.key === 'Enter') {
                e.preventDefault();
                handleSendAiChat();
              }
            }}
          />
          <div className="chat-send" onClick={handleSendAiChat}>
            <span className="chat-send-text">Send</span>
          </div>
        </div>
      </div>
    </div>
  );

  const renderRecommendations = () => (
    <div className="recommendations-container">
      <div className="recommendations-header">
        <div
          className="back-button"
          onClick={() => setCurrentView('main')}
        >
          <span className="back-button-text">← Back</span>
        </div>
        <span className="recommendations-title">Your Recommendations</span>
      </div>

      {isLoading ? (
        <div className="loading-recommendations">
          <span className="loading-text">Getting personalized recommendations...</span>
        </div>
      ) : currentRecommendation ? (
        <div className="recommendation-card">
          <div className="recommendation-header">
            <span className="recommendation-type">{currentRecommendation.type}</span>
            <span className="recommendation-category">{currentRecommendation.category}</span>
          </div>
          <span className="recommendation-title">{currentRecommendation.title}</span>
          <span className="recommendation-description">{currentRecommendation.description}</span>
          <span className="recommendation-reasoning">{currentRecommendation.reasoning}</span>
          <div className="recommendation-actions">
            <div
              className="action-button like"
              onClick={() => handleRecommendationFeedback('like')}
            >
              <span className="action-button-text">👍 Like</span>
            </div>
            <div
              className="action-button dislike"
              onClick={() => handleRecommendationFeedback('dislike')}
            >
              <span className="action-button-text">👎 Dislike</span>
            </div>
            <div
              className="action-button share"
              onClick={() => handleShareRecommendation()}
            >
              <span className="action-button-text">📤 Share</span>
            </div>
          </div>
          {recommendationList.length > 0 && (
            <div className="recommendation-list">
              <span className="recommendation-list-title">More ideas</span>
              {recommendationList.map((item, index) => (
                <div key={`${item.title}-${index}`} className="recommendation-list-item">
                  <span className="recommendation-list-type">{item.type}</span>
                  <span className="recommendation-list-title-text">{item.title}</span>
                  <span className="recommendation-list-description">{item.description}</span>
                </div>
              ))}
            </div>
          )}
        </div>
      ) : (
        <div className="loading-recommendations">
          <span className="loading-text">No recommendations yet</span>
          <div
            className="get-recommendations-button"
            onClick={() => {
              console.log('Get Recommendations button clicked!');
              console.log('Current moodData:', moodData);
              console.log('Current user:', user);
              handleGetRecommendation();
            }}
          >
            <span className="get-recommendations-button-text">Get Recommendations</span>
          </div>
        </div>
      )}
    </div>
  );

  const renderDayDetail = () => {
    if (!selectedDate) return renderMain();
    
    const dateKey = formatDateKey(selectedDate);
    const entries = dedupeMoodEntries(calendarMoodEntries[dateKey] || []);
    
    return (
      <div className="day-detail-container">
        <div className="day-detail-header">
          <div
            className="back-button"
            onClick={() => setCurrentView('main')}
          >
            <span className="back-button-text">← Back</span>
          </div>
          <span className="day-detail-title">
            {formatDate(selectedDate, { 
              weekday: 'long', 
              year: 'numeric', 
              month: 'long', 
              day: 'numeric' 
            })}
          </span>
        </div>

        {entries.length === 0 ? (
          <div className="no-entries">
            <span className="no-entries-text">No mood entries for this day</span>
            <div
              className="add-entry-button"
              onClick={() => {
                setCurrentView('mood-log');
              }}
            >
              <span className="add-entry-button-text">Add Mood Entry</span>
            </div>
          </div>
        ) : (
          <div className="day-entries">
            {entries.map((entry) => (
              <div key={getMoodEntryKey(entry)} className="day-entry-card">
                <div className="entry-header">
                  <span className="entry-mood-emoji">{getMoodEmoji(entry.mood)}</span>
                  <span className="entry-mood-name">{capitalizeFirst(entry.mood)}</span>
                  <div className="entry-intensity">
                    {Array.from({ length: entry.intensity }, (_, i) => (
                      <div key={i} className="intensity-dot" />
                    ))}
                  </div>
                </div>
                {entry.description && (
                  <span className="entry-description">{entry.description}</span>
                )}
                {entry.note && (
                  <span className="entry-note">{entry.note}</span>
                )}
                <span className="entry-time">
                  {formatTime(entry.date)}
                </span>
              </div>
            ))}
          </div>
        )}
      </div>
    );
  };

  const renderEditProfile = () => {
    const handleSaveProfile = async () => {
      if (!user?.token) return;
      
      setIsLoading(true);
      try {
        const result = await api.updateProfile(user.token, profileData);
        console.log('Profile updated successfully:', result);
        
        // Update local user state with the response data
        const updatedUserData = {
          ...user,
          username: profileData.username,
          age: profileData.age,
          gender: profileData.gender,
          nationality: profileData.nationality,
          hobbies: profileData.hobbies
        };
        
        setUser(updatedUserData);
        
        // Update localStorage
        try {
          if (typeof localStorage !== 'undefined') {
            localStorage.setItem('moodJournalUser', JSON.stringify(updatedUserData));
            console.log('Updated user data in localStorage');
          }
        } catch (error) {
          console.error('Error updating localStorage:', error);
        }
        
        setCurrentView('main');
      } catch (error) {
        console.error('Profile update error:', error);
        alert('Failed to update profile: ' + error.message);
      } finally {
        setIsLoading(false);
      }
    };

    return (
      <div className="edit-profile-container">
        <div className="edit-profile-header">
          <div
            className="back-button"
            onClick={() => setCurrentView('main')}
          >
            <span className="back-button-text">← Back</span>
          </div>
          <span className="edit-profile-title">Edit Profile</span>
        </div>

        <div className="edit-profile-form">
          <div className="profile-input-container">
            <span className="profile-input-label">Name</span>
            <input
              className="profile-input-field"
              placeholder={profileData.username ? profileData.username : "Enter your name"}
              value={profileData.username}
              type="text"
              
              onChange={(e) => {
                setProfileData(prev => ({ ...prev, username: e.target.value }));
              }}
              style={{
                backgroundColor: 'rgba(255, 255, 255, 0.95)',
                border: '2px solid rgba(255, 255, 255, 0.3)',
                borderRadius: '12px',
                padding: '16px',
                fontSize: '16px',
                color: '#333',
                minHeight: '60px',
                transition: 'all 0.3s ease',
                boxShadow: '0 4px 15px rgba(0, 0, 0, 0.1)'
              }}
            />
          </div>

          <div className="profile-input-container">
            <span className="profile-input-label">Age</span>
            <input
              className="profile-input-field"
              placeholder={profileData.age ? profileData.age.toString() : "Enter your age"}
              value={profileData.age}
              type="number"
              
              onChange={(e) => {
                setProfileData(prev => ({ ...prev, age: parseInt(e.target.value) || 0 }));
              }}
              style={{
                backgroundColor: 'rgba(255, 255, 255, 0.95)',
                border: '2px solid rgba(255, 255, 255, 0.3)',
                borderRadius: '12px',
                padding: '16px',
                fontSize: '16px',
                color: '#333',
                minHeight: '60px',
                transition: 'all 0.3s ease',
                boxShadow: '0 4px 15px rgba(0, 0, 0, 0.1)'
              }}
            />
          </div>

          <div className="profile-input-container">
            <span className="profile-input-label">Gender</span>
            <input
              className="profile-input-field"
              placeholder={profileData.gender ? profileData.gender : "Enter your gender"}
              value={profileData.gender}
              type="text"
              
              onChange={(e) => {
                setProfileData(prev => ({ ...prev, gender: e.target.value }));
              }}
              style={{
                backgroundColor: 'rgba(255, 255, 255, 0.95)',
                border: '2px solid rgba(255, 255, 255, 0.3)',
                borderRadius: '12px',
                padding: '16px',
                fontSize: '16px',
                color: '#333',
                minHeight: '60px',
                transition: 'all 0.3s ease',
                boxShadow: '0 4px 15px rgba(0, 0, 0, 0.1)'
              }}
            />
          </div>

          <div className="profile-input-container">
            <span className="profile-input-label">Nationality</span>
            <input
              className="profile-input-field"
              placeholder={profileData.nationality ? profileData.nationality : "Enter your nationality"}
              value={profileData.nationality}
              type="text"
              
              onChange={(e) => {
                setProfileData(prev => ({ ...prev, nationality: e.target.value }));
              }}
              style={{
                backgroundColor: 'rgba(255, 255, 255, 0.95)',
                border: '2px solid rgba(255, 255, 255, 0.3)',
                borderRadius: '12px',
                padding: '16px',
                fontSize: '16px',
                color: '#333',
                minHeight: '60px',
                transition: 'all 0.3s ease',
                boxShadow: '0 4px 15px rgba(0, 0, 0, 0.1)'
              }}
            />
          </div>

          <div className="profile-input-container">
            <span className="profile-input-label">Hobbies (comma separated)</span>
            <input
              className="profile-input-field"
              placeholder={profileData.hobbies && profileData.hobbies.length > 0 ? profileData.hobbies.join(', ') : "e.g., reading, music, sports"}
              value={Array.isArray(profileData.hobbies) ? profileData.hobbies.join(', ') : profileData.hobbies}
              type="text"
              
              onChange={(e) => {
                const hobbiesArray = e.target.value
                  .split(',')
                  .map(h => h.trim())
                  .filter(h => h);
                setProfileData(prev => ({ ...prev, hobbies: hobbiesArray }));
              }}
              style={{
                backgroundColor: 'rgba(255, 255, 255, 0.95)',
                border: '2px solid rgba(255, 255, 255, 0.3)',
                borderRadius: '12px',
                padding: '16px',
                fontSize: '16px',
                color: '#333',
                minHeight: '60px',
                transition: 'all 0.3s ease',
                boxShadow: '0 4px 15px rgba(0, 0, 0, 0.1)'
              }}
            />
          </div>

          <div 
            className="save-profile-button" 
            onClick={handleSaveProfile}
            style={{
              background: 'linear-gradient(135deg, var(--accent-strong) 0%, var(--accent-soft) 100%)',
              borderRadius: '16px',
              padding: '20px',
              textAlign: 'center',
              boxShadow: '0 8px 25px rgba(102, 126, 234, 0.3)',
              transition: 'all 0.3s ease',
              marginTop: '30px',
              border: 'none'
            }}
          >
            <span style={{
              color: 'white',
              fontSize: '18px',
              fontWeight: '600'
            }}>
              {isLoading ? 'Saving...' : 'Save Profile'}
            </span>
          </div>
        </div>
      </div>
    );
  };

  // Main render
  let content;
  switch (currentView) {
    case 'auth':
      content = renderAuth();
      break;
    case 'main':
      content = renderMain();
      break;
    case 'mood-log':
      content = renderMoodLog();
      break;
    case 'recommendations':
      content = renderRecommendations();
      break;
    case 'community':
      content = renderCommunity();
      break;
    case 'chat':
      content = renderChat();
      break;
    case 'ai-chat':
      content = renderAiChat();
      break;
    case 'day-detail':
      content = renderDayDetail();
      break;
    case 'edit-profile':
      content = renderEditProfile();
      break;
    default:
      content = renderAuth();
  }

  const wrappedContent =
    user?.token && currentView !== 'auth' ? renderAppShell(content) : content;

  return <div className="app">{wrappedContent}</div>;
}
