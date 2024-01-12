function displayAITools() {
            var aiCategories = document.getElementsByName('aiCategory');
            var selectedCategories = [];
            for(var i = 0; i < aiCategories.length; i++) {
                if(aiCategories[i].checked) {
                    selectedCategories.push(aiCategories[i].value);
                }
            }

            var aiToolListDiv = document.getElementById('aiToolList');

            // Dummy data for demonstration purposes
            var aiTools = {
                "Image Generation": ["DeepArt", "Pix2Pix", "StyleGAN"],
                "Chatbot": ["Dialogflow", "GPT-3", "Rasa"],
                "Data Analysis": ["Tableau", "Power BI", "Google Data Studio"],
                "Voice Recognition": ["Siri", "Google Assistant", "Alexa"],
                "Natural Language Processing": ["IBM Watson", "Google Cloud Natural Language", "SpaCy"],
                "Predictive Analytics": ["SAS", "RapidMiner", "IBM SPSS"],
                "Robotics": ["Boston Dynamics", "ABB Robotics", "KUKA"],
                "Machine Learning": ["TensorFlow", "PyTorch", "Scikit-Learn"],
                "Computer Vision": ["OpenCV", "Adobe Sensei", "Clarifai"],
                "Augmented Reality": ["ARKit", "ARCore", "Vuforia"],
                "Virtual Reality": ["Oculus Rift", "HTC Vive", "PlayStation VR"],
                "Biometrics": ["Clearview AI", "FaceFirst", "NEC"],
                "Blockchain": ["Ethereum", "Hyperledger", "IBM Blockchain"],
                "Internet of Things": ["AWS IoT", "Cisco IoT", "Siemens IoT"]
            };

            aiToolListDiv.innerHTML = '';

            selectedCategories.forEach(function(category) {
                if(aiTools[category]) {
                    aiToolListDiv.innerHTML += '<h3>AI Tools for ' + category + ':</h3><ul>';
                    aiTools[category].forEach(function(tool) {
                        aiToolListDiv.innerHTML += '<li>' + tool + '</li>';
                    });
                    aiToolListDiv.innerHTML += '</ul>';
                }
            });

            if(selectedCategories.length === 0) {
                aiToolListDiv.innerHTML = '<p>Please select at least one AI usage category.</p>';
            }
        }