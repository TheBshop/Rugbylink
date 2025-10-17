# RugbyLink - LinkedIn for Rugby

RugbyLink is a comprehensive social networking and job platform designed specifically for the rugby community. It connects rugby players, teams, and agents/scouts in a LinkedIn-style platform tailored for the rugby world.

## Features

### 🏉 User Types
- **Players**: Create detailed profiles showcasing skills, stats, and achievements
- **Teams**: Post contract opportunities and manage applications
- **Agents/Scouts**: Connect with players and teams to facilitate career opportunities

### 📋 Core Functionality
- **Profile System**: Detailed profiles for each user type with relevant information
- **Social Feed**: Share updates, achievements, and connect with the community
- **Contract Opportunities**: Teams can post opportunities, players can apply
- **Messaging System**: Direct communication between users
- **Networking**: Follow/connect with other users in the rugby community
- **Search & Discovery**: Find players, teams, and agents by various criteria

### 🎨 Modern UI/UX
- Responsive design with Bootstrap 5
- Mobile-friendly interface
- Clean, professional look and feel
- Intuitive navigation and user experience

## Technology Stack

- **Backend**: Django 5.0.4
- **Frontend**: Bootstrap 5, HTML5, CSS3, JavaScript
- **Database**: SQLite (development), PostgreSQL (production ready)
- **Image Handling**: Pillow
- **Forms**: django-crispy-forms with Bootstrap styling

## Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd django-template
   ```

2. **Create and activate virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run migrations**
   ```bash
   python manage.py migrate
   ```

5. **Create superuser**
   ```bash
   python manage.py createsuperuser
   ```

6. **Run development server**
   ```bash
   python manage.py runserver
   ```

7. **Access the application**
   - Main site: http://127.0.0.1:8000/
   - Admin panel: http://127.0.0.1:8000/admin/

## Project Structure

```
django-template/
├── accounts/          # Custom user authentication
├── profiles/          # Player, Team, Agent profiles
├── feed/             # Social feed functionality
├── opportunities/    # Contract opportunities and applications
├── messaging/        # Direct messaging system
├── connections/      # Networking and following system
├── core/             # Shared utilities and base templates
├── web_django/       # Main Django project settings
└── manage.py
```

## User Flows

### For Players
1. Sign up as a player
2. Create detailed profile with stats, videos, and achievements
3. Browse contract opportunities
4. Apply for positions
5. Connect with teams and agents
6. Share updates on the social feed

### For Teams
1. Sign up as a team
2. Create team profile with information and logo
3. Post contract opportunities
4. Review and manage applications
5. Connect with players and agents
6. Share team updates

### For Agents
1. Sign up as an agent
2. Create professional profile
3. Connect with players and teams
4. Facilitate connections and opportunities
5. Build professional network

## Development Status

✅ **Completed**
- User authentication system with three user types
- Profile system for players, teams, and agents
- Database models and relationships
- Basic UI/UX with Bootstrap 5
- Admin interface for content management
- Search functionality
- URL routing and basic views

🚧 **In Progress**
- Full implementation of social feed
- Complete messaging system
- Advanced search and filtering
- Real-time notifications

📋 **Planned**
- Advanced analytics and insights
- Mobile app development
- Payment integration for premium features
- API development for third-party integrations

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Support

For support and questions, please contact [your-email@example.com]

---

**RugbyLink** - Connecting the Rugby Community 🏉