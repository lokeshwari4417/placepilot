from django.core.management.base import BaseCommand

from apps.roadmaps.models import Roadmap, RoadmapTopic


class Command(BaseCommand):
    help = "Seed the database with sample learning roadmaps"

    def handle(self, *args, **options):
        roadmaps_data = [
            {
                "title": "Frontend Developer Roadmap",
                "description": "Comprehensive path to becoming a professional Frontend Developer",
                "target_role": Roadmap.TargetRole.FRONTEND,
                "estimated_weeks": 12,
                "topics": [
                    {"title": "HTML & CSS Fundamentals", "order": 1, "description": "Learn semantic HTML, CSS layouts, and responsive design"},
                    {"title": "JavaScript Basics", "order": 2, "description": "Variables, functions, DOM manipulation, ES6+ features"},
                    {"title": "React Framework", "order": 3, "description": "Components, hooks, state management, routing"},
                    {"title": "TypeScript", "order": 4, "description": "Type system, interfaces, generics"},
                    {"title": "Build Tools & Bundlers", "order": 5, "description": "Webpack, Vite, npm/yarn package managers"},
                    {"title": "Testing", "order": 6, "description": "Unit testing, integration testing, E2E testing"},
                    {"title": "Performance Optimization", "order": 7, "description": "Code splitting, lazy loading, caching strategies"},
                    {"title": "Deployment", "order": 8, "description": "CI/CD, hosting platforms, environment management"},
                ]
            },
            {
                "title": "Backend Developer Roadmap",
                "description": "Complete guide to becoming a Backend Developer",
                "target_role": Roadmap.TargetRole.BACKEND,
                "estimated_weeks": 14,
                "topics": [
                    {"title": "Server-Side Programming", "order": 1, "description": "Python, Node.js, or Java fundamentals"},
                    {"title": "Databases", "order": 2, "description": "SQL, NoSQL, database design, ORM"},
                    {"title": "API Design", "order": 3, "description": "REST, GraphQL, API documentation"},
                    {"title": "Authentication & Security", "order": 4, "description": "JWT, OAuth, encryption, security best practices"},
                    {"title": "Caching & Performance", "order": 5, "description": "Redis, CDN, database optimization"},
                    {"title": "Message Queues", "order": 6, "description": "Celery, RabbitMQ, async processing"},
                    {"title": "Containerization", "order": 7, "description": "Docker, Kubernetes basics"},
                    {"title": "Cloud Services", "order": 8, "description": "AWS, GCP, or Azure fundamentals"},
                ]
            },
            {
                "title": "Full Stack Developer Roadmap",
                "description": "End-to-end path for Full Stack development",
                "target_role": Roadmap.TargetRole.FULL_STACK,
                "estimated_weeks": 20,
                "topics": [
                    {"title": "Frontend Fundamentals", "order": 1, "description": "HTML, CSS, JavaScript, React"},
                    {"title": "Backend Development", "order": 2, "description": "Server-side programming, databases, APIs"},
                    {"title": "System Design", "order": 3, "description": "Architecture patterns, scalability, microservices"},
                    {"title": "DevOps Basics", "order": 4, "description": "CI/CD, monitoring, logging"},
                    {"title": "Testing Strategies", "order": 5, "description": "Full stack testing, TDD, BDD"},
                    {"title": "Project Management", "order": 6, "description": "Agile, Scrum, project planning"},
                ]
            }
        ]

        for roadmap_data in roadmaps_data:
            topics = roadmap_data.pop("topics")
            roadmap, created = Roadmap.objects.get_or_create(
                target_role=roadmap_data["target_role"],
                defaults=roadmap_data
            )
            
            if created:
                self.stdout.write(f"Created roadmap: {roadmap.title}")
                
                for topic_data in topics:
                    RoadmapTopic.objects.create(
                        roadmap=roadmap,
                        **topic_data
                    )
                self.stdout.write(f"  Added {len(topics)} topics")
            else:
                self.stdout.write(f"Roadmap already exists: {roadmap.title}")

        self.stdout.write(self.style.SUCCESS("Roadmaps seeded successfully!"))
