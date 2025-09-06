import { jsx as _jsx, jsxs as _jsxs } from "react/jsx-runtime";
import React, { useState, useEffect } from 'react';
import { BrowserRouter as Router, Routes, Route, useLocation, useNavigate } from 'react-router-dom';
import { AnimatePresence } from 'framer-motion';
import { AuthProvider } from './contexts/AuthContext';
import LandingPage from './components/LandingPage';
import ChatPage from './components/ChatPage';
import RegisterPage from './components/RegisterPage';
import LoginPage from './components/LoginPage';
import AboutPage from './components/AboutPage';
import HelpPage from './components/HelpPage';
import AccountPage from './components/AccountPage';
import Sidebar from './components/Sidebar';
import LanguageButton from './components/LanguageButton';
import PageTransition from './components/PageTransition';
import TransitionOverlay from './components/TransitionOverlay';
const AppContent = () => {
    const location = useLocation();
    const navigate = useNavigate();
    const [isOverlayVisible, setIsOverlayVisible] = useState(true); // Start with overlay visible
    const [isInitialLoad, setIsInitialLoad] = useState(true);
    // Initial loading effect
    useEffect(() => {
        if (isInitialLoad) {
            setTimeout(() => {
                setIsOverlayVisible(false);
                setTimeout(() => {
                    setIsInitialLoad(false);
                }, 300);
            }, 1000);
        }
    }, [isInitialLoad]);
    useEffect(() => {
        const handleRouteChange = (to) => {
            setIsOverlayVisible(true);
            setTimeout(() => {
                navigate(to);
                setTimeout(() => {
                    setIsOverlayVisible(false);
                }, 300);
            }, 400);
        };
        // Global route change handler
        window.handleRouteChange = handleRouteChange;
    }, [navigate]);
    return (_jsxs("div", { style: { position: 'relative', minHeight: '100vh' }, children: [_jsx(Sidebar, {}), _jsx(LanguageButton, {}), _jsx(TransitionOverlay, { isVisible: isOverlayVisible }), !isInitialLoad && (_jsx(AnimatePresence, { mode: "wait", children: _jsx(PageTransition, { children: _jsxs(Routes, { location: location, children: [_jsx(Route, { path: "/", element: _jsx(LandingPage, {}) }), _jsx(Route, { path: "/chat", element: _jsx(ChatPage, {}) }), _jsx(Route, { path: "/register", element: _jsx(RegisterPage, {}) }), _jsx(Route, { path: "/login", element: _jsx(LoginPage, {}) }), _jsx(Route, { path: "/about", element: _jsx(AboutPage, {}) }), _jsx(Route, { path: "/help", element: _jsx(HelpPage, {}) }), _jsx(Route, { path: "/account", element: _jsx(AccountPage, {}) })] }) }, location.pathname) }))] }));
};
const App = () => {
    return (_jsx(AuthProvider, { children: _jsx(Router, { children: _jsx(AppContent, {}) }) }));
};
export default App;
//# sourceMappingURL=App.js.map