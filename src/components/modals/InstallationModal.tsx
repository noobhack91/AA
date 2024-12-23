import React, { useEffect, useState } from 'react';
import DatePicker from 'react-datepicker';
import "react-datepicker/dist/react-datepicker.css";
import { toast } from 'react-toastify';
import * as api from '../../api';
import { FileDisplay } from '../FileDisplay';
import { BaseModal } from './BaseModal';

interface InstallationModalProps {
  isOpen: boolean;
  onClose: () => void;
  onSubmit: (data: FormData) => Promise<void>;
  consigneeId: string;
}

export const InstallationModal: React.FC<InstallationModalProps> = ({
  isOpen,
  onClose,
  onSubmit,
  consigneeId
}) => {
  const [date, setDate] = useState<Date | null>(null);
  const [file, setFile] = useState<File | null>(null);
  const [existingFiles, setExistingFiles] = useState<string[]>([]);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    if (isOpen && consigneeId) {
      fetchExistingDetails();
    } else {
      // Reset form when modal closes  
      setDate(null);
      setFile(null);
      setExistingFiles([]);
    }
  }, [isOpen, consigneeId]);

  const fetchExistingDetails = async () => {
    setLoading(true);
    try {
      const response = await api.getConsigneeDetails(consigneeId);
      const installationDetails = response.data.installationReport;

      if (installationDetails) {
        setDate(installationDetails.date ? new Date(installationDetails.date) : null);
        setExistingFiles(installationDetails.filePath || []);
      }
    } catch (error) {
      console.error('Error fetching installation details:', error);
      toast.error('Failed to fetch existing installation details');
    } finally {
      setLoading(false);
    }
  };

  const handleDeleteFile = async (url: string) => {
    try {
      await api.deleteFile(url, 'installation');
      setExistingFiles(prev => prev.filter(f => f !== url));
      toast.success('File deleted successfully');
    } catch (error) {
      toast.error('Failed to delete file');
    }
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);

    try {
      if (!date) {
        toast.error('Please select an installation date');
        return;
      }

      const formData = new FormData();
      formData.append('consigneeId', consigneeId);
      formData.append('date', date.toISOString());

      if (file) {
        formData.append('file', file);
      }

      await onSubmit(formData);
      toast.success('Installation details updated successfully');
      onClose();
    } catch (error) {
      toast.error('Failed to update installation details');
    } finally {
      setLoading(false);
    }
  };

  return (
    <BaseModal isOpen={isOpen} onClose={onClose} title="Update Installation Report">
      {loading ? (
        <div className="flex justify-center py-4">
          <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600"></div>
        </div>
      ) : (
        <form onSubmit={handleSubmit} className="space-y-4">
          {/* Installation Date */}
          <div>
            <label className="block text-sm font-medium text-gray-700">Installation Date</label>
            <DatePicker
              selected={date}
              onChange={(selectedDate: Date) => setDate(selectedDate)}
              className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500"
              dateFormat="yyyy-MM-dd"
              placeholderText="Select date"
              required
            />
          </div>

          {/* Installation Report File */}
          <div>
            <label className="block text-sm font-medium text-gray-700">Installation Report</label>
            <input
              type="file"
              onChange={(e) => setFile(e.target.files?.[0] || null)}
              className="mt-1 block w-full"
              accept=".pdf,.jpg,.jpeg,.png"
            />
            <p className="mt-1 text-sm text-gray-500">
              Accepted formats: PDF, JPG, JPEG, PNG
            </p>
          </div>

          {/* Existing Files */}
          {existingFiles.length > 0 && (
            <div className="mt-4">
              <FileDisplay
                files={[existingFiles]}
                onDelete={handleDeleteFile}
              />
            </div>
          )}

          {/* Action Buttons */}
          <div className="flex justify-end space-x-3 mt-6">
            <button
              type="button"
              onClick={onClose}
              className="px-4 py-2 border rounded-md text-gray-600 hover:bg-gray-50"
              disabled={loading}
            >
              Cancel
            </button>
            <button
              type="submit"
              className="px-4 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700 disabled:opacity-50"
              disabled={loading}
            >
              {loading ? 'Saving...' : 'Save'}
            </button>
          </div>
        </form>
      )}
    </BaseModal>
  );
};
