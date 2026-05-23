import { motion } from 'framer-motion';
import { ExternalLink, Github } from 'lucide-react';
import usePortfolioStore from '../../store/usePortfolioStore';

export default function Projects() {
  const { projects } = usePortfolioStore();

  if (!projects || projects.length === 0) return null;

  return (
    <section id="projects" className="py-24 bg-muted/30">
      <div className="container px-4 mx-auto">
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true }}
          transition={{ duration: 0.5 }}
          className="text-center mb-16"
        >
          <h2 className="text-3xl md:text-5xl font-bold tracking-tight mb-4">Featured Projects</h2>
          <div className="w-20 h-1 bg-primary mx-auto rounded-full" />
        </motion.div>

        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
          {projects.map((project, index) => (
            <motion.div
              key={project.id}
              initial={{ opacity: 0, y: 30 }}
              whileInView={{ opacity: 1, y: 0 }}
              viewport={{ once: true }}
              transition={{ delay: index * 0.1, duration: 0.5 }}
              className="group rounded-2xl overflow-hidden bg-card border shadow-sm hover:shadow-xl transition-all duration-300"
            >
              <div className="aspect-video relative overflow-hidden bg-muted">
                {project.image_url ? (
                  <img
                    src={project.image_url}
                    alt={project.title}
                    className="w-full h-full object-cover group-hover:scale-105 transition-transform duration-500"
                  />
                ) : (
                  <div className="w-full h-full flex items-center justify-center text-muted-foreground">
                    No Image
                  </div>
                )}
                {project.is_featured && (
                  <div className="absolute top-4 right-4 bg-primary text-primary-foreground px-3 py-1 rounded-full text-xs font-semibold shadow-md">
                    Featured
                  </div>
                )}
              </div>
              <div className="p-6 space-y-4">
                <h3 className="text-2xl font-bold">{project.title}</h3>
                <p className="text-muted-foreground line-clamp-3">
                  {project.description}
                </p>
                {project.tech_stack && project.tech_stack.length > 0 && (
                  <div className="flex flex-wrap gap-2 pt-2">
                    {project.tech_stack.map((tech) => (
                      <span key={tech} className="px-3 py-1 bg-secondary text-secondary-foreground rounded-full text-xs font-medium">
                        {tech}
                      </span>
                    ))}
                  </div>
                )}
                <div className="flex items-center gap-4 pt-4 mt-auto">
                  {project.github_url && (
                    <a href={project.github_url} target="_blank" rel="noreferrer" className="flex items-center gap-2 text-sm font-medium hover:text-primary transition-colors">
                      <Github size={18} />
                      Code
                    </a>
                  )}
                  {project.live_demo_url && (
                    <a href={project.live_demo_url} target="_blank" rel="noreferrer" className="flex items-center gap-2 text-sm font-medium hover:text-primary transition-colors">
                      <ExternalLink size={18} />
                      Demo
                    </a>
                  )}
                </div>
              </div>
            </motion.div>
          ))}
        </div>
      </div>
    </section>
  );
}
