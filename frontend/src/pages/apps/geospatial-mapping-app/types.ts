export interface DatasetMapsProps {
  datasetUid: string;
  primaryKeyColumn: string;
  bbox?: [number, number, number, number];
  setBBox?: (bbox: [number, number, number, number]) => void;
}
