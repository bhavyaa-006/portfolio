import { motion } from 'framer-motion';
import { Download, Github, Linkedin, Mail } from 'lucide-react';
import usePortfolioStore from '../../store/usePortfolioStore';

export default function Hero() {
  const { settings } = usePortfolioStore();

  if (!settings) return null;

  return (
    <section className="relative min-h-[90vh] flex items-center justify-center overflow-hidden">
      {/* Background gradients */}
      <div className="absolute inset-0 bg-background">
        <div className="absolute top-1/4 left-1/4 w-96 h-96 bg-primary/20 rounded-full blur-[128px] -z-10" />
        <div className="absolute bottom-1/4 right-1/4 w-96 h-96 bg-secondary/20 rounded-full blur-[128px] -z-10" />
      </div>

      <div className="container px-4 mx-auto relative z-10">
        <div className="flex flex-col items-center text-center space-y-8">
          <motion.div
            initial={{ scale: 0.8, opacity: 0 }}
            animate={{ scale: 1, opacity: 1 }}
            transition={{ duration: 0.5 }}
            className="w-32 h-32 md:w-40 md:h-40 rounded-full overflow-hidden border-4 border-background shadow-2xl relative"
          >
            <img
              src={settings.profile_picture_url || 'https://images.unsplash.com/photo-1535713875002-d1d0cf377fde?auto=format&fit=crop&w=800&q=80'}
              alt={settings.owner_name}
              className="w-full h-full object-cover"
            />
          </motion.div>

          <motion.div
            initial={{ y: 20, opacity: 0 }}
            animate={{ y: 0, opacity: 1 }}
            transition={{ delay: 0.2, duration: 0.5 }}
            className="space-y-4 max-w-3xl"
          >
            <h1 className="text-4xl md:text-6xl lg:text-7xl font-bold tracking-tight text-foreground">
              Hi, I'm <span className="text-transparent bg-clip-text bg-gradient-to-r from-primary to-accent-foreground">{settings.owner_name}</span>
            </h1>
            <h2 className="text-xl md:text-3xl font-medium text-muted-foreground">
              {settings.title || 'Software Engineer'}
            </h2>
            <p className="text-lg md:text-xl text-muted-foreground/80 leading-relaxed max-w-2xl mx-auto">
              {settings.bio || 'Building beautiful, scalable, and high-performance applications.'}
            </p>
          </motion.div>

          <motion.div
            initial={{ y: 20, opacity: 0 }}
            animate={{ y: 0, opacity: 1 }}
            transition={{ delay: 0.4, duration: 0.5 }}
            className="flex flex-wrap items-center justify-center gap-4 pt-4"
          >
            {settings.resume_url && (
              <a
                href={settings.resume_url}
                target="_blank"
                rel="noreferrer"
                className="flex items-center gap-2 px-6 py-3 bg-primary text-primary-foreground rounded-full font-medium hover:opacity-90 transition-all hover:scale-105"
              >
                <Download size={20} />
                Download Resume
              </a>
            )}
            <a
              href="#contact"
              className="flex items-center gap-2 px-6 py-3 bg-secondary text-secondary-foreground rounded-full font-medium hover:bg-secondary/80 transition-all hover:scale-105"
            >
              Contact Me
            </a>
          </motion.div>

          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            transition={{ delay: 0.6, duration: 0.5 }}
            className="flex items-center gap-6 pt-8 text-muted-foreground"
          >
            <a href="#" className="hover:text-foreground transition-colors"><Github size={24} /></a>
            <a href="#" className="hover:text-foreground transition-colors"><Linkedin size={24} /></a>
            {settings.contact_email && (
              <a href={`mailto:${settings.contact_email}`} className="hover:text-foreground transition-colors">
                <Mail size={24} />
              </a>
            )}
          </motion.div>
        </div>
      </div>
    </section>
  );
}
