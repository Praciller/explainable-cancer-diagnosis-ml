interface ReportFigureProps {
  src: string;
  alt: string;
  caption: string;
}

export function ReportFigure({ src, alt, caption }: ReportFigureProps) {
  return (
    <figure className="report-figure">
      <img src={src} alt={alt} loading="lazy" />
      <figcaption>{caption}</figcaption>
    </figure>
  );
}
